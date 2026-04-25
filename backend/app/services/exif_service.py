from __future__ import annotations

from pathlib import Path
from PIL import Image, ExifTags


def _clean_fraction(value):
    try:
        if hasattr(value, "numerator") and hasattr(value, "denominator"):
            return float(value.numerator) / float(value.denominator)
        return float(value)
    except Exception:
        return value


def extract_exif(image_path: Path) -> dict:
    with Image.open(image_path) as img:
        exif_raw = img.getexif()
        width, height = img.size

    tags = {}
    for key, value in exif_raw.items():
        tag_name = ExifTags.TAGS.get(key, str(key))
        tags[tag_name] = _clean_fraction(value)

    normalized = {
        "focal_length": tags.get("FocalLength"),
        "focal_length_35mm": tags.get("FocalLengthIn35mmFilm"),
        "lens_model": tags.get("LensModel"),
        "camera_model": tags.get("Model"),
        "timestamp": tags.get("DateTimeOriginal") or tags.get("DateTime"),
        "width": width,
        "height": height,
    }

    return {"raw": tags, "normalized": normalized}
