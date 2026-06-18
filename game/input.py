
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
import pygame
class Commands:
    """Normalised command object returned by read_commands().

    Attributes:
        move_left: True if the player is currently holding the left movement key.
        move_right: True if the player is currently holding the right movement key.
        jump: True if the player has just pressed the jump key this frame.
        attack: True if the player has just pressed the attack key this frame.
        pause: True if the player has just pressed the pause key this frame.
    """
    def __init__(self, move_left=False, move_right=False, jump=False, attack=False, pause=False):
        self.move_left = move_left
        self.move_right = move_right
        self.jump = jump
        self.attack = attack
        self.pause = pause
    
def read_commands(events) -> Commands:
    """Reads the current input state and returns a Commands object."""

    # if key stroke is pressed, jump or attack]
    keys = pygame.key.get_pressed()
    cmds = Commands(
        move_left=keys[pygame.K_LEFT] or keys[pygame.K_a],
        move_right=keys[pygame.K_RIGHT] or keys[pygame.K_d],
    )

    # One-frame actions
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cmds.jump = True
            elif event.key == pygame.K_f:
                cmds.attack = True
            elif event.key == pygame.K_ESCAPE:
                cmds.pause = True

    return cmds
    

    

