import pygame
import sys

from settings import TITLE, WIDTH, HEIGHT, FPS
from debug import debug


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        """Game loop."""

        while True:
            self.handle_events()
            self.clear_screen()
            self.draw()
            self.update()

    def handle_events(self) -> None:
        """Game loop - events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def clear_screen(self) -> None:
        """Clear the screen."""

        self.screen.fill('black')

    def draw(self) -> None:
        """Game loop - draw."""

        # draw sprites
        debug(f"FPS: {self.clock.get_fps():.2f}")

    def update(self) -> None:
        """Game loop - update."""

        # update sprites
        pygame.display.update()
        self.clock.tick(FPS)
