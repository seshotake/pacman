import pygame


class Wall(pygame.sprite.Sprite):
    """Represent the wall that blocks the moving of the sprites."""

    def __init__(self, position, *groups) -> None:
        super().__init__(*groups)

        self.image = pygame.image.load(
            "assets/images/wall.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-4, -4)
