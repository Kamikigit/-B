import pygame
from constants import (
    TARGET_WIDTH,
    TARGET_HEIGHT,
)

# 敵を作成
class Target(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.vx, self.vy = (vx, vy)
        self.image = pygame.image.load("img/car.png")    # 画像を読み込む
        self.rect = pygame.Rect(self.x, self.y, TARGET_WIDTH, TARGET_HEIGHT)
        self.screen.blit(self.image, self.rect)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, TARGET_WIDTH, TARGET_HEIGHT)
        self.screen.blit(self.image, self.rect)

    def attacked_pic(self):
        self.image = pygame.image.load("img/car_attacked.png")
        self.screen.blit(self.image, self.rect)

    def lose_pic(self):
        self.image = pygame.image.load("img/car_lose.png")
        self.screen.blit(self.image, self.rect)

    def default_pic(self):
        self.image = pygame.image.load("img/car.png")
        self.screen.blit(self.image, self.rect)