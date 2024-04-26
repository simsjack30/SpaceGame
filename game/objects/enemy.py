import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, player, group):
        super().__init__(group)
        self.image = pygame.image.load("assets/enemy_one.png")
        self.rect = self.image.get_rect(center=pos)
        self.player = player
        self.speed = 5
        self.health = 20

    def update(self):
        self.follow_player()

    def follow_player(self):
        direction = self.player.rect.center - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
        self.rect.center += direction * self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

class LungeEnemy(Enemy): 
    def __init__(self, pos, player, group):
        super().__init__(pos, player, group)
        self.image = pygame.image.load("assets/enemy_two.png")
        self.rect = self.image.get_rect(center=pos)
        self.lunge_speed = 12
        self.normal_speed = 0
        self.lunging = False
        self.lunge_timer = 0
        self.lunge_cooldown = 100

    def update(self):
        if self.lunge_timer <= 0:
            self.lunging = True
            self.lunge_timer = self.lunge_cooldown
        else:
            self.lunge_timer -= 1
            self.speed = self.lunge_speed if self.lunging else self.normal_speed
            super().follow_player()

        if self.lunging and self.lunge_timer <= self.lunge_cooldown - 30:
            self.lunging = False

class WanderEnemy(Enemy):
    def __init__(self, pos, player, group):
        super().__init__(pos, player, group)
        self.image = pygame.image.load("assets/enemy_three.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.wander_speed = 4
        self.follow_speed = 8
        self.follow_radius = 400
        self.world_bounds = pygame.Rect(0, 0, 2280, 1720)
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def update(self):
        if not self.world_bounds.contains(self.rect):
            self.return_to_play_area()
        else:
            distance = self.player.rect.center - pygame.math.Vector2(self.rect.center)
            if distance.length_squared() < self.follow_radius**2:
                self.follow_player()
            else:
                self.wander()

    def wander(self):
        if random.randint(0, 40) == 0:
            self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if self.direction.length() > 0:
                self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.wander_speed 

    def return_to_play_area(self):
        direction_to_player = pygame.math.Vector2(self.player.rect.center) - self.rect.center
        if direction_to_player.length() > 0:
            self.direction = direction_to_player.normalize()
        self.rect.center += self.direction * self.follow_speed

    def follow_player(self):
        direction_to_player = pygame.math.Vector2(self.player.rect.center) - self.rect.center
        if direction_to_player.length() > 0:
            self.direction = direction_to_player.normalize()
        self.rect.center += self.direction * self.follow_speed
