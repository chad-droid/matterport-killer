from app.utils.geometry import normalize_point, denormalize_point, direction_vector


def test_normalization_round_trip():
    x, y = normalize_point(50, 25, 200, 100)
    dx, dy = denormalize_point(x, y, 200, 100)
    assert round(dx, 5) == 50
    assert round(dy, 5) == 25


def test_direction_vector():
    dx, dy = direction_vector(0)
    assert round(dx, 4) == 1
    assert round(dy, 4) == 0
