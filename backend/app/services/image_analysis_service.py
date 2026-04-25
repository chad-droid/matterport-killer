from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class ImageAnalysisResult:
    perspective_hint: str
    visual_features: list[str]
    room_keywords: list[str]


class ImageAnalysisProvider:
    def analyze(self, image_path: Path) -> ImageAnalysisResult:
        raise NotImplementedError


class HeuristicImageAnalysisProvider(ImageAnalysisProvider):
    def analyze(self, image_path: Path) -> ImageAnalysisResult:
        name = image_path.stem.lower()
        tokens = re.split(r"[^a-z0-9]+", name)
        room_keywords = [t for t in tokens if t in {"kitchen", "bedroom", "bathroom", "living", "dining", "garage", "office"}]
        perspective_hint = "interior wide view" if any(t in name for t in ["wide", "overview", "room"]) else "interior perspective"
        visual_features = [t for t in tokens if t in {"island", "window", "stairs", "sink", "shower", "fireplace"}]
        return ImageAnalysisResult(perspective_hint=perspective_hint, visual_features=visual_features, room_keywords=room_keywords)
