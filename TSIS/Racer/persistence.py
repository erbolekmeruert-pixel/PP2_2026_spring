import json
from pathlib import Path


SETTINGS_PATH = Path(__file__).with_name("settings.json")
LEADERBOARD_PATH = Path(__file__).with_name("leaderboard.json")

DEFAULT_SETTINGS = {
    "sound_enabled": True,
    "car_color": "blue",
    "difficulty": "normal",
}


def _ensure_json_file(path, default_value):
    if not path.exists():
        path.write_text(json.dumps(default_value, indent=2), encoding="utf-8")


def load_settings():
    _ensure_json_file(SETTINGS_PATH, DEFAULT_SETTINGS)
    data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    return {**DEFAULT_SETTINGS, **data}


def save_settings(settings):
    SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")


def load_leaderboard():
    _ensure_json_file(LEADERBOARD_PATH, [])
    data = json.loads(LEADERBOARD_PATH.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    return []


def save_leaderboard(entries):
    ordered = sorted(
        entries,
        key=lambda item: (item.get("score", 0), item.get("distance", 0)),
        reverse=True,
    )[:10]
    LEADERBOARD_PATH.write_text(json.dumps(ordered, indent=2), encoding="utf-8")


def add_leaderboard_entry(entry):
    entries = load_leaderboard()
    entries.append(entry)
    save_leaderboard(entries)
    