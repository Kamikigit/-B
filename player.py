import pygame
from bullet import Bullet
from utils import checkcollision
from constants import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    STATE_STANDING,
    STATE_JUMPING,
    STATE_ATTACKING,
    STATE_ATTACKED,
    STATE_HIT,
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
    ENEMY_ATTACK_KIND,
    TARGET_WIDTH,
    TARGET_HEIGHT
)

from effect import Effect

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
        self.enemy = None
        self.effects = pygame.sprite.Group()

        self.image = pygame.image.load("img/cat_head.png")    # 画像を読み込む
        self.body_blow_effect = pygame.image.load("img/cat_punch_effect.png")


        # 肉球ショット
        self.bullets = pygame.sprite.Group()

        # 猫パンチ
        self.nikukyu_image = pygame.image.load("img/nikukyu.png")
        self.nikukyu = None
        self.punch_effect = pygame.image.load("img/cat_punch_effect.png")
        self.punchMotionFrame = 0
        self.punchDir = 0

        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.screen.blit(self.image, self.rect)

    def set_enemy(self, enemy):
        self.enemy = enemy

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
        
        self.effects.draw(self.screen)


    def update(self):
        assert self.enemy != None

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
                self.vx -= G * 0.5
            elif self.vx < 0:
                self.vx += G * 0.5
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)
        elif self.status == STATE_HIT:
            if self.vx > 0:
                self.vx -= G * 0.3
            elif self.vx < 0:
                self.vx += G * 0.3
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)

            self.hitMotionFrame -=1

            if self.hitMotionFrame <= 0:
                self.hitMotionFrame = 0
                self.status = STATE_JUMPING if self.vy != 0 else STATE_STANDING

        # 壁判定
        if self.x < 0:
            self.x = 0
        if self.x + PLAYER_WIDTH > BOX_WIDTH:
            self.x = BOX_WIDTH - PLAYER_WIDTH

        bb1 = {
            'x1': self.x,
            'y1': self.y,
            'x2': self.x + PLAYER_WIDTH,
            'y2': self.y + PLAYER_HEIGHT
        }
        bb2 = {
            'x1': self.enemy.x,
            'y1': self.enemy.y,
            'x2': self.enemy.x + TARGET_WIDTH,
            'y2': self.enemy.y + TARGET_HEIGHT
        }
        if checkcollision(bb1, bb2, 30):
            if self.status != STATE_HIT:
                # 今のフレームで初めてヒットになったら
                self.status = STATE_HIT
                self.hitMotionFrame = ENEMY_ATTACK_KIND['BODY_BLOW']['stop_time']
                self.hp -= ENEMY_ATTACK_KIND['BODY_BLOW']['damage']
                dir = 1 if (self.x + PLAYER_WIDTH / 2) - (self.enemy.x + TARGET_WIDTH / 2) > 0 else -1
                self.vx = ENEMY_ATTACK_KIND['BODY_BLOW']['knock_back'] * dir

                self.show_hit_effect()
        

        self.bullets.update()

        self.effects.update()

    def jump(self, vx, vy):
        self.status = STATE_JUMPING
        self.vx = vx
        self.vy = vy
        # self.rect.move_ip(self.vx, self.vy)
    
    def right(self):
        self.vx = PLAYER_VX

    def left(self):
        self.vx = -PLAYER_VX

    def shot(self, dir):
        self.bullets.add(Bullet(self.screen, self.x + PLAYER_WIDTH / 2, self.y + PLAYER_HEIGHT / 2 - 30, 5 * dir, -2))

    def punch(self, dir):
        if self.status == STATE_ATTACKING:
            print("already punching")
            # すでに攻撃中だったらなにもしない
            return
        
        self.punchDir = dir
        self.vx = 0
        self.vy = 0
        self.status = STATE_ATTACKING
        self.punchMotionFrame = PLAYER_PUNCH_MOTION_FRAME
        rect = self.nikukyu_image.get_rect()
        rect.center = (self.x + PLAYER_WIDTH / 2 + 50 * self.punchDir, self.y + PLAYER_HEIGHT / 2)
        self.nikukyu = Effect(self.nikukyu_image, rect, 1)
 
    def showPunchMotion(self):
        rect = self.punch_effect.get_rect()
        rect.center = (self.x + PLAYER_WIDTH / 2 + 50 * self.punchDir, self.y + PLAYER_HEIGHT / 2)
        self.screen.blit(self.punch_effect, rect)

        rect = self.nikukyu_image.get_rect()
        rect.center = (self.x + PLAYER_WIDTH / 2 + 50 * self.punchDir, self.y + PLAYER_HEIGHT / 2)
        self.screen.blit(self.nikukyu_image, rect)


    def show_hit_effect(self):
        rect = self.body_blow_effect.get_rect()
        rect.center = (self.x + PLAYER_WIDTH / 2, self.y + PLAYER_HEIGHT / 2)
        effect = Effect(self.body_blow_effect, rect, 5)
        self.effects.add(effect)

    def win(self):
        self.status = STATE_WIN
    
    def lose(self):
        self.status = STATE_LOSE