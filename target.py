import pygame
from utils import checkcollision
from constants import (
    TARGET_WIDTH,
    TARGET_HEIGHT,
    ENEMY_MAX_HP,
    ENEMY_MAX_MP,
    STATE_STANDING,
    STATE_ATTACKING,
    STATE_ATTACKED,
    STATE_HIT,
    STATE_WIN,
    STATE_LOSE,
    G,
    PLAYER_ATTACK_KIND,
    ENEMY_ATTACK_KIND,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    BOX_WIDTH
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
        self.player = None

        self.image = pygame.image.load("img/car.png")    # 画像を読み込む
        self.rect = pygame.Rect(self.x, self.y, TARGET_WIDTH, TARGET_HEIGHT)
        self.screen.blit(self.image, self.rect)
        self.status = status
        self.attackedMotionFrame = 0
        self.sprites = {
            STATE_STANDING: pygame.image.load("img/car.png"),
            STATE_ATTACKING: pygame.image.load("img/car_attack.png"),
            STATE_HIT: pygame.image.load("img/car_attack.png"),
            STATE_ATTACKED: pygame.image.load("img/car_attacked.png"),
            STATE_LOSE: pygame.image.load("img/car_lose.png"),
        }

    
    def set_player(self, player):
        self.player = player

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, TARGET_WIDTH, TARGET_HEIGHT)
        self.screen.blit(self.sprites[self.status], self.rect)

    def update(self):
        assert self.player != None

        if self.hp <= 0:
            self.hp = 0
            self.status = STATE_LOSE

        if self.status == STATE_STANDING:
            if abs((self.player.x + PLAYER_WIDTH / 2) - (self.x + TARGET_WIDTH / 2)) < 300:
                self.status = STATE_ATTACKING

            if self.vx > 0:
                self.vx -= G * 0.5
            elif self.vx < 0:
                self.vx += G * 0.5
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)

        elif self.status == STATE_ATTACKING:
            if abs((self.player.x + PLAYER_WIDTH / 2) - (self.x + TARGET_WIDTH / 2)) >= 300:
                self.status = STATE_STANDING
            dir = 1 if (self.player.x + PLAYER_WIDTH / 2) - (self.x + TARGET_WIDTH / 2) > 0 else -1
            self.vx += (G * 0.2 * dir)
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)
        elif self.status == STATE_ATTACKED:
            if self.vx > 0:
                self.vx -= G * 0.2
            elif self.vx < 0:
                self.vx += G * 0.2
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)

            self.attackedMotionFrame -= 1
            if self.attackedMotionFrame <= 0:
                self.attackedMotionFrame = 0
                self.status = STATE_STANDING
        elif self.status == STATE_HIT:
            if self.vx > 0:
                self.vx -= G * 0.2
            elif self.vx < 0:
                self.vx += G * 0.2
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)
            self.hitMotionFrame -= 1
            if self.hitMotionFrame <= 0:
                self.hitMotionFrame = 0
                self.status = STATE_STANDING if abs((self.player.x + PLAYER_WIDTH / 2) - (self.x + TARGET_WIDTH / 2)) >= 300 else STATE_ATTACKING
            
        # 壁判定
        if self.x < 0:
            self.x = 0
        if self.x + TARGET_WIDTH > BOX_WIDTH:
            self.x = BOX_WIDTH - TARGET_WIDTH

        bb1 = {
            'x1': self.x,
            'y1': self.y,
            'x2': self.x + TARGET_WIDTH,
            'y2': self.y + TARGET_HEIGHT
        }
        bb2 = {
            'x1': self.player.x,
            'y1': self.player.y,
            'x2': self.player.x + PLAYER_WIDTH,
            'y2': self.player.y + PLAYER_HEIGHT
        }

        if checkcollision(bb1, bb2, 30):
            if self.status != STATE_HIT:
                # 今のフレームで初めてヒットになったら
                self.status = STATE_HIT
                self.hitMotionFrame = ENEMY_ATTACK_KIND['BODY_BLOW']['stop_time'] / 5
                dir = 1 if (self.x + TARGET_WIDTH / 2) - (self.player.x + PLAYER_WIDTH / 2) > 0 else -1
                self.vx = dir * 2


    def attack(self, diff_x):
        self.status = STATE_ATTACKING
        self.diff_x = diff_x

    def get_attacked(self, attack_kind):
        assert attack_kind in (
            "SHOT",
            "PUNCH"
        )
        self.status = STATE_ATTACKED
        
        stop_time = PLAYER_ATTACK_KIND[attack_kind]['stop_time']
        damage = PLAYER_ATTACK_KIND[attack_kind]['damage']
        knock_back = PLAYER_ATTACK_KIND[attack_kind]['knock_back']
        dir = -1 if (self.player.x + PLAYER_WIDTH / 2) - (self.x + TARGET_WIDTH / 2) > 0 else 1
        self.vx = knock_back * dir
        self.hp -= damage
        
        self.attackedMotionFrame = stop_time


    
    def lose(self):
        self.status = STATE_LOSE

    def win(self):
        self.status = STATE_WIN