# utils.py
"""Utility helpers for statistics persistence, sound playback, and simple animations.
"""
import json
import os
import threading
from typing import Dict, Any

import customtkinter as ctk

# ---- Statistics persistence ----
STATS_FILE = os.path.join(os.path.expanduser("~"), ".tic_tac_toe_ai_stats.json")

def load_stats() -> Dict[str, Any]:
    """Load statistics from the JSON file. Returns a dictionary with default values if missing."""
    if not os.path.exists(STATS_FILE):
        return {"games_played": 0, "wins": 0, "losses": 0, "draws": 0, "longest_win_streak": 0, "current_streak": 0, "total_moves": 0}
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"games_played": 0, "wins": 0, "losses": 0, "draws": 0, "longest_win_streak": 0, "current_streak": 0, "total_moves": 0}

def save_stats(stats: Dict[str, Any]) -> None:
    """Write the statistics dictionary to disk atomically."""
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print(f"[utils] Failed to save stats: {e}")

# ---- Sound manager (optional) ----
_SOUND_ENABLED = True
_SOUND_INITIALIZED = False

def _init_sound():
    global _SOUND_INITIALIZED
    if _SOUND_INITIALIZED:
        return
    try:
        import pygame  # type: ignore
        pygame.mixer.init()
        _SOUND_INITIALIZED = True
    except Exception:
        _SOUND_INITIALIZED = False

def play_sound(sound_path: str) -> None:
    """Play a sound file in a non‑blocking way if sounds are enabled and pygame is available."""
    if not _SOUND_ENABLED:
        return
    _init_sound()
    if not _SOUND_INITIALIZED:
        return
    def _play():
        try:
            import pygame  # type: ignore
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except Exception:
            pass
    threading.Thread(target=_play, daemon=True).start()

def set_sound_enabled(enabled: bool) -> None:
    global _SOUND_ENABLED
    _SOUND_ENABLED = enabled

# ---- Simple animation helpers ----
def fade_in(widget: ctk.CTkBaseClass, duration: int = 200) -> None:
    """Fade‑in effect using widget's ``alpha`` property (if supported)."""
    # customtkinter does not expose an alpha attribute directly; we approximate with ``after`` to update bg.
    steps = 10
    interval = max(1, duration // steps)
    def step(opacity: int):
        # placeholder: could change fg_color brightness
        widget.after(interval, lambda: None)
    # No real implementation; left as a hook for future polish.
    return

def pulse(widget: ctk.CTkButton, cycles: int = 2, scale: float = 1.05, interval: int = 100) -> None:
    """Simple pulse effect that briefly enlarges the button and returns to original size."""
    orig_w = widget.cget("width")
    orig_h = widget.cget("height")
    def animate(step: int):
        if step >= cycles * 2:
            widget.configure(width=orig_w, height=orig_h)
            return
        factor = scale if step % 2 == 0 else 1 / scale
        widget.configure(width=int(orig_w * factor), height=int(orig_h * factor))
        widget.after(interval, lambda: animate(step + 1))
    animate(0)

"""End of utils"""
