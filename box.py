import math
from time import sleep
import random

import pygame
from player import Player
from target import Target
from bullet import Bullet
from effect import Effect
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
    BOX_HEIGHT,
    STAGE_INTRO,
    STAGE_TUTORIAL,
    STAGE_QUIT,
    STAGE_RUN,
    STAGE_CLEAR,
    STAGE_OVER,
    STAGE_CUTIN,
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
        self.rect_title = self.title.get_rect()
        self.tutorial = pygame.image.load("img/tutorial.png")
        self.rect_tutorial = self.tutorial.get_rect()
        self.star_guide_image = pygame.image.load("img/fukidashi.png")
        self.cutin_image = []           # 百裂肉球
        for i in range(25):
            cutin = pygame.image.load("img/cutin/frame_{:02}_delay-0.1s.gif".format(i))
            self.cutin_image.append(cutin)
        self.cutin_index = 0
        self.deg = 0

    def set(self):   # 初期設定を一括して行う
        self.stage = STAGE_START
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cat Fighter Z")
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
                self.show_intro_screen()
            elif self.stage == STAGE_TUTORIAL:
                self.show_tutorial_screen()
            elif self.stage == STAGE_RUN:
                self.show_battle_screen()
            elif self.stage == STAGE_CLEAR:
                self.show_clear_screen()
            elif self.stage == STAGE_OVER:
                self.show_gameover_screen()
            elif self.stage == STAGE_CUTIN:
                self.show_cutin_screen()


    def intro_message(self):
        text = self.font_intro.render("PRESS SPACE", True, (0, 0, 0))
        position = text.get_rect()
        position.center = (WIDTH/2, 250)
        alpha = (math.cos(float(self.deg) / 180 * math.pi) + 1) / 2 * 255
        text.set_alpha(alpha)
        self.screen.blit(text, position)
        self.deg = (self.deg + 5) % 360

    def show_intro_screen(self):
        self.stage = STAGE_INTRO
        while (self.stage == STAGE_INTRO):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.stage = STAGE_TUTORIAL


            self.clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延
            self.intro_message()
            pygame.display.flip()
            self.screen.fill((0,0,0))
            self.screen.blit(self.title, self.rect_title)

    def show_tutorial_screen(self):
        while(self.stage == STAGE_TUTORIAL):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.stage = STAGE_RUN
                        self.clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延
            pygame.display.flip()
            self.screen.fill((0,0,0))
            self.screen.blit(self.tutorial, self.rect_tutorial)   

    def show_battle_screen(self):
        while (self.stage == STAGE_RUN):  # メインループ
            if self.target.hp <= 0:
                # プレイヤーが勝った
                self.player.win()
                self.target.lose()
                self.stage = STAGE_CLEAR
                sleep(1)
                return
            if self.player.hp <= 0:
                # 敵が勝った
                self.player.lose()
                self.target.lose()
                self.stage = STAGE_OVER
                sleep(1)
                return
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
                self.player.jump(0, -15)
            if pressed_keys[pygame.K_RIGHT]:
                self.player.right()
            if pressed_keys[pygame.K_LEFT]:
                self.player.left()
            if self.player.mp == PLAYER_MAX_MP: # 百裂肉球を表示する
                position = self.star_guide_image.get_rect()
                position.center = (WIDTH/4*3+20, 40)
                alpha = (math.cos(float(self.deg) / 180 * math.pi) + 1) * 255
                self.star_guide_image.set_alpha(alpha)
                self.screen.blit(self.star_guide_image, position)
                self.deg = (self.deg + 3) % 360
                if pressed_keys[pygame.K_z]:  # 百裂肉球
                    for i in range(4):
                        surface = pygame.image.load("img/explosion_small.png")
                        rect = surface.get_rect()
                        rect.center = (random.randrange(BOX_WIDTH), random.randrange(BOX_HEIGHT))
                        effect = Effect(surface, rect, 100)
                        self.player.effects.add(effect)

                        surface = pygame.image.load("img/explosion_big.png")
                        rect = surface.get_rect()
                        rect.center = (random.randrange(BOX_WIDTH), random.randrange(BOX_HEIGHT))
                        effect = Effect(surface, rect, 100)
                        self.player.effects.add(effect)
                    self.stage = STAGE_CUTIN

            # 肉球の衝突判定
            collided = pygame.sprite.spritecollideany(self.target, self.player.bullets)
            if collided != None:
                self.target.get_attacked('SHOT')
                self.player.bullets.remove(collided)
            # 近接猫パンチとターゲットの衝突判定
            if self.player.nikukyu != None and pygame.sprite.collide_rect(self.target, self.player.nikukyu):
                self.target.get_attacked('PUNCH')



            # お互いの情報を伝え合う
            self.player.set_enemy(self.target)
            self.target.set_player(self.player)

            # オブジェクトのアップデート
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

    def show_cutin_screen(self):
        repeat_num = 2
        fps_scale = 3
        self.clock.tick(FPS)
        print(self.cutin_index)
        self.screen.blit(self.cutin_image[(self.cutin_index % (25 * fps_scale)) // fps_scale], self.cutin_image[(self.cutin_index % (25 * fps_scale)) // fps_scale].get_rect())
        self.cutin_index += 1
        pygame.display.flip()

        if self.cutin_index == 25 * fps_scale * repeat_num:
            self.cutin_index = 0
            self.stage = STAGE_RUN


    def show_clear_screen(self):
        self.clock.tick(FPS)
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        text = self.font_intro.render("CLEARED!!", True, (255, 255, 255))
        position = text.get_rect()
        position.center = (WIDTH / 2, HEIGHT / 2)
        self.screen.blit(text, position)

        

    def show_gameover_screen(self):
        self.clock.tick(FPS)
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        text = self.font_intro.render("GAME OVER!!", True, (255, 255, 255))
        position = text.get_rect()
        position.center = (WIDTH / 2, HEIGHT / 2)
        self.screen.blit(text, position)