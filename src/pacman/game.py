import sys

import pygame

from pacman.debug import debug
from pacman.level import Level
from pacman.settings import FPS, HEIGHT, TITLE, WIDTH


class Game:
    """Represents the pacman game."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.level = Level()

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
        debug(f"FPS: {self.clock.get_fps():.2f}")
        debug(f"Level: {self.level.level_number}", (10, 40))
        debug(f"Position: {self.level.player.rect.topleft}", (10, 80))
        debug(f"Health: {self.level.player.health}", (10, 120))

    def update(self) -> None:
        """Update the game."""

        # update sprites
        self.level.update()
        pygame.display.update()
        self.clock.tick(FPS)
