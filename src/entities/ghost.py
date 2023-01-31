import random

import pygame

from entities.player import Player


class Ghost(Player):
    def __init__(self, position, obstacle_sprites, *groups) -> None:
        super().__init__(position, obstacle_sprites, *groups)

        self.image = pygame.image.load(
            "assets/images/ghost.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

        self.obstacle_sprites = obstacle_sprites

        self.direction = pygame.math.Vector2(random.randint(
            -1, 1), random.randint(-1, 1))

        self.speed = 2
        self.health = self.max_health = 1

    def get_player_direction(self, player: Player) -> pygame.math.Vector2:
        enemy_center = pygame.math.Vector2(self.rect.center)
        player_center = pygame.math.Vector2(player.rect.center)
        distance = (player_center - enemy_center).magnitude()

        if distance > 0:
            direction = (player_center - enemy_center).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)
        return direction

    def update(self) -> None:
        self.move()

    def enemy_update(self, player: Player) -> None:
        self.direction = self.get_player_direction(player)
        self.collide_with_player(player)

    def collide_with_player(self, player: Player) -> None:
        if self.rect.colliderect(player.rect):
            player.health -= 1
            player.rect.topleft = player.start_position