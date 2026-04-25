from __future__ import annotations

import math
from typing import Iterable


def normalize_point(x: float, y: float, width: float, height: float) -> tuple[float, float]:
    return x / width, y / height


def denormalize_point(x: float, y: float, width: float, height: float) -> tuple[float, float]:
    return x * width, y * height


def direction_vector(angle_degrees: float) -> tuple[float, float]:
    rad = math.radians(angle_degrees)
    return math.cos(rad), math.sin(rad)


def polygon_centroid(points: Iterable[tuple[float, float]]) -> tuple[float, float]:
    pts = list(points)
    if not pts:
        return 0.0, 0.0
    x = sum(p[0] for p in pts) / len(pts)
    y = sum(p[1] for p in pts) / len(pts)
    return x, y


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))
