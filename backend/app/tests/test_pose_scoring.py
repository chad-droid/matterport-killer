from app.models import Point, Room
from app.services.pose_candidate_service import generate_pose_candidates
from app.services.pose_scoring_service import rank_candidates


def _room() -> Room:
    return Room(
        id="room_1",
        name="Kitchen",
        polygon=[Point(x=0, y=0), Point(x=100, y=0), Point(x=100, y=100), Point(x=0, y=100)],
        confidence=0.7,
        source="inferred",
    )


def test_candidate_generation_non_empty():
    candidates = generate_pose_candidates(_room(), fov_degrees=80, orientation_step=30)
    assert len(candidates) >= 24


def test_pose_scoring_determinism():
    room = _room()
    candidates = generate_pose_candidates(room, fov_degrees=80, orientation_step=90)
    ranked_1 = rank_candidates(candidates, room_match_score=0.8, room=room)
    ranked_2 = rank_candidates(candidates, room_match_score=0.8, room=room)
    assert ranked_1[0]["score"] == ranked_2[0]["score"]
    assert ranked_1[0]["orientation_degrees"] == ranked_2[0]["orientation_degrees"]
