from pathlib import Path
from PIL import Image

from app.services.exif_service import extract_exif


def test_exif_fallback_without_metadata(tmp_path: Path):
    image_path = tmp_path / "sample.jpg"
    Image.new("RGB", (640, 480), color="white").save(image_path)

    exif = extract_exif(image_path)

    assert exif["normalized"]["width"] == 640
    assert exif["normalized"]["height"] == 480
    assert exif["normalized"]["focal_length"] is None
