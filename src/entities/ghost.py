import pygame

from entities.entity import Entity
from entities.wall import Wall


def get_player(groups: list[pygame.sprite.AbstractGroup]) -> Entity | None:
    """Get the player from the groups"""

    for group in groups:
        for sprite in group:
            if isinstance(sprite, Entity) and sprite.type == "player":
                return sprite
    return None


class Ghost(Entity):
    """Represent the ghost that hostiles the player."""

    def __init__(self, position, obstacle_sprites, id: int, *groups) -> None:
        super().__init__(*groups, type="enemy", position=position,
                         obstacle_sprites=obstacle_sprites, speed=id+1,
                         max_health=id, image=f"assets/images/ghost{id}.png")

        self.hitbox = self.rect.inflate(-5, -5)
        self.player = get_player(self.groups())
        self.damage = id

    def collide_walls(self, xvel: float, yvel: float, walls: list[Wall]) -> None:
        """Check if the ghost collide with walls"""

        for wall in walls:
            if self.hitbox.colliderect(wall.hitbox):
                self.swap_position(xvel, yvel, self.hitbox, wall.hitbox)

    def get_player_direction(self,
                             player: Entity | None) -> pygame.math.Vector2:
        """Get the direction of the player"""

        if player is None:
            self.player = get_player(self.groups())
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

        self.direction = self.get_player_direction(self.player)
        return super().update()
