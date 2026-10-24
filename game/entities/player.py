"""Player: a Character driven by an InputReader and a StateMachine."""
from game import config
from game.core.physics import PhysicsBody
from game.core.sprite_set import SpriteSet
from game.entities.character import Character
from game.input import InputReader
from game.logger import get_logger
from game.states.player_states import IdleState, default_player_states
from game.states.state_machine import StateMachine

logger = get_logger()


class Player(Character):
    """The user-controlled stickman."""

    def __init__(self, input_reader: InputReader, start_pos: tuple[int, int]) -> None:
        sprite_set = SpriteSet(config.STATE_PATHS, config.PLAYER_HEIGHT)
        physics = PhysicsBody(gravity=config.GRAVITY, jump_force=config.PLAYER_JUMP_FORCE)
        super().__init__(
            sprite_set=sprite_set,
            physics=physics,
            speed=config.PLAYER_SPEED,
            start_pos=start_pos,
            initial_sprite_name=IdleState.name,
        )

        self._input_reader = input_reader
        self.attack_lunge_speed = 8
        self._state_machine = StateMachine(
            default_player_states(), initial=IdleState.name, owner=self
        )

        logger.info(
            "Player ready at %s (sprites: %s)",
            self._rect.midbottom,
            sprite_set.names(),
        )

    @property
    def state_name(self) -> str:
        return self._state_machine.current_name

    def update(self) -> None:
        commands = self._input_reader.get_commands()
        self._state_machine.update(commands)
        self._refresh_sprite(self._state_machine.current_name)
        self._apply_gravity()
        self._clamp_horizontally()
