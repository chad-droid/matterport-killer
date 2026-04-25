from __future__ import annotations

from ..models import ImageAsset, Room
from .image_analysis_service import ImageAnalysisResult


def match_rooms(image: ImageAsset, rooms: list[Room], analysis: ImageAnalysisResult) -> list[dict]:
    filename = image.filename.lower()
    candidates: list[dict] = []

    for room in rooms:
        score = 0.1
        room_name = room.name.lower()
        if room_name.split()[0] in filename:
            score += 0.55
        if any(token in room_name for token in analysis.room_keywords):
            score += 0.25
        if image.timestamp:
            score += 0.05
        score += room.confidence * 0.15
        candidates.append({"room_id": room.id, "room_name": room.name, "score": min(score, 1.0)})

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:3]
