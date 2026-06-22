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
    JUMPING = "jumping"
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
        
        logger.info(f"Loaded sprites dictionary keys: {list(self.sprites.keys())}")
        
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

        # Direction tracking
        self._facing_left = False

        # Physics tracking variables
        self.velocity_y = 0.0
        self.jump_force = config.PLAYER_JUMP_FORCE  # Recommend a negative integer like -15
        self.gravity = config.GRAVITY            # Recommend a positive float like 0.8
        self.is_grounded = True

    # ------------------------------------------------------------------
    # Public interface (called every frame by Game)
    # ------------------------------------------------------------------

    def set_state(self, new_state: str) -> None:
        """Changes the player state and swaps the displayed image."""
        if self.state == new_state:
            return  # Skip if the state hasn't actually changed

        self.state = new_state
        
        # Grab the base image for this state
        base_sprite = self.sprites[self.state]
        
        # Apply the correct direction flip immediately
        if self._facing_left:
            self.image = pygame.transform.flip(base_sprite, True, False)
        else:
            self.image = base_sprite
            
        # Update width/height if your different state sprites have different widths
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        # Keep the bottom of the rectangle locked to the ground after resizing
        bottom_center = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = bottom_center

    def move(self, direction: list[int]) -> None:
        """Handles movement calculation and physics equations."""
        horizontal_direction = direction[0]
        vertical_direction = direction[1]

        # --- 1. Horizontal Movement ---
        self.rect.x += horizontal_direction * self.speed
        self.rect.x = max(0, min(self.rect.x, config.SCREEN_WIDTH - self.width))
        
        # Flip the current state's image if direction changes
        if horizontal_direction < 0 and not self._facing_left:
            self._facing_left = True
            self.image = pygame.transform.flip(self.sprites[self.state], True, False)
        elif horizontal_direction > 0 and self._facing_left:
            self._facing_left = False
            self.image = self.sprites[self.state]

        # --- 2. Vertical Movement & Jumping Mechanics ---
        if vertical_direction < 0 and self.is_grounded:
            self.velocity_y = self.jump_force
            self.is_grounded = False

        # Apply continuous downward gravitational pull when airborne
        if not self.is_grounded:
            self.velocity_y += self.gravity
            self.rect.y += round(self.velocity_y)

        # --- 3. Ground Collision Checks ---
        if self.rect.bottom >= config.SCREEN_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT
            self.velocity_y = 0.0
            self.is_grounded = True

    def update(self, commands) -> None:
        # direction = [x, y]
        direction = [0, 0]

        if commands.move_left:
            direction[0] -= 1
        if commands.move_right:
            direction[0] += 1
        if commands.jump:
            direction[1] -= 1
        if commands.attack:
            pass 

        # Calculate coordinates and position values first
        self.move(direction)

        # Evaluate and process state machine textures after positions resolve
        if not self.is_grounded:
            self.set_state(State.JUMPING)
        elif direction[0] != 0:
            self.set_state(State.WALKING)
        else:
            self.set_state(State.IDLE)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player sprite on the given surface."""
        surface.blit(self.image, self.rect)
