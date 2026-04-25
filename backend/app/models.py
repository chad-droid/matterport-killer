from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float
    y: float


class DirectionVector(BaseModel):
    dx: float
    dy: float


class Room(BaseModel):
    id: str
    name: str
    polygon: list[Point]
    confidence: float = Field(ge=0, le=1)
    source: Literal["ocr", "inferred", "manual_seed", "unknown"] = "unknown"


class Floorplan(BaseModel):
    id: str
    file_path: str
    width: int
    height: int
    normalized_coordinate_system: str = "normalized_image_pixels"
    rooms: list[Room] = Field(default_factory=list)


class ImageAsset(BaseModel):
    id: str
    filename: str
    file_path: str
    width: int
    height: int
    exif: dict = Field(default_factory=dict)
    timestamp: str | None = None
    room_candidates: list[dict] = Field(default_factory=list)
    visual_features: list[str] = Field(default_factory=list)


class AlternatePose(BaseModel):
    position: Point
    orientation_degrees: float
    confidence: float


class CameraPose(BaseModel):
    image_id: str
    room_id: str
    position: Point
    orientation_degrees: float
    direction_vector: DirectionVector
    fov_degrees: float
    confidence: float
    perspective_description: str
    alternates: list[AlternatePose] = Field(default_factory=list)
    uncertainty_reasons: list[str] = Field(default_factory=list)


class Project(BaseModel):
    id: str
    floorplan: Floorplan | None = None
    images: list[ImageAsset] = Field(default_factory=list)
    rooms: list[Room] = Field(default_factory=list)
    camera_poses: list[CameraPose] = Field(default_factory=list)
