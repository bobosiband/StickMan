"""Game: owns the window, the main loop, and the entity registry.

Depends only on the abstract :class:`Updatable` / :class:`Drawable`
interfaces and on :class:`InputReader` — never on concrete entities or
pygame input primitives — so new entity types plug in without touching
the loop (Open/Closed, Dependency Inversion).
"""
import pygame

from game.config import COLOUR_BG, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from game.core.interfaces import Drawable, Updatable
from game.entities.player import Player
from game.input import InputReader, KeyboardInputReader
from game.logger import get_logger

logger = get_logger()


class Game:
    """Top-level game object; create one and call :meth:`run`."""

    def __init__(self) -> None:
        pygame.init()
        self._screen: pygame.Surface = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption(TITLE)

        self._clock = pygame.time.Clock()
        self._running = False

        self._input_reader: InputReader = KeyboardInputReader()
        self._player = Player(
            self._input_reader,
            start_pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT),
        )

        self._updatables: list[Updatable] = [self._player]
        self._drawables: list[Drawable] = [self._player]

        logger.info(
            "Game initialised — window %dx%d @ %d FPS",
            SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
        )

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Block until the user quits."""
        logger.info("Game started")
        self._running = True
        while self._running:
            self._tick()
        self._shutdown()

    def _tick(self) -> None:
        events = pygame.event.get()
        self._handle_system_events(events)
        self._input_reader.poll(events)
        for entity in self._updatables:
            entity.update()
        self._draw()
        self._clock.tick(FPS)

    # ------------------------------------------------------------------
    # Per-frame helpers
    # ------------------------------------------------------------------
    def _handle_system_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False

    def _draw(self) -> None:
        self._screen.fill(COLOUR_BG)
        for drawable in self._drawables:
            drawable.draw(self._screen)
        pygame.display.flip()

    # ------------------------------------------------------------------
    # Clean-up
    # ------------------------------------------------------------------
    def _shutdown(self) -> None:
        logger.info("Window closed — goodbye!")
        pygame.quit()
