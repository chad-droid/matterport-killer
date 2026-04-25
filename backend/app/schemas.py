from pydantic import BaseModel

from .models import CameraPose, Floorplan, ImageAsset


class ProjectCreateResponse(BaseModel):
    id: str


class AnalyzeResponse(BaseModel):
    project_id: str
    floorplan: Floorplan
    images: list[ImageAsset]
    camera_poses: list[CameraPose]


class ResultsResponse(BaseModel):
    project_id: str
    results: dict
