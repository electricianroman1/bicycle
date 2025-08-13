import json
import sys
from pathlib import Path
import pytest

# Ensure project root is on sys.path for imports
sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.app.models import LSSSheet


@pytest.mark.parametrize(
    "payload, expected_name",
    [
        ({"data": json.dumps({"name": {"value": "Rick"}})}, "Rick"),
        ({"data": {}, "name": "Morty"}, "Morty"),
        ({"data": {}}, "Безымянный"),
    ],
)
def test_lsssheet_name_resolution(payload, expected_name):
    sheet = LSSSheet(payload=payload, name=None)
    assert sheet.name == expected_name
