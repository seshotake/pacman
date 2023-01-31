import pygame

import random

from entities.ghost import Ghost
from entities.player import Player
from entities.wall import Wall

from pacman.settings import BLOCK_SIZE


class Level:
    """Represents a level."""

    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player(self.obstacle_sprites, [self.visible_sprites])

        self.level_number = 1

        self.generate_level()

    def generate_level(self) -> None:
        """Generate the level."""

        level = self.load_level()

        for row, tiles in enumerate(level):
            for col, tile in enumerate(tiles):
                if tile == "=":
                    Wall((col * BLOCK_SIZE, row * BLOCK_SIZE),
                         [self.visible_sprites, self.obstacle_sprites])
                if tile == "P":
                    self.player.set_position((col * BLOCK_SIZE, row * BLOCK_SIZE))
                if tile == "G":
                    Ghost((col * BLOCK_SIZE, row * BLOCK_SIZE),
                          self.obstacle_sprites,
                          random.randint(1, 3), [self.visible_sprites, self.enemies])

    def load_level(self) -> list[str]:
        """Load the level from a file."""

        filename = f"assets/levels/level_{self.level_number}.txt"
        with open(filename, "r") as file:
            return file.read().splitlines()

    def draw(self) -> None:
        """Draw the level."""

        self.visible_sprites.draw(self.display_surface)

    def update(self) -> None:
        """Update the level."""

        self.visible_sprites.update()
