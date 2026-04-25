# Algorithm (MVP Heuristic)

1. Normalize floorplan dimensions from uploaded image.
2. OCR room labels if `pytesseract` is available; otherwise deterministic quadrant inference.
3. Extract EXIF metadata per image.
4. Analyze image filename/features with `HeuristicImageAnalysisProvider`.
5. Rank likely rooms using room-name match + analysis tokens + room confidence.
6. Estimate FOV from (a) 35mm equivalent, (b) focal length with estimated sensor, (c) heuristic default.
7. Generate candidate camera poses:
   - center,
   - inset corners,
   - inset wall midpoints,
   - orientations every 30°.
8. Score candidates via weighted components:
   - room match,
   - FOV geometry,
   - wall alignment,
   - visible features,
   - sequence consistency placeholder,
   - photographer prior (facing room center).
9. Return top pose + alternates + uncertainty reasons.
10. Render overlay markers and camera cones onto floorplan.
