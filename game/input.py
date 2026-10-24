"""Input abstraction.

Dependency Inversion Principle: entities depend on the abstract
:class:`InputReader`, not on pygame.  The concrete
:class:`KeyboardInputReader` is the only place pygame key codes appear,
so swapping in a replay reader or a gamepad reader won't touch any
gameplay code.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

import pygame


@dataclass
class Commands:
    """A normalised snapshot of what the player is asking for this frame."""

    move_left: bool = False
    move_right: bool = False
    jump: bool = False
    attack: bool = False
    pause: bool = False
    duck: bool = False


class InputReader(ABC):
    """Reads the current frame's input and exposes it as a Commands snapshot."""

    @abstractmethod
    def poll(self, events: list[pygame.event.Event]) -> None:
        """Consume this frame's events and refresh the internal snapshot."""

    @abstractmethod
    def get_commands(self) -> Commands:
        """Return the most recently polled commands."""


class KeyboardInputReader(InputReader):
    """Translates physical keyboard state into Commands."""

    _MOVE_LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
    _MOVE_RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)
    _DUCK_KEYS = (pygame.K_DOWN, pygame.K_s)
    _JUMP_KEYS = (pygame.K_SPACE,)
    _ATTACK_KEYS = (pygame.K_f,)
    _PAUSE_KEYS = (pygame.K_ESCAPE,)

    def __init__(self) -> None:
        self._commands = Commands()

    def poll(self, events: list[pygame.event.Event]) -> None:
        keys = pygame.key.get_pressed()
        snapshot = Commands(
            move_left=any(keys[k] for k in self._MOVE_LEFT_KEYS),
            move_right=any(keys[k] for k in self._MOVE_RIGHT_KEYS),
            duck=any(keys[k] for k in self._DUCK_KEYS),
        )
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in self._JUMP_KEYS:
                snapshot.jump = True
            elif event.key in self._ATTACK_KEYS:
                snapshot.attack = True
            elif event.key in self._PAUSE_KEYS:
                snapshot.pause = True
        self._commands = snapshot

    def get_commands(self) -> Commands:
        return self._commands
