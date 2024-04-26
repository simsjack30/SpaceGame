import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/background.jpg")
        self.rect = self.image.get_rect(center=pos)
