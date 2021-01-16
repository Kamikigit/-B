import pygame
from constants import (
    BULLET_WIDTH,
    BULLET_HEIGHT
)

# 弾
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.vx, self.vy = (vx, vy)
        self.image = pygame.image.load("img/nikukyu.png")    # 画像を読み込む
        self.rect = pygame.Rect(self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT)
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(self.vx, self.vy)
