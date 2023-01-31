import random

import pygame

from entities.player import Player


class Ghost(Player):
    """Represent the ghost that hostiles the player."""

    def __init__(self, position, obstacle_sprites, *groups) -> None:
        super().__init__(position, obstacle_sprites, *groups)

        # load random ghost image
        ghost_id = random.randint(1, 3)
        ghost_filename = f"assets/images/ghost{ghost_id}.png"

        self.image = pygame.image.load(ghost_filename).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-5, -5)

        self.obstacle_sprites = obstacle_sprites

        self.direction = pygame.math.Vector2()

        self.speed = ghost_id + 1
        self.damage = ghost_id
        self.health = self.max_health = ghost_id

    def get_player_direction(self, player: Player) -> pygame.math.Vector2:
        """Get the direction of the player"""

        enemy_center = pygame.math.Vector2(self.rect.center)
        player_center = pygame.math.Vector2(player.rect.center)
        distance = (player_center - enemy_center).magnitude()

        if distance > 0:
            direction = (player_center - enemy_center).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)
        return direction

    def update(self) -> None:
        """Update the ghost"""

        self.move()

    def enemy_update(self, player: Player) -> None:
        """Update the ghost depending on the player"""

        self.direction = self.get_player_direction(player)
        player.collide_enemy(self)

    def collide_walls(self, xvel, yvel, walls) -> None:
        """Check if the ghost collide with walls"""

        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                self.swap_position(xvel, yvel, self.hitbox, wall.hitbox)

