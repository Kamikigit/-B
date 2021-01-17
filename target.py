import pygame
from constants import (
    TARGET_WIDTH,
    TARGET_HEIGHT,
    ENEMY_MAX_HP,
    ENEMY_MAX_MP,
    STATE_STANDING,
    STATE_ATTACKING,
    STATE_HIT,
    G
)

# 敵を作成
class Target(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, vx, vy, status):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.vx, self.vy = (vx, vy)
        self.hp = ENEMY_MAX_HP
        self.mp = ENEMY_MAX_MP
        self.image = pygame.image.load("img/car.png")    # 画像を読み込む
        self.rect = pygame.Rect(self.x, self.y, TARGET_WIDTH, TARGET_HEIGHT)
        self.screen.blit(self.image, self.rect)
        self.status = status

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, TARGET_WIDTH, TARGET_HEIGHT)
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        if self.status == STATE_ATTACKING:
            self.vx += G
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)
        elif self.status == STATE_HIT:
            self.vx -= G 
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)
        # 壁判定
        # if self.y >= BOX_HEIGHT - PLAYER_HEIGHT:

    def attacked_pic(self):
        self.image = pygame.image.load("img/car_attacked.png")
        self.screen.blit(self.image, self.rect)

    def lose_pic(self):
        self.image = pygame.image.load("img/car_lose.png")
        self.screen.blit(self.image, self.rect)

    def default_pic(self):
        self.image = pygame.image.load("img/car.png")
        self.screen.blit(self.image, self.rect)

    def attack(self, diff_x):
        self.status = STATE_ATTACKING
        self.diff_x = diff_x
        self.image = pygame.image.load("img/car_attack.png")
        self.screen.blit(self.image, self.rect)
    
    def attack_success(self):
        self.status = STATE_HIT
        self.image = pygame.image.load("img/car.png")
        self.screen.blit(self.image, self.rect)
