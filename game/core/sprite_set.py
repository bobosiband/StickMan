"""Sprite loading, scaling, and caching.

Single Responsibility: SpriteSet exists only to turn a dict of
state-name → image-path into cached pygame Surfaces at the right size,
pre-computed for both facing directions.
"""
from pathlib import Path

import pygame


class SpriteSet:
    """A named collection of sprites, scaled to a uniform height."""

    def __init__(self, paths: dict[str, Path], target_height: int) -> None:
        self._right: dict[str, pygame.Surface] = {}
        self._left: dict[str, pygame.Surface] = {}

        for name, path in paths.items():
            raw = pygame.image.load(path).convert_alpha()
            scale = target_height / raw.get_height()
            size = (round(raw.get_width() * scale), target_height)
            scaled = pygame.transform.scale(raw, size)
            self._right[name] = scaled
            self._left[name] = pygame.transform.flip(scaled, True, False)

    def get(self, name: str, flipped: bool = False) -> pygame.Surface:
        """Return the sprite for `name`, mirrored horizontally if flipped."""
        return (self._left if flipped else self._right)[name]

    def names(self) -> list[str]:
        return list(self._right.keys())
