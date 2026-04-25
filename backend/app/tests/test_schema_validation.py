import json
from pathlib import Path

import jsonschema


def test_example_matches_schema():
    repo_root = Path(__file__).resolve().parents[3]
    schema = json.loads((repo_root / "shared/schemas/camera_pose.schema.json").read_text())
    example = json.loads((repo_root / "shared/schemas/project_output.example.json").read_text())
    jsonschema.validate(example, schema)
