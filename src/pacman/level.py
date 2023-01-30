import pygame
from entities.player import Player

from entities.wall import Wall

from pacman.settings import BLOCK_SIZE

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.level_number = 1

        self.generate_level()

    def generate_level(self) -> None:
        level = self.load_level()

        for row, tiles in enumerate(level):
            for col, tile in enumerate(tiles):
                if tile == "=":
                    Wall((col * BLOCK_SIZE, row * BLOCK_SIZE),
                         [self.visible_sprites, self.obstacle_sprites])
                if tile == "P":
                    self.player = Player(
                        (col * BLOCK_SIZE, row * BLOCK_SIZE), self.obstacle_sprites,
                        [self.visible_sprites])

    def load_level(self) -> list[str]:
        filename = f"assets/levels/level_{self.level_number}.txt"
        with open(filename, "r") as file:
            return file.read().splitlines()

    def draw(self) -> None:
        self.visible_sprites.draw(self.display_surface)

    def update(self) -> None:
        self.visible_sprites.update()