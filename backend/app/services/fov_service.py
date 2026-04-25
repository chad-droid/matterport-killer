from __future__ import annotations

import math


def estimate_fov(exif: dict, image_analysis: dict | None = None) -> dict:
    normalized = exif.get("normalized", {}) if exif else {}

    f35 = normalized.get("focal_length_35mm")
    if f35:
        fov = math.degrees(2 * math.atan(36 / (2 * float(f35))))
        return {"fov_degrees": round(fov, 1), "confidence": 0.88, "method": "35mm_equivalent"}

    focal = normalized.get("focal_length")
    if focal:
        sensor_width_mm = 6.4
        fov = math.degrees(2 * math.atan(sensor_width_mm / (2 * float(focal))))
        return {"fov_degrees": round(fov, 1), "confidence": 0.67, "method": "focal_plus_estimated_sensor"}

    hint = (image_analysis or {}).get("perspective_hint", "")
    if "wide" in hint:
        return {"fov_degrees": 84.0, "confidence": 0.45, "method": "heuristic_wide"}

    return {"fov_degrees": 72.0, "confidence": 0.35, "method": "default_interior"}
