"""Player entity module for managing the stickman character."""

import sys
import pygame
import random

from game import config 
from game.logger import get_logger
from game import input

logger = get_logger()

class State:
    """Player state constants and attack categories."""
    ATTACKING_TYPES = ["punching", "vodloza"]
    
    IDLE = "idle"
    WALKING = "walking"
    JUMPING = "jumping"
    INJURED = "inured"
    DEAD = "dead"
    DUCKING = "ducking"

class Player:
    """The player character (stickman) handling physics, movement, and combat."""

    def __init__(self) -> None:
        """Initialise player properties and pre-load scaled sprite surfaces."""
        self.sprites = {}

        for state, path in config.STATE_PATHS.items():
            raw_image = pygame.image.load(path).convert_alpha()
            scale = config.PLAYER_HEIGHT / raw_image.get_height()
            new_size = (round(raw_image.get_width() * scale), config.PLAYER_HEIGHT)
            self.sprites[state] = pygame.transform.scale(raw_image, new_size)
        
        logger.info(f"Loaded sprites dictionary keys: {list(self.sprites.keys())}")
        
        self.state = State.IDLE
        self.image = self.sprites[self.state]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        logger.info(f"Loaded stickman sprite with size {self.width}x{self.height}.")

        self.rect = self.image.get_rect()
        self.rect.midbottom = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT)
        logger.info(f"Positioned player at {self.rect.topleft} (midbottom: {self.rect.midbottom}).")

        self.speed = config.PLAYER_SPEED
        self._facing_left = False

        self.velocity_y = 0.0
        self.jump_force = config.PLAYER_JUMP_FORCE  
        self.gravity = config.GRAVITY            
        self.is_grounded = True

        self.attack_timer = 0
        self.attack_lunge_speed = 8  

    def set_state(self, new_state: str) -> None:
        """Changes the player state and swaps the displayed image."""
        if self.state == new_state:
            return  

        self.state = new_state
        base_sprite = self.sprites[self.state]
        
        if self._facing_left:
            self.image = pygame.transform.flip(base_sprite, True, False)
        else:
            self.image = base_sprite
            
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        bottom_center = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = bottom_center

    def move(self, direction: list[int]) -> None:
        """Handles movement calculation and physics equations."""
        if self.state in State.ATTACKING_TYPES:
            lunge_direction = -1 if self._facing_left else 1
            current_lunge = lunge_direction * max(1, round(self.attack_lunge_speed * (self.attack_timer / config.PLAYER_ATTACK_DURATION)))
            self.rect.x += current_lunge
        elif self.state == State.DUCKING:
            pass
        else:
            horizontal_direction = direction[0]
            self.rect.x += horizontal_direction * self.speed
            
            if horizontal_direction < 0 and not self._facing_left:
                self._facing_left = True
                self.image = pygame.transform.flip(self.sprites[self.state], True, False)
            elif horizontal_direction > 0 and self._facing_left:
                self._facing_left = False
                self.image = self.sprites[self.state]

        self.rect.x = max(0, min(self.rect.x, config.SCREEN_WIDTH - self.width))
            
        vertical_direction = direction[1]

        if vertical_direction < 0 and self.is_grounded and self.state not in State.ATTACKING_TYPES and self.state != State.DUCKING:
            self.velocity_y = self.jump_force
            self.is_grounded = False

        if not self.is_grounded:
            self.velocity_y += self.gravity
            self.rect.y += round(self.velocity_y)

        if self.rect.bottom >= config.SCREEN_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT
            self.velocity_y = 0.0
            self.is_grounded = True

    def update(self, commands) -> None:
        """Updates physics processing, command inputs, and timers every frame."""
        direction = [0, 0]

        if commands.move_left:
            direction[0] -= 1
        if commands.move_right:
            direction[0] += 1
        if commands.jump:
            direction[1] -= 1

        if self.state in State.ATTACKING_TYPES:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.set_state(State.IDLE)  

        if commands.attack and self.state not in State.ATTACKING_TYPES:
            self.attack_timer = config.PLAYER_ATTACK_DURATION
            random_attack = random.choice(State.ATTACKING_TYPES)
            self.set_state(random_attack)

        if self.state not in State.ATTACKING_TYPES:
            if commands.duck and self.is_grounded:
                self.set_state(State.DUCKING)
            elif not self.is_grounded:
                self.set_state(State.JUMPING)
            elif direction[0] != 0:
                self.set_state(State.WALKING)
            else:
                self.set_state(State.IDLE)

        self.move(direction)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player sprite on the given surface."""
        surface.blit(self.image, self.rect)
