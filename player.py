import pygame
from constants import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    STATE_STANDING,
    STATE_JUMPING,
    G,
    MAX_VY,
    BOX_WIDTH,
    BOX_HEIGHT,
    PLAYER_Y,
    PLAYER_VX,
    PLAYER_VY
)

# 自機
class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y,  vx, vy, status):
        pygame.sprite.Sprite.__init__(self)  # spriteを継承
        self.status = status
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.image = pygame.image.load("img/cat_head.png")    # 画像を読み込む
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.screen.blit(self.image, self.rect)

    def move(self):
        pass

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.status == STATE_JUMPING:
            self.vy += G    
            self.vy = max(self.vy, MAX_VY)
            self.x += self.vx
            self.y += self.vy
            self.rect.move_ip(self.vx, self.vy)
            # 地面判定
            if self.y >= BOX_HEIGHT - PLAYER_HEIGHT: # ==はだめ
                self.y = PLAYER_Y       # 埋まるのを防ぐ
                self.status = STATE_STANDING
            # 天井判定
            if self.y <= 0:
                self.y = 0
            
        else:
            self.vx = PLAYER_VX
            self.vy = PLAYER_VY
            self.rect.move_ip(self.vx, self.vy)

    def jump(self, vx, vy):
        self.status = STATE_JUMPING
        self.vx = vx
        self.vy = vy
        # self.rect.move_ip(self.vx, self.vy)
    
    def right(self):
        x = self.x + self.vx
        if x + PLAYER_WIDTH < BOX_WIDTH:
            self.x = x

    def left(self):
        x = self.x - self.vx
        if x > 0:
            self.x = x