"""Abstract capability interfaces.

Interface Segregation Principle: a class only implements the capabilities
it actually provides.  A particle system is Drawable but not Updatable;
a timer may be Updatable but not Drawable.  Entities implement both.
"""
from abc import ABC, abstractmethod

import pygame


class Drawable(ABC):
    """Anything that can render itself to a pygame Surface."""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Render this object onto the given surface."""


class Updatable(ABC):
    """Anything that advances its own state once per game tick."""

    @abstractmethod
    def update(self) -> None:
        """Advance this object by one frame."""
