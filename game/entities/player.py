"""Player entity: loads and draws the static stickman sprite.

Only loading and drawing are implemented here.
Movement, animation, and combat are TODO stubs — all logic for those
features will be written in the corresponding methods below.
"""
import sys

import pygame

from game.config import PLAYER_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, STICKMAN_PATH
from game.logger import get_logger

logger = get_logger()


class Player:
    """The player character (stickman).

    Currently only loads a PNG sprite and draws it statically.
    The sprite is centred horizontally and stands on the bottom edge
    of the screen.

    Attributes:
        image: The scaled pygame surface for the stickman.
        rect:  The bounding rectangle used for positioning and (later) collision.
    """

    def __init__(self) -> None:
        self._load_sprite()

        # Place the player: horizontally centred, feet on the ground.
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_sprite(self) -> None:
        """Load stickman.png from disk and scale it to PLAYER_HEIGHT.

        Preserves the image's aspect ratio.
        Logs an error and exits cleanly if the file is missing.
        """
        if not STICKMAN_PATH.exists():
            logger.error(
                "Asset not found: %s — place stickman.png in the assets/ folder",
                STICKMAN_PATH,
            )
            pygame.quit()
            sys.exit(1)

        raw: pygame.Surface = pygame.image.load(str(STICKMAN_PATH)).convert_alpha()
        original_w, original_h = raw.get_size()

        # Scale height to PLAYER_HEIGHT; derive width to keep the aspect ratio.
        scale_factor: float = PLAYER_HEIGHT / original_h
        scaled_w: int = int(original_w * scale_factor)

        self.image: pygame.Surface = pygame.transform.smoothscale(
            raw, (scaled_w, PLAYER_HEIGHT)
        )
        logger.info(
            "Assets loaded — stickman scaled to %dx%d px", scaled_w, PLAYER_HEIGHT
        )

    # ------------------------------------------------------------------
    # Public interface (called every frame by Game)
    # ------------------------------------------------------------------

    def update(self) -> None:
        """TODO: Update player state each frame.

        Will apply velocity, step the animation frame, check ground
        collision, and tick down attack / hurt timers.
        """
        pass

    def move(self, direction: int) -> None:
        """TODO: Walk the player left or right.

        Args:
            direction: -1 to move left, +1 to move right, 0 to stop.

        Will update a velocity attribute and flip the sprite horizontally
        when the player changes direction.
        """
        pass

    def attack(self) -> None:
        """TODO: Trigger the player's melee attack.

        Will guard against attacking while already mid-swing, start the
        attack animation, and notify the combat system to test for hits
        against nearby enemies.
        """
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Blit the stickman sprite onto *surface* at its current position.

        Args:
            surface: The pygame surface to draw onto (usually the screen).
        """
        surface.blit(self.image, self.rect)
