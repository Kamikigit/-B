import pygame

class Effect(pygame.sprite.Sprite):
    def __init__(self, surface, rect, ttl):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = rect
        self.ttl = ttl
    def set_rect(self, rect):
        self.rect = rect

    def update(self):
        self.ttl -= 1

        if self.ttl <= 0:
            self.kill()
