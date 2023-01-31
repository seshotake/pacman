import pygame
from pacman.settings import HEIGHT, WIDTH


class Player(pygame.sprite.Sprite):
    rect: pygame.rect.Rect

    def __init__(self, position, obstacle_sprites, *groups) -> None:
        super().__init__(*groups)

        self.image = pygame.image.load(
            "assets/images/player.png").convert_alpha()

        self.start_position = position
        self.rect = self.image.get_rect(topleft=position)

        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2(0, 0)

        self.speed = 5
        self.health = self.max_health = 3

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self) -> None:
        self.input()
        self.move()

    def move(self) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += int(self.direction.x * self.speed)
        self.collide(self.direction.x, 0, walls=self.obstacle_sprites)
        self.rect.y += int(self.direction.y * self.speed)
        self.collide(0, self.direction.y, walls=self.obstacle_sprites)

        if self.rect.top > HEIGHT:
            self.rect.top = 0
        if self.rect.top < 0:
            self.rect.top = HEIGHT

        if self.rect.left > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = WIDTH

    def collide(self, xvel, yvel, walls) -> None:
        for wall in walls:
            if self.rect.colliderect(wall.hitbox):
                if xvel > 0:
                    self.rect.right = wall.hitbox.left
                if xvel < 0:
                    self.rect.left = wall.hitbox.right
                if yvel > 0:
                    self.rect.bottom = wall.hitbox.top
                if yvel < 0:
                    self.rect.top = wall.hitbox.bottom