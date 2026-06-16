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
TITLE: str = "Deep Jungle"

# ---------------------------------------------------------------------------
# Colours  (R, G, B)
# ---------------------------------------------------------------------------
COLOUR_BG: tuple[int, int, int] = (34, 85, 34)   # dark jungle green

# ---------------------------------------------------------------------------
# Asset paths
# ---------------------------------------------------------------------------
# ASSETS_DIR resolves to  <project-root>/assets/  regardless of where the
# script is invoked from, because we anchor on this file's location.
ASSETS_DIR: Path = Path(__file__).parent.parent / "assets"
STICKMAN_PATH: Path = ASSETS_DIR / "stickman.png"

# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
# The sprite is scaled so its height matches this value; width scales
# proportionally to preserve the aspect ratio.
PLAYER_HEIGHT: int = 120  # pixels
