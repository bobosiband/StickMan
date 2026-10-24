"""Concrete player states (State pattern).

Each state is its own class and decides:
  * what the player can do this frame (behaviour)
  * which state to switch to next (transitions)

Adding a new behaviour (e.g. a block state) means adding one class —
no changes to Player or to any existing state (Open/Closed).

State ``name`` doubles as the key into :data:`config.STATE_PATHS` so the
sprite set resolves the right image automatically.
"""
from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from game import config

if TYPE_CHECKING:
    from game.entities.player import Player
    from game.input import Commands


class PlayerState(ABC):
    """Abstract base for every player behaviour state."""

    name: str = ""

    def enter(self, player: "Player") -> None:
        """Called once when the machine switches into this state."""

    def exit(self, player: "Player") -> None:
        """Called once when the machine switches out of this state."""

    @abstractmethod
    def update(self, player: "Player", commands: "Commands") -> Optional[str]:
        """Run this state's behaviour; return next state name or None."""


def _horizontal(commands: "Commands") -> int:
    return (1 if commands.move_right else 0) - (1 if commands.move_left else 0)


class _GroundedState(PlayerState):
    """Shared transitions available from any ground-based state."""

    def update(self, player: "Player", commands: "Commands") -> Optional[str]:
        if commands.attack:
            return random.choice([PunchingState.name, VodlozaState.name])
        if commands.jump and player.physics.jump():
            return JumpingState.name
        return None


class IdleState(_GroundedState):
    name = "idle"

    def update(self, player: "Player", commands: "Commands") -> Optional[str]:
        transition = super().update(player, commands)
        if transition is not None:
            return transition
        if commands.duck:
            return DuckingState.name
        direction = _horizontal(commands)
        if direction != 0:
            player.walk(direction)
            return WalkingState.name
        return None


class WalkingState(_GroundedState):
    name = "walking"

    def update(self, player: "Player", commands: "Commands") -> Optional[str]:
        transition = super().update(player, commands)
        if transition is not None:
            return transition
        if commands.duck:
            return DuckingState.name
        direction = _horizontal(commands)
        if direction == 0:
            return IdleState.name
        player.walk(direction)
        return None


class JumpingState(PlayerState):
    name = "jumping"

    def update(self, player: "Player", commands: "Commands") -> Optional[str]:
        if commands.attack:
            return random.choice([PunchingState.name, VodlozaState.name])
        direction = _horizontal(commands)
        if direction != 0:
            player.walk(direction)
        if player.physics.is_grounded:
            return IdleState.name
        return None


class DuckingState(PlayerState):
    name = "ducking"

    def update(self, player: "Player", commands: "Commands") -> Optional[str]:
        if not commands.duck:
            return IdleState.name
        return None


class _AttackState(PlayerState):
    """Base for timed melee attacks that lunge forward then end."""

    def enter(self, player: "Player") -> None:
        self._timer = config.PLAYER_ATTACK_DURATION

    def update(self, player: "Player", commands: "Commands") -> Optional[str]:
        self._timer -= 1
        if self._timer <= 0:
            return JumpingState.name if not player.physics.is_grounded else IdleState.name
        ratio = self._timer / config.PLAYER_ATTACK_DURATION
        step = max(1, round(player.attack_lunge_speed * ratio))
        direction = -1 if player.facing_left else 1
        player.lunge(direction * step)
        return None


class PunchingState(_AttackState):
    name = "punching"


class VodlozaState(_AttackState):
    name = "vodloza"


def default_player_states() -> dict[str, PlayerState]:
    """Build a fresh instance of every known player state, keyed by name."""
    classes = (
        IdleState,
        WalkingState,
        JumpingState,
        DuckingState,
        PunchingState,
        VodlozaState,
    )
    return {cls.name: cls() for cls in classes}
