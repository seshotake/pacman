import random

import pygame

import re

from entities.player import Player


class Ghost(Player):
    def __init__(self, position, obstacle_sprites, *groups) -> None:
        super().__init__(position, obstacle_sprites, *groups)

        # load random ghost image
        ghost_id = random.randint(1, 3)

        self.image = pygame.image.load(
            f"assets/images/ghost{ghost_id}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-5, -5)

        self.obstacle_sprites = obstacle_sprites

        self.direction = pygame.math.Vector2()

        self.speed = ghost_id + 1
        self.damage = ghost_id
        self.health = self.max_health = ghost_id

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
        player.collide_enemy(self)

    def collide(self, xvel, yvel, walls) -> None:
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                self.swap_position(xvel, yvel, self.hitbox, wall)
