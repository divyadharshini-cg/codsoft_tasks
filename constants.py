# constants.py
"""Project-wide constants, theme colors, asset paths, and enums.
"""
import os
from enum import Enum, auto

# -------------------- Theme Colors --------------------
BACKGROUND_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
ACCENT_COLOR = "#3B82F6"
SUCCESS_COLOR = "#22C55E"
DANGER_COLOR = "#EF4444"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT_COLOR = "#D1D5DB"  # Light gray

# -------------------- Asset Paths --------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICON_PATH = r"C:/Users/DIVYA DHARSHINI/.gemini/antigravity-ide/brain/e3609dd7-1fe5-4481-a186-f20b962c770b/app_icon_1784003912496.png"
SPLASH_PATH = os.path.join(ASSETS_DIR, "splash.png")
CLICK_SOUND = os.path.join(ASSETS_DIR, "click.wav")
WIN_SOUND = os.path.join(ASSETS_DIR, "win.wav")
LOSE_SOUND = os.path.join(ASSETS_DIR, "lose.wav")
DRAW_SOUND = os.path.join(ASSETS_DIR, "draw.wav")

# -------------------- Enums --------------------
class Difficulty(Enum):
    EASY = auto()      # Random moves
    MEDIUM = auto()    # 70% optimal, 30% random
    HARD = auto()      # Full Minimax
    EXPERT = auto()    # Minimax with Alpha‑Beta pruning

class GameState(Enum):
    IN_PROGRESS = auto()
    X_WON = auto()
    O_WON = auto()
    DRAW = auto()

# -------------------- Misc --------------------
FONT_FAMILY = "Inter"  # Ensure this font is installed or fallback to system default
"""End of constants"""
