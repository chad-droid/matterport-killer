from __future__ import annotations

import json
import math
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw

from .config import PROJECTS_DIR
from .models import AlternatePose, CameraPose, DirectionVector, ImageAsset, Point, Project
from .schemas import AnalyzeResponse, ProjectCreateResponse, ResultsResponse
from .services.exif_service import extract_exif
from .services.export_service import build_project_output
from .services.floorplan_service import parse_floorplan
from .services.fov_service import estimate_fov
from .services.image_analysis_service import HeuristicImageAnalysisProvider
from .services.pose_candidate_service import generate_pose_candidates
from .services.pose_scoring_service import rank_candidates
from .services.room_matching_service import match_rooms
from .utils.geometry import direction_vector

app = FastAPI(title="Matterport Killer MVP")
analysis_provider = HeuristicImageAnalysisProvider()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


def project_dir(project_id: str) -> Path:
    return PROJECTS_DIR / project_id


def project_file(project_id: str) -> Path:
    return project_dir(project_id) / "project.json"


def load_project(project_id: str) -> Project:
    pf = project_file(project_id)
    if not pf.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    return Project.model_validate_json(pf.read_text())


def save_project(project: Project) -> None:
    pd = project_dir(project.id)
    pd.mkdir(parents=True, exist_ok=True)
    project_file(project.id).write_text(project.model_dump_json(indent=2))


@app.post("/projects", response_model=ProjectCreateResponse)
def create_project() -> ProjectCreateResponse:
    project_id = f"project_{uuid.uuid4().hex[:8]}"
    project = Project(id=project_id)
    save_project(project)
    return ProjectCreateResponse(id=project_id)


@app.post("/projects/{project_id}/floorplan")
async def upload_floorplan(project_id: str, file: UploadFile = File(...)) -> dict:
    project = load_project(project_id)
    pdir = project_dir(project_id)
    floorplan_path = pdir / f"floorplan_{file.filename}"
    floorplan_path.write_bytes(await file.read())
    floorplan = parse_floorplan(project_id, floorplan_path)
    project.floorplan = floorplan
    project.rooms = floorplan.rooms
    save_project(project)
    return {"ok": True, "rooms_detected": len(project.rooms)}


@app.post("/projects/{project_id}/images")
async def upload_images(project_id: str, files: list[UploadFile] = File(...)) -> dict:
    project = load_project(project_id)
    pdir = project_dir(project_id)
    images_dir = pdir / "images"
    images_dir.mkdir(exist_ok=True)

    for upload in files:
        image_path = images_dir / upload.filename
        image_path.write_bytes(await upload.read())
        exif = extract_exif(image_path)
        normalized = exif.get("normalized", {})
        image = ImageAsset(
            id=upload.filename,
            filename=upload.filename,
            file_path=str(image_path),
            width=normalized.get("width", 0),
            height=normalized.get("height", 0),
            exif=exif,
            timestamp=normalized.get("timestamp"),
        )
        project.images.append(image)

    save_project(project)
    return {"ok": True, "uploaded": len(files)}


@app.post("/projects/{project_id}/analyze", response_model=AnalyzeResponse)
def analyze(project_id: str) -> AnalyzeResponse:
    project = load_project(project_id)
    if not project.floorplan:
        raise HTTPException(status_code=400, detail="Upload a floorplan first")
    if not project.images:
        raise HTTPException(status_code=400, detail="Upload images first")

    poses: list[CameraPose] = []

    for image in project.images:
        analysis = analysis_provider.analyze(Path(image.file_path))
        room_candidates = match_rooms(image, project.rooms, analysis)
        image.room_candidates = room_candidates
        image.visual_features = analysis.visual_features

        best_room_candidate = room_candidates[0]
        room = next(r for r in project.rooms if r.id == best_room_candidate["room_id"])
        fov = estimate_fov(image.exif, {"perspective_hint": analysis.perspective_hint})
        candidates = generate_pose_candidates(room, fov["fov_degrees"], orientation_step=30)
        ranked = rank_candidates(candidates, room_match_score=best_room_candidate["score"], room=room)

        top = ranked[0]
        alt = ranked[1:4]
        dx, dy = direction_vector(top["orientation_degrees"])
        uncertainty = []
        if fov["confidence"] < 0.5:
            uncertainty.append("fov_estimate_low_confidence")
        if len(room_candidates) > 1 and abs(room_candidates[0]["score"] - room_candidates[1]["score"]) < 0.15:
            uncertainty.append("multiple_rooms_plausible")

        pose_confidence = round(min(0.99, top["score"] * 0.7 + fov["confidence"] * 0.3), 3)
        perspective_description = (
            f"{analysis.perspective_hint.capitalize()} from {room.name} facing {int(top['orientation_degrees'])} degrees."
        )

        poses.append(
            CameraPose(
                image_id=image.id,
                room_id=room.name,
                position=Point(x=top["position"]["x"], y=top["position"]["y"]),
                orientation_degrees=top["orientation_degrees"],
                direction_vector=DirectionVector(dx=round(dx, 3), dy=round(dy, 3)),
                fov_degrees=fov["fov_degrees"],
                confidence=pose_confidence,
                perspective_description=perspective_description,
                alternates=[
                    AlternatePose(
                        position=Point(x=a["position"]["x"], y=a["position"]["y"]),
                        orientation_degrees=a["orientation_degrees"],
                        confidence=round(a["score"], 3),
                    )
                    for a in alt
                ],
                uncertainty_reasons=uncertainty,
            )
        )

    project.camera_poses = poses
    save_project(project)
    output = build_project_output(project_id, project.floorplan, project.images, poses)
    (project_dir(project_id) / "output.json").write_text(json.dumps(output, indent=2))

    return AnalyzeResponse(project_id=project.id, floorplan=project.floorplan, images=project.images, camera_poses=poses)


@app.get("/projects/{project_id}/results", response_model=ResultsResponse)
def results(project_id: str) -> ResultsResponse:
    project = load_project(project_id)
    if not project.floorplan:
        raise HTTPException(status_code=404, detail="No floorplan")
    output = build_project_output(project_id, project.floorplan, project.images, project.camera_poses)
    return ResultsResponse(project_id=project_id, results=output)


@app.get("/projects/{project_id}/overlay")
def overlay(project_id: str):
    project = load_project(project_id)
    if not project.floorplan:
        raise HTTPException(status_code=404, detail="No floorplan")
    img = Image.open(project.floorplan.file_path).convert("RGB")
    draw = ImageDraw.Draw(img, "RGBA")

    for pose in project.camera_poses:
        x, y = pose.position.x, pose.position.y
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(220, 0, 0, 220))
        angle = math.radians(pose.orientation_degrees)
        for delta in (-pose.fov_degrees / 2, pose.fov_degrees / 2):
            ray = math.radians(pose.orientation_degrees + delta)
            x2, y2 = x + 80 * math.cos(ray), y + 80 * math.sin(ray)
            draw.line((x, y, x2, y2), fill=(255, 100, 0, 180), width=2)
        draw.text((x + 8, y - 8), f"{pose.image_id} ({pose.confidence:.2f})", fill=(0, 0, 255, 255))

    out_path = project_dir(project_id) / "overlay.png"
    img.save(out_path)
    return FileResponse(out_path)
