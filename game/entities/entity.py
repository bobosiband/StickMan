"""Entity: abstract root of every on-screen actor.

Implements both :class:`Drawable` and :class:`Updatable` so the game
loop can hold a single ``list[Entity]`` and still iterate those
capabilities independently when it chooses to (ISP-friendly).
"""
from abc import abstractmethod

import pygame

from game.core.interfaces import Drawable, Updatable


class Entity(Drawable, Updatable):
    """A positioned actor with a bounding rect.  Abstract."""

    def __init__(self, start_pos: tuple[int, int], size: tuple[int, int]) -> None:
        self._rect = pygame.Rect(0, 0, *size)
        self._rect.midbottom = start_pos

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def position(self) -> tuple[int, int]:
        return self._rect.midbottom

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...
