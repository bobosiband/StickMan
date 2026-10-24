"""Generic finite state machine.

Open/Closed: adding a new state is a new class — the machine itself
never changes.  The machine knows nothing about what the states do;
it just owns the transition protocol.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.input import Commands
    from game.states.player_states import PlayerState


class StateMachine:
    """Owns the current state and routes update/transition calls."""

    def __init__(
        self,
        states: dict[str, "PlayerState"],
        initial: str,
        owner: object,
    ) -> None:
        self._states = states
        self._owner = owner
        self._current = self._states[initial]
        self._current.enter(owner)

    @property
    def current_name(self) -> str:
        return self._current.name

    def update(self, commands: "Commands") -> None:
        next_name = self._current.update(self._owner, commands)
        if next_name is not None and next_name != self._current.name:
            self._transition(next_name)

    def _transition(self, name: str) -> None:
        self._current.exit(self._owner)
        self._current = self._states[name]
        self._current.enter(self._owner)
