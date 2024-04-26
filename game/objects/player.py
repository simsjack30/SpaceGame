import pygame
from objects.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, bullets_group):
        super().__init__()
        self.original_image = pygame.image.load("assets/player.png")
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 7
        self.max_health = 500
        self.health = self.max_health
        self.health_bar_length = 200
        self.health_bar_height = 20
        self.bullets_group = bullets_group
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.camera_offset = pygame.math.Vector2(0, 0)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.xy = 0, 0
        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1

    def update(self):
        self.input()
        self.process_input()
        self.rect.center += self.direction * self.speed
        self.flip_sprite()
        self.rect.clamp_ip(pygame.Rect(0, 0, 2280, 1720))

    def flip_sprite(self):
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.direction.x > 0:
            self.image = self.original_image

    def draw_health_bar(self, screen):
        health_ratio = self.health / self.max_health
        current_health_length = self.health_bar_length * health_ratio
        
        background_rect = pygame.Rect(10, 10, self.health_bar_length, self.health_bar_height)
        pygame.draw.rect(screen, (255,0,0), background_rect)
        
        health_rect = pygame.Rect(10, 10, current_health_length, self.health_bar_height)
        pygame.draw.rect(screen, (0,255,0), health_rect)

    def take_damage(self, amount):
        self.health -= amount

    def process_input(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = current_time

    def update_camera_offset(self, offset):
        self.camera_offset = pygame.math.Vector2(offset)

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_mouse_x = mouse_x + self.camera_offset.x
        world_mouse_y = mouse_y + self.camera_offset.y
        direction = pygame.math.Vector2(world_mouse_x - self.rect.centerx, world_mouse_y - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize()
        bullet = Bullet(self.rect.center, direction)
        self.bullets_group.add(bullet)