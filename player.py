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
    PLAYER_VY,
    PLAYER_MAX_HP,
    PLAYER_MAX_MP,
    AX
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
        self.hp = PLAYER_MAX_HP
        self.mp = PLAYER_MAX_MP
        self.image = pygame.image.load("img/cat_head.png")    # 画像を読み込む

        self.punch_effect = pygame.image.load("img/cat_punch_effect.png")
        self.punchMotionFrame = 0

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
                self.vy = 0
                self.status = STATE_STANDING
            # 天井判定
            if self.y <= 0:
                self.y = 0
        elif :
        else:
            if self.vx > 0:
                self.vx -= AX
            elif self.vx < 0:
                self.vx += AX

            self.x += self.vx
            self.y += self.vy
            self.rect.move_ip(self.vx, self.vy)


    def jump(self, vx, vy):
        self.status = STATE_JUMPING
        self.vx = vx
        self.vy = vy
        # self.rect.move_ip(self.vx, self.vy)
    
    def right(self):
        self.vx = PLAYER_VX

    def left(self):
        self.vx = -PLAYER_VX

    def punch(self, dir):
        print("pos:", self.x + PLAYER_WIDTH / 2 + 20 * dir, self.y + PLAYER_HEIGHT / 2 - 20)
        rect = self.punch_effect.get_rect()
        rect.center = (self.x + PLAYER_WIDTH / 2 + 50 * dir, self.y + PLAYER_HEIGHT / 2 - 20)
        self.screen.blit(self.punch_effect, rect)

    def showPunchMotion(self):
