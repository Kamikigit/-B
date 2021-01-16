# coding:UTF-8

import time
from pygame import Color 
import pygame
import random
import math

FPS = 60     # Frame per Second 毎秒のフレーム数

# 定数群
WIDTH = 1000            # ウィンドウの幅
HEIGHT = 320            # ウィンドウの高さ
BOX_WIDTH = 1000       # ゲーム領域の幅
BOX_HEIGHT = 320       # ゲーム領域の高さ

DURATION = 0.05        # 描画間隔

PLAYER_WIDTH = 100      # 自機の画像サイズ
PLAYER_HEIGHT = 100     
PLAYER_X = BOX_WIDTH - PLAYER_WIDTH
PLAYER_Y = BOX_HEIGHT - PLAYER_HEIGHT
PLAYER_VX = 10          # 自機の速度
PLAYER_VY = 10
MAX_VY = -200
STATE_JUMPING = 1       # 自機の状態
STATE_STANDING = 0

TARGET_VX = 0           # 敵機の速度
TARGET_VY = 0
TARGET_WIDTH = 260      # 敵機の画像サイズ
TARGET_HEIGHT = 260
TAEGET_X = 0            #敵機の出現位置
TARGET_Y = 50

BULLET_WIDTH = 50        # 弾の画像サイズ
BULLET_HEIGHT = 46


# ステージ状態
STAGE_START = 1
STAGE_INTRO = 2
STAGE_RUN = 3
STAGE_CAR = 4
STAGE_NORA = 5
STAGE_BOSS = 6
STAGE_OVER = 7
STAGE_QUIT = 8

#

MESSAGE_GAP = 20

WHITE = (255, 255, 255)
D = 10
MY_HP = 200
ENEMY_HP = 200

G = 1 # 重力

FONT_SIZE = 24


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


# ----------------------------------
# Box(ゲーム領域)の定義
class Box():
    def __init__(self, w, h):
        pygame.init()
        self.width = w
        self.height = h
        self.bullets = pygame.sprite.Group()
        self.target = None
        self.font = pygame.font.SysFont('comicsansms', FONT_SIZE)
        self.font_intro = pygame.font.SysFont('comicsansms', 40)
        self.bg = pygame.image.load("img/bg.jpg")    # 背景画像の取得
        self.rect_bg = self.bg.get_rect()
        self.title = pygame.image.load("img/title.png")
        self.rect_title = self.bg.get_rect()
        self.time = 0
        self.deg = 0

    def set(self):   # 初期設定を一括して行う
        self.stage = STAGE_START
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = screen
        self.myHP = MY_HP
        self.enemyHP = ENEMY_HP
        self.clock = pygame.time.Clock()   # 時計オブジェクト
        self.player = Player(screen, PLAYER_X, PLAYER_Y, PLAYER_VX, PLAYER_VY, STATE_STANDING)
        self.target = Target(screen, TAEGET_X, TARGET_Y, TARGET_VX, TARGET_VY )
        self.show_score()


    def show_score(self):
        text = self.font.render( ("ENEMY'S HP : %d" % self.enemyHP), True, WHITE)
        self.screen.blit(text, [20, 20])
        text = self.font.render( ("MY HP : %d" % self.myHP), True, WHITE)
        self.screen.blit(text, [BOX_WIDTH-120, 20])

    def run(self):
        while (self.stage != STAGE_QUIT):
            if self.stage == STAGE_START:
                self.intro()
            self.animate()
            self.myHP = 100
            # if self.stage == STAGE_DOWN and self.myHP > 0 and self.enemyHP <= 0:
            #     self.stage = STAGE_NEXT
            #     self.next()
            # if self.stage != STAGE_QUIT:
            #     if self.myHP <= 0:
            #         self.stage = STAGE_OVER
            #         self.game_over()
            #     else:       # 再開する
            #         self.stage = STAGE_RUN


    def intro_message(self):
        text = self.font_intro.render("PRESS SPACE", True, (0, 0, 0))
        position = text.get_rect()
        position.center = (WIDTH/2, 250)
        alpha = (math.cos(float(self.deg) / 180 * math.pi) + 1) / 2 * 255
        text.set_alpha(alpha)
        self.screen.blit(text, position)
        self.deg = (self.deg + 5) % 360

    def intro(self):
        self.stage = STAGE_INTRO
        while (self.stage == STAGE_INTRO):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.stage = STAGE_RUN


            self.clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延
            self.intro_message()
            pygame.display.flip()
            self.screen.fill((0,0,0))
            self.screen.blit(self.title, self.rect_title)



    def animate(self):
        while (self.stage == STAGE_RUN):  # メインループ
            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: LOOP = False
                if event.type == pygame.KEYDOWN: # aキーで攻撃
                    if event.key == pygame.K_a:
                        self.bullets.add(Bullet(self.screen, self.player.x, self.player.y, -3, 0))         

            self.clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延

            pressed_keys = pygame.key.get_pressed() # キー情報を取得
            if pressed_keys[pygame.K_UP]:    # 上でジャンプ
                self.player.jump(0, -10)
            if pressed_keys[pygame.K_RIGHT]:
                self.player.right()
            if pressed_keys[pygame.K_LEFT]:
                self.player.left()
            # if pressed_keys[pygame.K_a]:    # aで攻撃
            #     self.bullets.add(Bullet(self.screen, self.player.x, self.player.y, -3, 0))         

            # オブジェクトのアップデート
            self.bullets.update()
            self.player.update()

            # 衝突判定
            collided = pygame.sprite.spritecollideany(self.target, self.bullets)
            if self.enemyHP > 0:
                if collided != None:
                    self.time = 40
                    self.enemyHP -= 3
                    self.bullets.remove(collided)

                if self.time > 0:
                    self.target.attacked_pic()
                    self.time -= 1
                else:
                    self.target.default_pic()
        
            else:
                self.target.lose_pic()
            # print(self.player.y, BOX_HEIGHT - PLAYER_HEIGHT)
            # 表示の更新
            self.show_score()
            self.bullets.draw(self.screen)
            self.target.draw()
            self.player.draw()
            pygame.display.flip() # パドルとボールの描画を画面に反映
            self.screen.blit(self.bg, self.rect_bg)     # 背景画像
            # self.screen.fill((0, 0, 0))  # 塗潰し：次の flip まで反映されない

box = Box(BOX_WIDTH, BOX_HEIGHT)
box.set()       # ゲームの初期設定
box.run()       # ステージの切り替え
box.animate()   # アニメーション
pygame.quit()   # 画面を閉じる