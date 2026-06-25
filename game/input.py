import pygame
class Commands:
    """Normalised command object returned by read_commands().

    Attributes:
        move_left: True if the player is currently holding the left movement key.
        move_right: True if the player is currently holding the right movement key.
        jump: True if the player has just pressed the jump key this frame.
        attack: True if the player has just pressed the attack key this frame.
        pause: True if the player has just pressed the pause key this frame.
        duck: True if the player has just pressed the duck key this frame.
    """
    def __init__(self, move_left=False, move_right=False, jump=False, attack=False, pause=False, duck=False):
        self.move_left = move_left
        self.move_right = move_right
        self.jump = jump
        self.attack = attack
        self.pause = pause
        self.duck = duck  # Placeholder for ducking input, to be implemented later

def read_commands(events) -> Commands:
    """Reads the current input state and returns a Commands object."""

    # if key stroke is pressed, jump or attack]
    keys = pygame.key.get_pressed()
    cmds = Commands(
        move_left=keys[pygame.K_LEFT] or keys[pygame.K_a],
        move_right=keys[pygame.K_RIGHT] or keys[pygame.K_d],
        duck=keys[pygame.K_DOWN] or keys[pygame.K_s]
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
    

    

