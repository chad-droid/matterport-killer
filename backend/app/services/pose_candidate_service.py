from __future__ import annotations

import math
from ..models import Room
from ..utils.geometry import polygon_centroid


def _inset_point(px: float, py: float, cx: float, cy: float, inset_ratio: float = 0.1) -> tuple[float, float]:
    return px + (cx - px) * inset_ratio, py + (cy - py) * inset_ratio


def generate_pose_candidates(room: Room, fov_degrees: float, orientation_step: int = 30) -> list[dict]:
    points = [(p.x, p.y) for p in room.polygon]
    cx, cy = polygon_centroid(points)

    positions = [{"x": cx, "y": cy, "kind": "center"}]
    for px, py in points:
        ix, iy = _inset_point(px, py, cx, cy)
        positions.append({"x": ix, "y": iy, "kind": "corner_inset"})

    if len(points) >= 2:
        for i in range(len(points)):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % len(points)]
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            ix, iy = _inset_point(mx, my, cx, cy, inset_ratio=0.15)
            positions.append({"x": ix, "y": iy, "kind": "wall_mid"})

    candidates = []
    for pos in positions:
        for angle in range(0, 360, orientation_step):
            candidates.append({
                "position": {"x": pos["x"], "y": pos["y"]},
                "orientation_degrees": angle,
                "fov_degrees": fov_degrees,
                "source": pos["kind"],
            })
    return candidates
