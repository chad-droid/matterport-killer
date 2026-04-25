from app.services.fov_service import estimate_fov


def test_estimate_fov_35mm():
    exif = {"normalized": {"focal_length_35mm": 18}}
    out = estimate_fov(exif)
    assert out["method"] == "35mm_equivalent"
    assert out["fov_degrees"] > 80


def test_estimate_fov_default():
    out = estimate_fov({}, {"perspective_hint": "interior perspective"})
    assert out["fov_degrees"] == 72.0
