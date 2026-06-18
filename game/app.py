"""Game class: owns the pygame window, clock, and the main loop.

All per-frame coordination (events → update → draw) happens here.
Feature-specific logic (input, AI, collisions, scoring) will be
called from update() once those systems are implemented.
"""
import pygame

from game.config import COLOUR_BG, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from game.entities import player
from game.entities.player import Player
from game.input import read_commands
from game.logger import get_logger

logger = get_logger()


class Game:
    """Top-level game object.

    Owns the pygame display and drives the main loop.  Create one
    instance and call run() to start the game.

    Attributes:
        screen:  The pygame display surface.
        clock:   Regulates the frame rate.
        running: Set to False to break out of the main loop cleanly.
        player:  The player entity.
    """

    def __init__(self) -> None:
        pygame.init()

        self.screen: pygame.Surface = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption(TITLE)

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = False
        self.player: Player = Player()

        logger.info(
            "Game initialised — window %dx%d @ %d FPS", SCREEN_WIDTH, SCREEN_HEIGHT, FPS
        )

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the main game loop and block until the user quits."""
        logger.info("Game started")
        self.running = True

        while self.running:
            self._handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        self._shutdown()

    # ------------------------------------------------------------------
    # Per-frame methods (called in order every frame)
    # ------------------------------------------------------------------

    def _handle_events(self) -> None:
        """Process all pygame events queued since the last frame."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        commands = read_commands(events)
        self.player.update(commands)

    def update(self) -> None:
        """Update all game objects for this frame.

        Per-frame logic will be routed through here as it is implemented:
        reading player input, running enemy AI, applying physics,
        testing collisions, and updating the score.
        """
        pass

    def draw(self) -> None:
        """Clear the screen, draw every visible object, then flip the buffer."""
        self.screen.fill(COLOUR_BG)
        self.player.draw(self.screen)
        pygame.display.flip()

    # ------------------------------------------------------------------
    # Clean-up
    # ------------------------------------------------------------------

    def _shutdown(self) -> None:
        """Release pygame resources and exit."""
        logger.info("Window closed — goodbye!")
        pygame.quit()
