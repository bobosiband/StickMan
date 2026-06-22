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

# states 
class State:
    """
    player states 
    bhorile is dead
    """
    IDLE = "idle"
    WALKING = "walking"
    JUMPING = ["up", "down"]
    ATTACKING = "attacking"
    INJURED = "inured"
    DEAD = "Bhorile"
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

        self.sprites = {}

        # Loop through your config paths and pre-load/scale every state image
        for state, path in config.STATE_PATHS.items():
            raw_image = pygame.image.load(path).convert_alpha()
            scale = config.PLAYER_HEIGHT / raw_image.get_height()
            new_size = (round(raw_image.get_width() * scale), config.PLAYER_HEIGHT)
            
            # Save the scaled image to our dictionary
            self.sprites[state] = pygame.transform.scale(raw_image, new_size)

        self.state = State.IDLE
        self.image = self.sprites[self.state]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        logger.info(f"Loaded stickman sprite with size {self.width}x{self.height}.")

        # position the player at the bottom centre of the screen
        self.rect = self.image.get_rect()
        self.rect.midbottom = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT)
        logger.info(f"Positioned player at {self.rect.topleft} (midbottom: {self.rect.midbottom}).")

        # read speed and attack cooldown from config
        self.speed = config.PLAYER_SPEED

        # keep original for direction flipping
        self._base_image = self.image
        self._facing_left = False

        # set the initial state to idle
        self.state = State.IDLE

        # other types of images for different states will be added later, for now we just have one



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
        # Flip the sprite from the original when direction changes
        if direction < 0 and not self._facing_left:
            self._facing_left = True
            self.image = pygame.transform.flip(self._base_image, True, False)
        elif direction > 0 and self._facing_left:
            self._facing_left = False
            self.image = self._base_image

    

    def update(self, commands) -> None:
        direction = 0

        if commands.move_left:
            direction -= 1

        if commands.move_right:
            direction += 1

        if direction != 0:
            self.state = State.WALKING
        else:
            self.state = State.IDLE

        self.move(direction)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player sprite on the given surface."""
        surface.blit(self.image, self.rect)

