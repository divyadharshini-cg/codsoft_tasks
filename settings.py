# settings.py
"""Manages user preferences such as difficulty, game mode, starting symbol, and sound options.
Persists these configurations in a JSON file in the user's home directory.
"""
import os
import json
from typing import Dict, Any

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".tic_tac_toe_ai_settings.json")

DEFAULT_SETTINGS = {
    "difficulty": "MEDIUM",       # EASY, MEDIUM, HARD, EXPERT
    "game_mode": "vs_ai",         # vs_ai, vs_player
    "player_symbol": "X",         # X, O
    "sound_enabled": True
}

def load_settings() -> Dict[str, Any]:
    """Loads user configurations from the JSON storage file, or returns default values."""
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            settings = DEFAULT_SETTINGS.copy()
            # Overwrite defaults with saved keys
            for key in settings:
                if key in data:
                    settings[key] = data[key]
            return settings
    except Exception:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings: Dict[str, Any]) -> None:
    """Saves the current configuration dictionary to disk."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"[settings] Failed to save settings: {e}")
