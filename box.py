import math

import pygame
from player import Player
from target import Target
from bullet import Bullet
from utils import show_health_bar, show_magic_point
from constants import (
    FONT_SIZE,
    STAGE_START,
    PLAYER_MAX_HP,
    ENEMY_MAX_HP,
    PLAYER_MAX_MP,
    ENEMY_MAX_MP,
    PLAYER_MAX_MP,
    ENEMY_MAX_MP,
    PLAYER_X,
    PLAYER_Y,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_VX,
    PLAYER_VY,
    TARGET_X,
    TARGET_Y,
    TARGET_VX,
    TARGET_VY,
    TARGET_WIDTH,
    WIDTH,
    HEIGHT,
    WHITE,
    STATE_STANDING,
    STATE_ATTACKING,
    STATE_HIT,
    BOX_WIDTH,
    STAGE_INTRO,
    STAGE_QUIT,
    STAGE_RUN,
    FPS,
)

# Box(ゲーム領域)の定義
class Box():
    def __init__(self, w, h):
        pygame.init()
        self.width = w
        self.height = h
        self.target = None
        self.font = pygame.font.SysFont('comicsansms', FONT_SIZE)
        self.font_intro = pygame.font.SysFont('comicsansms', 40)
        self.bg = pygame.image.load("img/bg.jpg")    # 背景画像の取得
        self.rect_bg = self.bg.get_rect()
        self.title = pygame.image.load("img/title.png")
        self.rect_title = self.bg.get_rect()
        self.deg = 0

    def set(self):   # 初期設定を一括して行う
        self.stage = STAGE_START
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()   # 時計オブジェクト
        self.player = Player(self.screen, PLAYER_X, PLAYER_Y, 0, 0, STATE_STANDING)
        self.target = Target(self.screen, TARGET_X, TARGET_Y, 0, 0, STATE_STANDING)
        self.show_score()


    def show_score(self):

        h_scale = 2
        self.screen.blit(self.font.render("HP", True, WHITE), [BOX_WIDTH-40, 20])
        show_health_bar(self.screen, self.player.hp / h_scale, PLAYER_MAX_HP / h_scale, (BOX_WIDTH-150, 20))
        self.screen.blit(self.font.render("MP", True, WHITE), [BOX_WIDTH-40, 40])
        show_magic_point(self.screen, self.player.mp, PLAYER_MAX_MP, (BOX_WIDTH - 130, 50))

        self.screen.blit(self.font.render("HP", True, WHITE), [20, 20])
        show_health_bar(self.screen, self.target.hp / h_scale, ENEMY_MAX_HP / h_scale, (50, 20))
        self.screen.blit(self.font.render("MP", True, WHITE), [20, 40])
        show_magic_point(self.screen, self.target.mp, ENEMY_MAX_MP, (70, 50))

    def run(self):
        while (self.stage != STAGE_QUIT):
            if self.stage == STAGE_START:
                self.intro()
            elif self.stage == STAGE_RUN:
                self.animate()


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
            enemy_direction = 1 if self.player.x < self.target.x else -1
            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT:
                    print("finish animation")
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN: # aキーで攻撃
                    if event.key == pygame.K_a:
                        self.player.shot(enemy_direction)
                    if event.key == pygame.K_s:
                        self.player.punch(enemy_direction)

            self.clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延

            pressed_keys = pygame.key.get_pressed() # キー情報を取得
            if pressed_keys[pygame.K_UP]:    # 上でジャンプ
                self.player.jump(0, -10)
            if pressed_keys[pygame.K_RIGHT]:
                self.player.right()
            if pressed_keys[pygame.K_LEFT]:
                self.player.left()

            if self.target.hp > 0:
                # 肉球の衝突判定
                collided = pygame.sprite.spritecollideany(self.target, self.player.bullets)
                if collided != None:
                    self.target.get_attacked('SHOT')
                    self.player.bullets.remove(collided)
                # 近接猫パンチとターゲットの衝突判定
                if self.player.nikukyu != None and pygame.sprite.collide_rect(self.target, self.player.nikukyu):
                    self.target.get_attacked('PUNCH')


            else:
                # プレイヤーが勝った
                self.player.win()
                self.target.lose()

            # オブジェクトのアップデート
            self.player.set_enemy(self.target)
            self.target.set_player(self.player)

            # お互いの情報を伝え合う
            self.player.update()
            self.target.update()
            
            # 表示の更新
            self.show_score()
            self.target.draw()
            self.player.draw()
            self.player.bullets.draw(self.screen)
            pygame.display.flip() # パドルとボールの描画を画面に反映
            self.screen.blit(self.bg, self.rect_bg)     # 背景画像
            # self.screen.fill((0, 0, 0))  # 塗潰し：次の flip まで反映されない
