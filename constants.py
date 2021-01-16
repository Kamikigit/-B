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
TARGET_X = 0            #敵機の出現位置
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
