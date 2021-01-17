import pygame
from constants import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    STATE_STANDING,
    STATE_JUMPING,
    STATE_ATTACKING,
    STATE_WIN,
    STATE_LOSE,
    G,
    MAX_VY,
    BOX_WIDTH,
    BOX_HEIGHT,
    PLAYER_Y,
    PLAYER_VX,
    PLAYER_VY,
    PLAYER_MAX_HP,
    PLAYER_MAX_MP,
    PLAYER_PUNCH_MOTION_FRAME,
    AX
)

# 自機
class Player(pygame.sprite.Sprite):
    
    class Punch(pygame.sprite.Sprite):
        def __init__(self, surface):
            pygame.sprite.Sprite.__init__(self)
            self.image = surface
            self.rect = self.image.get_rect()
        def set_rect(self, rect):
            self.rect = rect
    
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

        self.nikukyu_image = pygame.image.load("img/nikukyu.png")
        self.nikukyu = None
        self.punch_effect = pygame.image.load("img/cat_punch_effect.png")
        self.punchMotionFrame = 0
        self.punchDir = 0

        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.screen.blit(self.image, self.rect)

    def move(self):
        pass

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.screen.blit(self.image, self.rect)

        # playerが各状態の時に表示したい処理を追加
        if self.status == STATE_JUMPING:
            pass
        elif self.status == STATE_STANDING:
            pass
        elif self.status == STATE_ATTACKING:
            self.showPunchMotion()


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
        elif self.status == STATE_ATTACKING:
            if self.nikukyu != None:
                # 1フレームだけ肉球を表示して、以降のフレームであたり判定を出さないようにする
                self.nikukyu.update()
                self.nikukyu.kill()
                self.nikukyu = None
            if self.punchMotionFrame > 0:
                self.punchMotionFrame-=1
            
            if self.punchMotionFrame <= 0:
                self.punchMotionFrame = 0
                self.status = STATE_STANDING
        elif self.status == STATE_STANDING:
            assert self.vy == 0
            if self.vx > 0:
                self.vx -= AX
            elif self.vx < 0:
                self.vx += AX

            self.x += self.vx
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
        if self.punchMotionFrame > 0:
            # すでに攻撃中だったらなにもしない
            return
        
        self.punchDir = dir
        self.vx = 0
        self.vy = 0
        self.status = STATE_ATTACKING
        self.punchMotionFrame = PLAYER_PUNCH_MOTION_FRAME
        self.nikukyu = Player.Punch(self.nikukyu_image)
        rect = self.nikukyu_image.get_rect()
        rect.center = (self.x + PLAYER_WIDTH / 2 + 50 * self.punchDir, self.y + PLAYER_HEIGHT / 2)
        self.nikukyu.set_rect(rect)
 
    def showPunchMotion(self):
        rect = self.punch_effect.get_rect()
        rect.center = (self.x + PLAYER_WIDTH / 2 + 50 * self.punchDir, self.y + PLAYER_HEIGHT / 2)
        self.screen.blit(self.punch_effect, rect)

        rect = self.nikukyu_image.get_rect()
        rect.center = (self.x + PLAYER_WIDTH / 2 + 50 * self.punchDir, self.y + PLAYER_HEIGHT / 2)
        self.screen.blit(self.nikukyu_image, rect)

    def win(self):
        self.status = STATE_WIN
    
    def lose(self):
        self.status = STATE_LOSE