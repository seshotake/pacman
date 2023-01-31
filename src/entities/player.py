import pygame
from pacman.settings import IMMUNITY_TIME, MAX_HEALTH, PLAYER_SPEED

from entities.entity import Entity, get_enemies


class Player(Entity):
    """Represents the player"""

    def __init__(self, obstacle_sprites, *groups) -> None:
        super().__init__(*groups, type="player", obstacle_sprites=obstacle_sprites,
                         speed=PLAYER_SPEED, max_health=MAX_HEALTH)

        self.enemies = get_enemies(self.groups())

        self.immune = False
        self.start_time_immunity = 0
        self.time_immunity = IMMUNITY_TIME

    def set_position(self, position) -> None:
        """Set the position of the player"""

        self.rect.topleft = position

    def input(self) -> None:
        """Get the input of the player"""

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
        """Update the player"""

        self.input()
        self.move()
        self.update_immunity()

    def collide(self, xvel: float, yvel: float) -> None:
        """Check if the player collide with other sprites"""

        self.collide_enemies()
        return super().collide(xvel, yvel)

    def collide_enemies(self) -> None:
        """Check if the player collide with an enemy"""

        for enemy in self.enemies:

            if self.immune:
                return

            if self.rect.colliderect(enemy.rect):
                self.get_damage(enemy.damage)
                self.get_immunity(pygame.time.get_ticks())

    def get_damage(self, damage_value: int) -> None:
        """Get damage from an enemy"""

        if self.health > 0:
            self.health -= damage_value

    def get_health(self, health_value: int = 1) -> None:
        """Get health"""

        if self.health < self.max_health:
            self.health += health_value

    def get_immunity(self, start_time) -> None:
        """Get immunity"""

        self.immune = True
        self.start_time_immunity = start_time
        self.time_immunity = self.start_time_immunity + IMMUNITY_TIME

    def update_immunity(self) -> None:
        """Update the immunity"""

        if self.immune:
            self.image.set_alpha(128)
            if pygame.time.get_ticks() >= self.time_immunity:
                self.reset_immunity()
        else:
            self.image.set_alpha(255)

    def reset_immunity(self) -> None:
        """Reset the immunity"""

        self.immune = False
        self.start_time_immunity = 0
        self.time_immunity = IMMUNITY_TIME
