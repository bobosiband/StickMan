"""TODO: Input handler — translates raw key / gamepad state into game commands.

This module will be called once per frame (inside Game.update()) and will
return a normalised command object so that entity logic never talks to
pygame's keyboard API directly.

Planned interface example:

    from game.input import read_commands, Commands

    def update(self) -> None:
        cmds = read_commands()
        if cmds.move_left:
            self.player.move(-1)
        if cmds.attack:
            self.player.attack()

Planned commands to support:
    move_left  — held: walk left
    move_right — held: walk right
    jump       — on key-down: jump
    attack     — on key-down: melee strike
    pause      — on key-down: open/close pause menu
"""
