"""Player entity: loads and draws the static stickman sprite.

Only loading and drawing are implemented here.
Movement, animation, and combat are TODO stubs — all logic for those
features will be written in the corresponding methods below.
"""
import sys

import pygame

from game import config 
from game.logger import get_logger
from game import input

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
        """
        Load the stick man 
        """

        image = pygame.image.load(config.STICKMAN_PATH).convert_alpha()
        scale = config.PLAYER_HEIGHT / image.get_height()
        new_size = (round(image.get_width() * scale), config.PLAYER_HEIGHT)
        self.image = pygame.transform.scale(image, new_size)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        logger.info(f"Loaded stickman sprite with size {self.width}x{self.height}.")

        # position the player at the bottom centre of the screen
        self.rect = self.image.get_rect()
        self.rect.midbottom = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT)

        # feet should be exactly on the bottom edge of the screen, so adjust y position
        self.rect.y -= self.height
        logger.info(f"Positioned player at {self.rect.topleft} (midbottom: {self.rect.midbottom}).")

        # read speed and attack cooldown from config
        self.speed = config.PLAYER_SPEED


    # ------------------------------------------------------------------
    # Public interface (called every frame by Game)
    # ------------------------------------------------------------------


    def move(self, direction: int) -> None:
        """TODO: Walk the player left or right.

        Args:
            direction: -1 to move left, +1 to move right, 0 to stop.

        Will update a velocity attribute and flip the sprite horizontally
        when the player changes direction.
        """
        # move player left or right, or stop if direction is 0
        
        # Change the player's x position based on the direction and speed
        self.rect.x += direction * self.speed
        # Ensure the player does not move off the screen
        self.rect.x = max(0, min(self.rect.x, config.SCREEN_WIDTH - self.width))
        # Flip the sprite horizontally if changing direction
        if direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        elif direction > 0:
            self.image = pygame.transform.flip(self.image, False, False)

    def update(self) -> None:
        command = input.read_commands()
        if command.move_left:
            self.move(-1)
        elif command.move_right:
            self.move(1)
        else:
            self.move(0)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player sprite on the given surface."""
        surface.blit(self.image, self.rect)

