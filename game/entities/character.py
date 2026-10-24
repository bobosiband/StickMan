"""Character: an Entity that moves, has sprites, and feels gravity.

Still abstract — concrete behaviour (how it decides to move, how it
picks a sprite, how it dies) is left to subclasses like Player and the
future Enemy classes.

Favours composition over inheritance for its sub-components:
  * SpriteSet — rendering concern
  * PhysicsBody — motion concern

...so a Character isn't locked into any particular rendering or physics
implementation (Dependency Inversion).
"""
from abc import ABC

import pygame

from game import config
from game.core.physics import PhysicsBody
from game.core.sprite_set import SpriteSet
from game.entities.entity import Entity


class Character(Entity, ABC):
    """A sprite-driven, gravity-affected actor."""

    def __init__(
        self,
        sprite_set: SpriteSet,
        physics: PhysicsBody,
        speed: int,
        start_pos: tuple[int, int],
        initial_sprite_name: str,
    ) -> None:
        reference = sprite_set.get(initial_sprite_name)
        super().__init__(start_pos, (reference.get_width(), reference.get_height()))

        self._sprite_set = sprite_set
        self._physics = physics
        self._speed = speed
        self._facing_left = False
        self._image: pygame.Surface = reference

    # ------------------------------------------------------------------
    # Read-only accessors for state classes and the game loop
    # ------------------------------------------------------------------
    @property
    def physics(self) -> PhysicsBody:
        return self._physics

    @property
    def facing_left(self) -> bool:
        return self._facing_left

    @property
    def speed(self) -> int:
        return self._speed

    # ------------------------------------------------------------------
    # Shared motion primitives (used by state classes)
    # ------------------------------------------------------------------
    def walk(self, direction: int) -> None:
        """Move one step at walking speed; direction is -1 (left) or +1 (right)."""
        if direction < 0:
            self._facing_left = True
        elif direction > 0:
            self._facing_left = False
        self._rect.x += direction * self._speed

    def lunge(self, dx: int) -> None:
        """Horizontal displacement that bypasses walking speed (e.g. attack lunge)."""
        self._rect.x += dx

    # ------------------------------------------------------------------
    # Default rendering + ground / bounds handling
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._image, self._rect)

    def _refresh_sprite(self, state_name: str) -> None:
        """Swap the active sprite without moving the character's feet."""
        new_image = self._sprite_set.get(state_name, flipped=self._facing_left)
        if new_image is self._image:
            return
        bottom_center = self._rect.midbottom
        self._image = new_image
        self._rect = self._image.get_rect()
        self._rect.midbottom = bottom_center

    def _apply_gravity(self) -> None:
        self._rect.y += self._physics.tick()
        if self._rect.bottom >= config.SCREEN_HEIGHT:
            self._rect.bottom = config.SCREEN_HEIGHT
            self._physics.land()

    def _clamp_horizontally(self) -> None:
        self._rect.x = max(0, min(self._rect.x, config.SCREEN_WIDTH - self._rect.width))
