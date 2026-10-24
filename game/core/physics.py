"""Gravity-aware vertical physics.

Single Responsibility: PhysicsBody tracks vertical velocity, applies
gravity, and knows whether its owner is grounded.  Horizontal motion
belongs to whoever owns the body — it's an input, not a physical state.

Composed into Character (not inherited) so that different entities can
share the behaviour without being locked into a single inheritance chain.
"""


class PhysicsBody:
    """One frame of vertical motion = one call to :meth:`tick`."""

    def __init__(self, gravity: float, jump_force: float) -> None:
        self._gravity = gravity
        self._jump_force = jump_force
        self._velocity_y = 0.0
        self._is_grounded = True

    @property
    def velocity_y(self) -> float:
        return self._velocity_y

    @property
    def is_grounded(self) -> bool:
        return self._is_grounded

    def jump(self) -> bool:
        """Trigger a jump if currently grounded.  Returns True on success."""
        if not self._is_grounded:
            return False
        self._velocity_y = self._jump_force
        self._is_grounded = False
        return True

    def tick(self) -> int:
        """Advance one frame.  Returns the integer dy to apply to a rect."""
        if self._is_grounded:
            return 0
        self._velocity_y += self._gravity
        return round(self._velocity_y)

    def land(self) -> None:
        """Called by the owner when it touches the ground this frame."""
        self._velocity_y = 0.0
        self._is_grounded = True
