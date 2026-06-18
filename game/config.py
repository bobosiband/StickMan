"""All game-wide constants live here.

Import from this module instead of hard-coding numbers anywhere else.
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60
TITLE: str = "Stickman Game"

# ---------------------------------------------------------------------------
# Colours  (R, G, B)
# ---------------------------------------------------------------------------
COLOUR_BG: tuple[int, int, int] = (255, 255, 255)   # dark jungle green

# ---------------------------------------------------------------------------
# Asset paths
# ---------------------------------------------------------------------------
# ASSETS_DIR resolves to  <project-root>/assets/  regardless of where the
# script is invoked from, because we anchor on this file's location.
ASSETS_DIR: Path = Path(__file__).parent.parent / "assets"
PLAYER_DIR = ASSETS_DIR / "player"
STICKMAN_PATH: Path = PLAYER_DIR / "normal.png"

# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
# The sprite is scaled so its height matches this value; width scales
# proportionally to preserve the aspect ratio.
PLAYER_HEIGHT: int = 120  # pixels
PLAYER_SPEED: int = 5  # pixels per frame

