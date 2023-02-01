import sys

import pygame

from pacman.level import Level
from pacman.settings import FPS, HEIGHT, TITLE, WIDTH
from pacman.ui import UI


class Game:
    """Represents the pacman game."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.player = self.level.player
        self.ui = UI(self.player)

    def run(self) -> None:
        """Run the game."""

        while True:
            self.handle_events()
            self.clear_screen()
            self.draw()
            self.update()

    def handle_events(self) -> None:
        """Handle events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def clear_screen(self) -> None:
        """Clear the screen."""

        self.screen.fill('black')

    def draw(self) -> None:
        """Draw the game."""

        # draw sprites
        self.level.draw()
        self.ui.display()

    def update(self) -> None:
        """Update the game."""

        # update sprites
        self.level.update()
        pygame.display.update()
        self.clock.tick(FPS)
