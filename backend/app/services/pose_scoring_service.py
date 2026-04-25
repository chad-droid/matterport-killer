from __future__ import annotations

from ..models import Room
from ..utils.geometry import direction_vector, polygon_centroid, clamp


WEIGHTS = {
    "room_match": 0.30,
    "fov_geometry": 0.15,
    "wall_alignment": 0.15,
    "visible_feature": 0.20,
    "sequence": 0.15,
    "photographer_prior": 0.05,
}


def _score_wall_alignment(orientation: float) -> float:
    nearest = min(abs((orientation % 90) - k) for k in (0, 90))
    return clamp(1 - nearest / 45, 0, 1)


def _score_fov(fov: float) -> float:
    return clamp(1 - abs(fov - 82) / 60, 0, 1)


def _score_center_facing(candidate: dict, room: Room) -> float:
    cx, cy = polygon_centroid([(p.x, p.y) for p in room.polygon])
    dx = cx - candidate["position"]["x"]
    dy = cy - candidate["position"]["y"]
    vec = direction_vector(candidate["orientation_degrees"])
    dot = (dx * vec[0] + dy * vec[1])
    return 1.0 if dot >= 0 else 0.3


def score_candidate(candidate: dict, room_match_score: float, room: Room, sequence_score: float = 0.5, feature_score: float = 0.5) -> float:
    score = (
        room_match_score * WEIGHTS["room_match"]
        + _score_fov(candidate["fov_degrees"]) * WEIGHTS["fov_geometry"]
        + _score_wall_alignment(candidate["orientation_degrees"]) * WEIGHTS["wall_alignment"]
        + feature_score * WEIGHTS["visible_feature"]
        + sequence_score * WEIGHTS["sequence"]
        + _score_center_facing(candidate, room) * WEIGHTS["photographer_prior"]
    )
    return round(clamp(score, 0.0, 1.0), 4)


def rank_candidates(candidates: list[dict], room_match_score: float, room: Room) -> list[dict]:
    ranked = []
    for cand in candidates:
        scored = dict(cand)
        scored["score"] = score_candidate(cand, room_match_score=room_match_score, room=room)
        ranked.append(scored)
    ranked.sort(key=lambda c: c["score"], reverse=True)
    return ranked
