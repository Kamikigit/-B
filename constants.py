FPS = 60     # Frame per Second 毎秒のフレーム数

# 定数群
WIDTH = 1000            # ウィンドウの幅
HEIGHT = 320            # ウィンドウの高さ
BOX_WIDTH = 1000       # ゲーム領域の幅
BOX_HEIGHT = 320       # ゲーム領域の高さ

DURATION = 0.05        # 描画間隔

PLAYER_WIDTH = 80      # 自機の画像サイズ
PLAYER_HEIGHT = 80     
PLAYER_X = BOX_WIDTH - PLAYER_WIDTH
PLAYER_Y = BOX_HEIGHT - PLAYER_HEIGHT
PLAYER_VX = 10          # 自機の速度
PLAYER_VY = 10
MAX_VY = -200
PLAYER_ATTACK_KIND = {
    'SHOT': {
        'stop_time': 10,
        'damage': 1,
        'knock_back': 2,
    },
    'PUNCH': {
        'stop_time': 20,
        'damage': 10,
        'knock_back': 5,
    },
}

ENEMY_ATTACK_KIND = {
    'BODY_BLOW': {
        'stop_time': 10,
        'damage': 3,
        'knock_back': 10,
    }
}

PLAYER_PUNCH_MOTION_FRAME = 10

STATE_STANDING = 0      # 自機や適機の状態
STATE_JUMPING = 1 
STATE_ATTACKING = 2
STATE_ATTACKED = 3
STATE_HIT = 4
STATE_LOSE = 5
STATE_WIN = 6

TARGET_VX = 0           # 敵機の速度
TARGET_VY = 0
TARGET_WIDTH = 200      # 敵機の画像サイズ
TARGET_HEIGHT = 180
TARGET_X = 0            #敵機の出現位置
TARGET_Y = BOX_HEIGHT - TARGET_HEIGHT


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

# プレイヤーと敵の最大HP,MP
PLAYER_MAX_HP = 200
ENEMY_MAX_HP = 200
PLAYER_MAX_MP = 3
ENEMY_MAX_MP = 3

G = 1 # 重力
AX = 1 # 横方向に減速する時の加速度

FONT_SIZE = 24
