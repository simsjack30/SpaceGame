import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.image.load("assets/bullet.png")
        self.rect = self.image.get_rect(center=pos)
        self.speed = 10
        self.damage = 10
        self.velocity = direction * self.speed

    def update(self):
        self.rect.center += self.velocity
        if not pygame.Rect(0, 0, 2280, 1720).contains(self.rect):
            self.kill()
