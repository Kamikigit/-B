import pygame
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
        self.attackedMotionFrame = 0
        self.sprites = {
            STATE_STANDING: pygame.image.load("img/car.png"),
            STATE_ATTACKING: pygame.image.load("img/car_attack.png"),
            STATE_ATTACKED: pygame.image.load("img/car_attacked.png"),
            STATE_LOSE: pygame.image.load("img/car_lose.png"),
        }

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, TARGET_WIDTH, TARGET_HEIGHT)
        self.screen.blit(self.sprites[self.status], self.rect)
    
    def update(self):
        if self.hp <= 0:
            self.hp = 0
            self.status = STATE_LOSE

        if self.status == STATE_ATTACKING:
            self.vx += G
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)
        elif self.status == STATE_HIT:
            self.vx -= G 
            self.x += self.vx
            self.rect.move_ip(self.vx, self.vy)
        elif self.status == STATE_ATTACKED:
            self.attackedMotionFrame -= 1
            if self.attackedMotionFrame <= 0:
                self.attackedMotionFrame = 0
                self.status = STATE_STANDING
            
        # 壁判定
        # if self.y >= BOX_HEIGHT - PLAYER_HEIGHT:


    def attack(self, diff_x):
        self.status = STATE_ATTACKING
        self.diff_x = diff_x

    def attack_success(self):
        self.status = STATE_HIT

    def get_attacked(self, attack_kind):
        assert attack_kind in (
            "SHOT",
            "PUNCH"
        )
        self.status = STATE_ATTACKED
        
        stop_time = PLAYER_ATTACK_KIND[attack_kind]['stop_time']
        damage = PLAYER_ATTACK_KIND[attack_kind]['damage']
        if attack_kind == 'SHOT':
            self.hp -= damage
        elif attack_kind == 'PUNCH':
            self.hp -= damage
        
        self.attackedMotionFrame = stop_time
        
        
        self.attackedMotionFrame = stop_time
    
    def lose(self):
        self.status = STATE_LOSE

    def win(self):
        self.status = STATE_WIN