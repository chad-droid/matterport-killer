from __future__ import annotations

from pathlib import Path

import cv2

from ..models import Floorplan, Point, Room
from ..utils.image_io import ensure_image

ROOM_KEYWORDS = ["kitchen", "living", "bedroom", "bath", "dining", "garage", "office", "hall"]


def _extract_labels_with_ocr(image_path: Path) -> list[tuple[str, tuple[int, int]]]:
    try:
        import pytesseract
    except Exception:
        return []

    img = cv2.imread(str(image_path))
    if img is None:
        return []
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    labels = []
    for i, text in enumerate(data.get("text", [])):
        token = (text or "").strip().lower()
        if token and any(k in token for k in ROOM_KEYWORDS):
            x = int(data["left"][i] + data["width"][i] / 2)
            y = int(data["top"][i] + data["height"][i] / 2)
            labels.append((text.strip(), (x, y)))
    return labels


def _infer_rooms_from_labels(labels: list[tuple[str, tuple[int, int]]], width: int, height: int) -> list[Room]:
    rooms: list[Room] = []
    box_w = max(80, width // 8)
    box_h = max(80, height // 8)
    for idx, (name, (cx, cy)) in enumerate(labels):
        x0, y0 = max(0, cx - box_w // 2), max(0, cy - box_h // 2)
        x1, y1 = min(width, cx + box_w // 2), min(height, cy + box_h // 2)
        polygon = [Point(x=x0, y=y0), Point(x=x1, y=y0), Point(x=x1, y=y1), Point(x=x0, y=y1)]
        rooms.append(Room(id=f"room_{idx + 1}", name=name.title(), polygon=polygon, confidence=0.6, source="ocr"))
    return rooms


def _fallback_rooms(width: int, height: int) -> list[Room]:
    w2, h2 = width // 2, height // 2
    boxes = [
        ("Living Room", (0, 0, w2, h2)),
        ("Kitchen", (w2, 0, width, h2)),
        ("Bedroom", (0, h2, w2, height)),
        ("Bathroom", (w2, h2, width, height)),
    ]
    rooms: list[Room] = []
    for idx, (name, (x0, y0, x1, y1)) in enumerate(boxes):
        polygon = [Point(x=x0, y=y0), Point(x=x1, y=y0), Point(x=x1, y=y1), Point(x=x0, y=y1)]
        rooms.append(Room(id=f"room_{idx + 1}", name=name, polygon=polygon, confidence=0.35, source="inferred"))
    return rooms


def parse_floorplan(project_id: str, floorplan_path: Path) -> Floorplan:
    resolved_path, width, height = ensure_image(floorplan_path)

    labels = _extract_labels_with_ocr(resolved_path)
    rooms = _infer_rooms_from_labels(labels, width, height)
    if not rooms:
        rooms = _fallback_rooms(width, height)

    return Floorplan(
        id=f"floorplan_{project_id}",
        file_path=str(resolved_path),
        width=width,
        height=height,
        rooms=rooms,
    )
