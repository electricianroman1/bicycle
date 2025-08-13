import json
import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))
from telegram_bot.telegram_bot import extract_name


def test_extract_name_json_string():
    payload = {"data": json.dumps({"name": {"value": "Alice"}})}
    assert extract_name(payload) == "Alice"


def test_extract_name_dict_data():
    payload = {"data": {"name": {"value": "Bob"}}}
    assert extract_name(payload) == "Bob"


def test_extract_name_fallback_name():
    payload = {"name": "Charlie"}
    assert extract_name(payload) == "Charlie"


def test_extract_name_fallback_default():
    payload = {}
    assert extract_name(payload) == "Безымянный"


def test_extract_name_invalid_json_with_name():
    payload = {"data": "{", "name": "Fallback"}
    assert extract_name(payload) == "Fallback"


def test_extract_name_invalid_json_without_name():
    payload = {"data": "not json"}
    assert extract_name(payload) == "Безымянный"
