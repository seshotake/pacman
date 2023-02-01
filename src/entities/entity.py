import pygame
from pacman.settings import HEIGHT, WIDTH

from entities.wall import Wall


class Entity(pygame.sprite.Sprite):
    """Represent an absract entity that can move"""

    rect: pygame.rect.Rect
    image: pygame.surface.Surface

    def __init__(self, *groups, **kwargs) -> None:
        super().__init__(*groups)

        self.type = kwargs.get("type", "entity")

        self.obstacle_sprites = kwargs.get(
            "obstacle_sprites", pygame.sprite.Group())

        self.image = pygame.image.load(kwargs.get(
            "image", "assets/images/player.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=kwargs.get("position", (0, 0)))

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = kwargs.get("speed", 1)
        self.health = self.max_health = kwargs.get("max_health", 1)

        self.damage = kwargs.get("damage", 0)

    def update(self) -> None:
        """Update the entity"""

        self.move()

    def move(self) -> None:

        self.normalize_direction(self.direction)

        self.rect.x += int(self.direction.x * self.speed)
        self.collide(self.direction.x, 0)
        self.rect.y += int(self.direction.y * self.speed)
        self.collide(0, self.direction.y)

    def collide(self, xvel: float, yvel: float) -> None:
        """Check collision with other sprites"""

        self.collide_walls(xvel, yvel, walls=self.obstacle_sprites)
        self.collide_outside()

    def collide_walls(self, xvel: float, yvel: float, walls: pygame.sprite.Group) -> None:
        """Check collision with walls"""

        for wall in walls:
            if isinstance(wall, Wall):
                if self.rect.colliderect(wall.hitbox):
                    self.swap_position(xvel, yvel, self.rect, wall.hitbox)

    def collide_outside(self) -> None:
        """Check collision with the outside of the screen"""

        if self.rect.top > HEIGHT:
            self.rect.top = 0
        if self.rect.bottom < 0:
            self.rect.bottom = HEIGHT
        if self.rect.left > WIDTH:
            self.rect.left = 0
        if self.rect.right < 0:
            self.rect.right = WIDTH

    @staticmethod
    def normalize_direction(direction: pygame.math.Vector2) -> None:
        """Normalize the direction vector"""

        if direction.magnitude() != 0:
            direction = direction.normalize()

    @staticmethod
    def swap_position(xvel: float, yvel: float,
                      rect: pygame.rect.Rect, hitbox: pygame.rect.Rect) -> None:
        """Swap the position of the player with the hitbox of other sprite"""

        if xvel > 0:
            rect.right = hitbox.left
        if xvel < 0:
            rect.left = hitbox.right
        if yvel > 0:
            rect.bottom = hitbox.top
        if yvel < 0:
            rect.top = hitbox.bottom
