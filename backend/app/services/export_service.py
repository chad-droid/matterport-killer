from __future__ import annotations

from ..models import CameraPose, Floorplan, ImageAsset


def build_project_output(project_id: str, floorplan: Floorplan, images: list[ImageAsset], poses: list[CameraPose]) -> dict:
    pose_by_image = {p.image_id: p for p in poses}
    image_entries = []

    for image in images:
        pose = pose_by_image.get(image.id)
        if not pose:
            continue
        image_entries.append(
            {
                "image_id": image.id,
                "room": pose.room_id,
                "camera": {
                    "position": {"x": round(pose.position.x, 2), "y": round(pose.position.y, 2)},
                    "orientation_degrees": pose.orientation_degrees,
                    "direction_vector": {"dx": pose.direction_vector.dx, "dy": pose.direction_vector.dy},
                    "field_of_view_degrees": pose.fov_degrees,
                    "height_estimate": "standing_eye_level",
                },
                "perspective_description": pose.perspective_description,
                "visible_elements": image.visual_features,
                "confidence": pose.confidence,
                "alternates": [
                    {
                        "position": {"x": round(a.position.x, 2), "y": round(a.position.y, 2)},
                        "orientation_degrees": a.orientation_degrees,
                        "confidence": a.confidence,
                    }
                    for a in pose.alternates
                ],
                "uncertainty_reasons": pose.uncertainty_reasons,
            }
        )

    return {
        "project_id": project_id,
        "floorplan": {
            "width": floorplan.width,
            "height": floorplan.height,
            "coordinate_system": floorplan.normalized_coordinate_system,
        },
        "images": image_entries,
    }
