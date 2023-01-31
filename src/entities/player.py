import pygame
from entities.wall import Wall
from pacman.settings import HEIGHT, MAX_HEALTH, WIDTH, PLAYER_SPEED, IMMUNITY_TIME


class Player(pygame.sprite.Sprite):
    """Represent the player that can move"""

    rect: pygame.rect.Rect
    image: pygame.surface.Surface

    def __init__(self, position, obstacle_sprites, *groups) -> None:
        super().__init__(*groups)

        self.image = pygame.image.load(
            "assets/images/player.png").convert_alpha()

        self.start_position = position
        self.rect = self.image.get_rect(topleft=position)
        self.enemies = [enemy for enemy in obstacle_sprites
                        if hasattr(enemy, "enemy_update")]

        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2(0, 0)

        self.speed = PLAYER_SPEED
        self.health = self.max_health = MAX_HEALTH

        self.immune = False
        self.start_time_immunity = 0
        self.time_immune = self.start_time_immunity + IMMUNITY_TIME

    @staticmethod
    def normalize_direction(direction):
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

    def move(self) -> None:
        """Move the player"""

        self.normalize_direction(self.direction)

        self.rect.x += int(self.direction.x * self.speed)
        self.collide_walls(self.direction.x, 0, walls=self.obstacle_sprites)
        self.rect.y += int(self.direction.y * self.speed)
        self.collide_walls(0, self.direction.y, walls=self.obstacle_sprites)

    def check_oustide(self):
        """Check if the player is outside the screen"""

        if self.rect.top > HEIGHT:
            self.rect.top = 0
        if self.rect.top < 0:
            self.rect.top = HEIGHT

        if self.rect.left > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = WIDTH

    def collide_walls(self, xvel: float, yvel: float, walls: list[Wall]) -> None:
        """Check if the player collides with a wall"""

        for wall in walls:
            if self.rect.colliderect(wall.hitbox):
                self.swap_position(xvel, yvel, self.rect, wall.hitbox)

        self.check_oustide()

    def collide_enemy(self, enemy) -> None:
        """Check if the player collides with an enemy"""

        if self.immune:
            return

        if self.rect.colliderect(enemy.rect):
            self.health -= enemy.damage
            self.give_immunity(IMMUNITY_TIME)

    def give_health(self, health) -> None:
        """Give the player health"""

        self.health += health

        if self.health > self.max_health:
            self.health = self.max_health

    def give_immunity(self, time) -> None:
        """Give the player immunity"""

        self.immune = True
        self.speed = PLAYER_SPEED + 2
        self.start_time_immunity = pygame.time.get_ticks()
        self.time_immune = self.start_time_immunity + time

    def update_immunity(self) -> None:
        """Update the immunity of the player"""

        if self.immune:
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)

        self.reset_immunity()

    def reset_immunity(self) -> None:
        """Reset the immunity of the player"""

        if self.time_immune <= pygame.time.get_ticks():
            self.immune = False
            self.speed = PLAYER_SPEED
