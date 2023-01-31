import pygame

from entities.entity import Entity, get_player
from entities.wall import Wall


class Ghost(Entity):
    """Represent the ghost that hostiles the player."""

    def __init__(self, position, obstacle_sprites, id: int, *groups) -> None:
        super().__init__(*groups, type="enemy", position=position,
                         obstacle_sprites=obstacle_sprites, speed=id+1,
                         max_health=id, image=f"assets/images/ghost{id}.png")

        self.hitbox = self.rect.inflate(-5, -5)
        self.damage = id


    def collide_walls(self, xvel: float, yvel: float, walls: list[Wall]) -> None:
        """Check if the ghost collide with walls"""

        for wall in walls:
            if self.hitbox.colliderect(wall.hitbox):
                self.swap_position(xvel, yvel, self.hitbox, wall.hitbox)

    def get_player_direction(self, player: Entity) -> pygame.math.Vector2:
        """Get the direction of the player"""

        if not player:
            return pygame.math.Vector2(0, 0)

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

        player = get_player(self.groups())
        self.direction = self.get_player_direction(player)
        return super().update()
