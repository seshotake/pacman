import pygame

from entities.player import Player


class UI:
    def __init__(self, player: Player) -> None:
        self.display_surface = pygame.display.get_surface()
        self.heart_image = pygame.image.load("assets/images/full_heart.png")
        self.empty_heart_image = pygame.image.load(
            "assets/images/empty_heart.png")

        self.player = player

    def display(self) -> None:
        self.show_health(self.player)

    def show_health(self, player: Player) -> None:
        for heart in range(player.max_health):
            if heart < player.health:
                self.display_surface.blit(self.heart_image, (heart * 32, 0))
            else:
                self.display_surface.blit(
                    self.empty_heart_image, (heart * 32, 0))
