"""
游戏常量配置
"""

# ==================== 屏幕 / 棋盘 ====================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ROWS = 8
COLS = 8
BOARD_SIZE = 480

CELL_SIZE = BOARD_SIZE // COLS

BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = 62

SAVE_FILE = "save.json"

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"


# ==================== 颜色 ====================

BG_COLOR = (8, 12, 32)

NEBULA_PALETTE = [
    (70, 45, 120),
    (40, 80, 130),
    (100, 45, 100),
    (45, 60, 140),
    (60, 90, 150),
]

GALAXY_CORE_COLOR = (255, 240, 210)
GALAXY_INNER_COLOR = (200, 215, 245)
GALAXY_MID_COLOR = (130, 150, 220)
GALAXY_OUTER_COLOR = (70, 80, 160)
GALAXY_DUST_COLOR = (10, 12, 30)

STAR_COLOR_BRIGHT = (240, 245, 255)
STAR_COLOR_DIM = (150, 180, 230)

BOARD_GRID_COLOR = (70, 140, 220)
BOARD_BORDER_COLOR = (90, 180, 255)
BOARD_GLOW_COLOR = (60, 140, 230)

ROCKET_BODY_COLOR = (225, 230, 240)
ROCKET_BODY_DARK = (170, 180, 200)
ROCKET_TIP_COLOR = (245, 245, 250)
ROCKET_FIN_COLOR = (210, 80, 80)
ROCKET_WINDOW_COLOR = (80, 170, 230)
ROCKET_WINDOW_RIM = (200, 215, 235)

FLAME_COLOR_OUTER = (255, 140, 50)
FLAME_COLOR_MID = (255, 180, 80)
FLAME_COLOR_INNER = (255, 230, 150)

HIT_COLOR = (220, 70, 70)

TEXT_COLOR = (230, 240, 255)
TEXT_DIM_COLOR = (150, 180, 220)
TEXT_DISABLED_COLOR = (90, 105, 130)

BUTTON_COLOR = (30, 70, 140)
BUTTON_HOVER_COLOR = (50, 110, 200)
BUTTON_BORDER_COLOR = (90, 180, 255)

BUTTON_DISABLED_COLOR = (40, 45, 60)
BUTTON_DISABLED_BORDER = (80, 90, 110)

TIMER_BG_COLOR = (255, 240, 180)
TIMER_BG_ALPHA = 45
TIMER_BORDER_COLOR = (255, 225, 130)
TIMER_TEXT_COLOR = (255, 250, 230)

PAUSE_BUTTON_COLOR = (30, 70, 140)
PAUSE_BUTTON_HOVER = (50, 110, 200)
PAUSE_BUTTON_BORDER = (90, 180, 255)

OVERLAY_COLOR = (0, 0, 0, 160)
PAUSE_PANEL_COLOR = (20, 30, 60)
PAUSE_PANEL_BORDER = (90, 180, 255)

WHITE = (255, 255, 255)


# ==================== 字体 ====================

import pygame

# 注意：字体需要在 pygame.init() 之后才能创建
# 这里只存路径，字体对象由 main.py 创建后注入
title_font = None
large_font = None
font = None
small_font = None


def init_fonts():
    """初始化字体，必须在 pygame.init() 之后调用"""

    global title_font, large_font, font, small_font

    title_font = pygame.font.Font(FONT_PATH, 42)
    large_font = pygame.font.Font(FONT_PATH, 32)
    font = pygame.font.Font(FONT_PATH, 24)
    small_font = pygame.font.Font(FONT_PATH, 20)