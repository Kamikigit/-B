# coding:UTF-8

import time
from pygame import Color 
import pygame
import random
import math
from constants import *
from box import Box


# ----------------------------------

box = Box(BOX_WIDTH, BOX_HEIGHT)
box.set()       # ゲームの初期設定
box.run()       # ステージの切り替え
# box.animate()   # アニメーション
# pygame.quit()   # 画面を閉じる
