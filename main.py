"""
editor: Lai Yanran
date: 2026-09-21
task: 一箭又一箭
"""

import math
import random

import pygame

from game.arrow import Arrow
from game.board import Board
from levels.levels import LEVELS


# ==================== 基本设置 ====================

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("一箭又一箭")

clock = pygame.time.Clock()

ROWS = 8
COLS = 8
BOARD_SIZE = 480

CELL_SIZE = BOARD_SIZE // COLS

BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = 62


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

BUTTON_COLOR = (30, 70, 140)
BUTTON_HOVER_COLOR = (50, 110, 200)
BUTTON_BORDER_COLOR = (90, 180, 255)

# 计时器
TIMER_BG_COLOR = (255, 240, 180)
TIMER_BG_ALPHA = 45
TIMER_BORDER_COLOR = (255, 225, 130)
TIMER_TEXT_COLOR = (255, 250, 230)

WHITE = (255, 255, 255)


# ==================== 字体 ====================

font_path = "C:/Windows/Fonts/msyh.ttc"

title_font = pygame.font.Font(font_path, 42)
large_font = pygame.font.Font(font_path, 32)
font = pygame.font.Font(font_path, 24)
small_font = pygame.font.Font(font_path, 20)


# ==================== 星空生成 ====================

STAR_SEED = 20260921

random.seed(STAR_SEED)


def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def multi_stop_gradient(stops, t):
    t = max(0.0, min(1.0, t))

    for i in range(len(stops) - 1):

        p1, c1 = stops[i]
        p2, c2 = stops[i + 1]

        if p1 <= t <= p2:
            local_t = (t - p1) / (p2 - p1) if p2 > p1 else 0
            return lerp_color(c1, c2, local_t)

    return stops[-1][1]


def build_starfield_surface():
    """预渲染星云 + 银河"""

    surface = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )

    # ---------- 星云 ----------

    nebula_centers = [
        (-60, 520, 340, 0),
        (760, 100, 320, 1),
        (80, -40, 280, 2),
        (820, 560, 300, 3),
        (400, 620, 260, 4),
    ]

    for cx, cy, radius, palette_index in nebula_centers:

        base_color = NEBULA_PALETTE[palette_index]

        for _ in range(180):

            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(0, 1) ** 0.7 * radius

            px = cx + math.cos(angle) * dist
            py = cy + math.sin(angle) * dist

            r = random.uniform(15, 55) * (1 - dist / radius * 0.6)
            r = max(8, r)

            a = int(28 * (1 - dist / radius) + random.uniform(0, 10))
            a = max(4, min(40, a))

            tint = random.uniform(0, 1) * 0.4
            color = lerp_color(base_color, WHITE, tint)

            pygame.draw.circle(
                surface,
                (*color, a),
                (int(px), int(py)),
                int(r)
            )

    # ---------- 银河 ----------

    def galaxy_point(t):
        x = SCREEN_WIDTH * 1.05 - t * SCREEN_WIDTH * 1.25
        y = SCREEN_HEIGHT * 0.95 - t * SCREEN_HEIGHT * 1.1
        y += math.sin(t * math.pi) * 40
        return x, y

    def galaxy_tangent(t):
        dx = -SCREEN_WIDTH * 1.25
        dy = -SCREEN_HEIGHT * 1.1 + math.cos(t * math.pi) * 40 * math.pi
        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        return dx / length, dy / length

    def galaxy_normal(t):
        tx, ty = galaxy_tangent(t)
        return -ty, tx

    galaxy_stops = [
        (0.0, GALAXY_CORE_COLOR),
        (0.12, GALAXY_INNER_COLOR),
        (0.35, GALAXY_MID_COLOR),
        (0.7, GALAXY_OUTER_COLOR),
        (1.0, (30, 35, 80)),
    ]

    for _ in range(220):

        t = random.uniform(0, 1)
        cx, cy = galaxy_point(t)
        nx, ny = galaxy_normal(t)

        offset = random.gauss(0, 45)

        px = cx + nx * offset
        py = cy + ny * offset

        dist_factor = min(1.0, abs(offset) / 90)

        color = multi_stop_gradient(galaxy_stops, dist_factor)

        r = random.randint(6, 14)
        a = int(12 * (1 - dist_factor) + random.uniform(0, 4))
        a = max(2, min(16, a))

        pygame.draw.circle(surface, (*color, a), (int(px), int(py)), r)

    for _ in range(700):

        t = random.uniform(0, 1)
        cx, cy = galaxy_point(t)
        nx, ny = galaxy_normal(t)

        offset = random.gauss(0, 18)

        px = cx + nx * offset
        py = cy + ny * offset

        dist_factor = min(1.0, abs(offset) / 45)

        color = multi_stop_gradient(galaxy_stops, dist_factor)

        r = random.randint(1, 3)
        a = int(28 * (1 - dist_factor) + random.uniform(0, 8))
        a = max(4, min(40, a))

        pygame.draw.circle(surface, (*color, a), (int(px), int(py)), r)

    for _ in range(260):

        t = random.uniform(0, 1)
        cx, cy = galaxy_point(t)
        nx, ny = galaxy_normal(t)

        offset = random.gauss(0, 12)

        px = cx + nx * offset
        py = cy + ny * offset

        dist_factor = min(1.0, abs(offset) / 30)

        r = random.randint(2, 5)
        a = int(26 * (1 - dist_factor) + random.uniform(0, 6))
        a = max(6, min(32, a))

        pygame.draw.circle(
            surface,
            (*GALAXY_DUST_COLOR, a),
            (int(px), int(py)),
            r
        )

    for _ in range(60):

        t = random.uniform(0, 1)
        cx, cy = galaxy_point(t)
        nx, ny = galaxy_normal(t)

        offset = random.gauss(0, 22)

        px = cx + nx * offset
        py = cy + ny * offset

        color = GALAXY_INNER_COLOR
        r = random.choice([1, 1, 2])
        a = random.randint(80, 160)

        pygame.draw.circle(surface, (*color, a), (int(px), int(py)), r)

    return surface


starfield_surface = build_starfield_surface()


# ---------- 星星 ----------

stars = []

for _ in range(140):

    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)

    radius = random.choice([1, 1, 1, 2, 2, 3])

    base_brightness = random.uniform(0.5, 1.0)
    phase = random.uniform(0, math.pi * 2)

    if random.random() < 0.3:
        speed = random.uniform(0.06, 0.10)
        flicker_amp = 0.45
    else:
        speed = random.uniform(0.02, 0.05)
        flicker_amp = 0.2

    has_cross = radius >= 3 and base_brightness > 0.85

    stars.append(
        (x, y, radius, base_brightness, phase, speed, flicker_amp, has_cross)
    )


# ---------- 星球 ----------

def build_planet_texture(seed_offset, count):
    rng = random.Random(STAR_SEED + seed_offset)

    points = []

    for _ in range(count):

        lon = rng.uniform(0, math.pi * 2)
        lat = rng.uniform(-math.radians(75), math.radians(75))

        size = rng.uniform(0.08, 0.18)
        alpha = rng.randint(30, 70)

        points.append((lon, lat, size, alpha))

    return points


PLANET_SMALL = {
    "x": 90,
    "y": 130,
    "radius": 26,
    "base_color": (60, 70, 110),
    "light_color": (120, 140, 190),
    "texture": build_planet_texture(1, 40),
    "rot_speed": 0.15,
    "ring": False,
}

PLANET_LARGE = {
    "x": 720,
    "y": 500,
    "radius": 48,
    "base_color": (70, 60, 100),
    "light_color": (150, 130, 180),
    "texture": build_planet_texture(2, 70),
    "rot_speed": 0.08,
    "ring": True,
    "ring_color": (140, 130, 180),
    "ring_tilt": 0.35,
}


# ==================== 游戏变量 ====================

game_state = "start"

current_level = 0

board = None
arrows = []

mistakes = 3

# 计时器
level_start_ticks = 0       # 本关开始时刻（毫秒）
level_elapsed_ms = 0        # 本关已耗时（毫秒，停表后固定）
timer_running = False       # 是否正在计时


tutorial_timer = 0
tutorial_arrow_x = 0
tutorial_arrows = []


# ==================== 基本函数 ====================

def load_level(level_index):

    global board
    global arrows
    global mistakes
    global level_start_ticks
    global level_elapsed_ms
    global timer_running

    board = Board(ROWS, COLS)
    arrows = []

    for row, col, direction in LEVELS[level_index]:

        arrow = Arrow(row, col, direction)

        board.add_arrow(arrow)
        arrows.append(arrow)

    mistakes = 3

    for arrow in arrows:

        x, y = get_cell_center(arrow.row, arrow.col)
        arrow.set_position(x, y)

    # 重置计时器并开始计时
    level_start_ticks = pygame.time.get_ticks()
    level_elapsed_ms = 0
    timer_running = True


def get_cell_center(row, col):

    x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

    return x, y


def stop_timer():

    global level_elapsed_ms
    global timer_running

    if timer_running:
        level_elapsed_ms = pygame.time.get_ticks() - level_start_ticks
        timer_running = False


def get_elapsed_ms():

    if timer_running:
        return pygame.time.get_ticks() - level_start_ticks
    else:
        return level_elapsed_ms


def format_time(ms):

    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


# ==================== 绘制星球 ====================

def draw_planet(planet, time_s):

    cx = planet["x"]
    cy = planet["y"]
    radius = planet["radius"]

    base_color = planet["base_color"]
    light_color = planet["light_color"]

    if planet["ring"]:

        ring_color = planet["ring_color"]

        ring_rx = int(radius * 1.9)
        ring_ry = int(radius * 0.55)

        ring_surface = pygame.Surface(
            (ring_rx * 2 + 4, ring_ry * 2 + 4),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            ring_surface,
            (*ring_color, 90),
            (2, 2, ring_rx * 2, ring_ry * 2),
            width=3
        )

        pygame.draw.ellipse(
            ring_surface,
            (*ring_color, 40),
            (2, 2, ring_rx * 2, ring_ry * 2),
            width=6
        )

        screen.blit(
            ring_surface,
            (cx - ring_rx - 2, cy - ring_ry - 2)
        )

    light_dir_x = -0.4
    light_dir_y = -0.4

    steps = 18

    for i in range(steps, 0, -1):

        t = i / steps

        r = int(radius * t)

        offset = (1 - t) * radius * 0.35
        ox = int(cx + light_dir_x * offset)
        oy = int(cy + light_dir_y * offset)

        color_t = 1 - t
        color = lerp_color(base_color, light_color, color_t)

        pygame.draw.circle(screen, color, (ox, oy), r)

    rotation = time_s * planet["rot_speed"]

    texture_surface = pygame.Surface(
        (radius * 2, radius * 2),
        pygame.SRCALPHA
    )

    for lon, lat, size, alpha in planet["texture"]:

        cur_lon = lon + rotation

        cos_lat = math.cos(lat)
        px3 = cos_lat * math.cos(cur_lon)
        py3 = math.sin(lat)
        pz3 = cos_lat * math.sin(cur_lon)

        if pz3 <= 0:
            continue

        sx = radius + px3 * radius
        sy = radius + py3 * radius

        edge_factor = pz3

        r = max(1, int(size * radius))
        a = int(alpha * edge_factor)
        if a <= 0:
            continue

        tex_color = lerp_color(base_color, (0, 0, 0), 0.4)

        pygame.draw.circle(
            texture_surface,
            (*tex_color, a),
            (int(sx), int(sy)),
            r
        )

    mask_surface = pygame.Surface(
        (radius * 2, radius * 2),
        pygame.SRCALPHA
    )
    pygame.draw.circle(mask_surface, (255, 255, 255, 255), (radius, radius), radius)

    texture_surface.blit(
        mask_surface,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MIN
    )

    screen.blit(texture_surface, (cx - radius, cy - radius))

    if planet["ring"]:

        ring_color = planet["ring_color"]

        ring_rx = int(radius * 1.9)
        ring_ry = int(radius * 0.55)

        front_surface = pygame.Surface(
            (ring_rx * 2 + 4, ring_ry + 4),
            pygame.SRCALPHA
        )

        pygame.draw.arc(
            front_surface,
            (*ring_color, 110),
            (2, 2, ring_rx * 2, ring_ry * 2),
            math.pi,
            math.pi * 2,
            3
        )

        screen.blit(
            front_surface,
            (cx - ring_rx - 2, cy - 2)
        )

    glow_surface = pygame.Surface(
        (radius * 2 + 20, radius * 2 + 20),
        pygame.SRCALPHA
    )

    glow_center = radius + 10

    for i in range(4):

        glow_r = radius + 2 + i * 3
        a = max(0, 30 - i * 8)

        pygame.draw.circle(
            glow_surface,
            (*light_color, a),
            (glow_center, glow_center),
            glow_r,
            width=1
        )

    screen.blit(glow_surface, (cx - glow_center, cy - glow_center))


# ==================== 绘制星空 ====================

def draw_star_cross(ix, iy, color, brightness):

    arm_length = 6

    for offset in range(-arm_length, arm_length + 1):

        if offset == 0:
            continue

        rel = abs(offset) / arm_length

        a = int(120 * (1 - rel) ** 2 * brightness)
        if a <= 2:
            continue

        pygame.draw.circle(screen, (*color, a), (ix + offset, iy), 1)

    for offset in range(-arm_length, arm_length + 1):

        if offset == 0:
            continue

        rel = abs(offset) / arm_length

        a = int(120 * (1 - rel) ** 2 * brightness)
        if a <= 2:
            continue

        pygame.draw.circle(screen, (*color, a), (ix, iy + offset), 1)


def draw_starfield(time_s):

    screen.blit(starfield_surface, (0, 0))

    draw_planet(PLANET_SMALL, time_s)
    draw_planet(PLANET_LARGE, time_s)

    t = time_s

    for x, y, radius, base_brightness, phase, speed, flicker_amp, has_cross in stars:

        flicker = base_brightness + math.sin(phase + t * speed * 10) * flicker_amp
        flicker = max(0.15, min(1.0, flicker))

        color = (
            int(STAR_COLOR_DIM[0] + (STAR_COLOR_BRIGHT[0] - STAR_COLOR_DIM[0]) * flicker),
            int(STAR_COLOR_DIM[1] + (STAR_COLOR_BRIGHT[1] - STAR_COLOR_DIM[1]) * flicker),
            int(STAR_COLOR_DIM[2] + (STAR_COLOR_BRIGHT[2] - STAR_COLOR_DIM[2]) * flicker),
        )

        ix = int(x)
        iy = int(y)

        if has_cross:
            draw_star_cross(ix, iy, color, flicker)

        pygame.draw.circle(screen, color, (ix, iy), radius)


# ==================== 绘制按钮 ====================

def draw_button(text, rect):

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR

    pygame.draw.rect(screen, color, rect, border_radius=8)

    pygame.draw.rect(
        screen,
        BUTTON_BORDER_COLOR,
        rect,
        width=2,
        border_radius=8
    )

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center

    screen.blit(text_surface, text_rect)


# ==================== 绘制计时器 ====================

def draw_timer():

    timer_width = 130
    timer_height = 44
    timer_x = SCREEN_WIDTH - timer_width - 20
    timer_y = 10

    # 半透明淡黄底
    bg_surface = pygame.Surface(
        (timer_width, timer_height),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        bg_surface,
        (*TIMER_BG_COLOR, TIMER_BG_ALPHA),
        (0, 0, timer_width, timer_height),
        border_radius=10
    )

    screen.blit(bg_surface, (timer_x, timer_y))

    # 边框
    pygame.draw.rect(
        screen,
        TIMER_BORDER_COLOR,
        (timer_x, timer_y, timer_width, timer_height),
        width=2,
        border_radius=10
    )

    # 时间文字
    elapsed = get_elapsed_ms()
    time_str = format_time(elapsed)

    time_text = font.render(time_str, True, TIMER_TEXT_COLOR)
    time_rect = time_text.get_rect(center=(timer_x + timer_width // 2, timer_y + timer_height // 2))

    screen.blit(time_text, time_rect)


# ==================== 开始界面 ====================

def draw_start_screen():

    title = title_font.render("一箭又一箭", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 170))
    screen.blit(title, title_rect)

    subtitle = font.render(
        "点击火箭，让它们依次飞出棋盘",
        True,
        TEXT_DIM_COLOR
    )
    subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 240))
    screen.blit(subtitle, subtitle_rect)

    start_button = pygame.Rect(300, 320, 200, 60)
    draw_button("开始游戏", start_button)


# ==================== 游戏信息 ====================

def draw_game_info():

    level_text = font.render(f"第 {current_level + 1} 关", True, TEXT_COLOR)
    mistake_text = font.render(f"剩余机会：{mistakes}", True, TEXT_COLOR)
    arrow_text = font.render(f"剩余火箭：{len(arrows)}", True, TEXT_COLOR)

    screen.blit(level_text, (30, 14))
    screen.blit(mistake_text, (250, 14))
    screen.blit(arrow_text, (500, 14))


# ==================== 绘制棋盘 ====================

def draw_board():

    for i, alpha in enumerate([40, 70, 110]):

        glow_rect = pygame.Rect(
            BOARD_X - i * 3,
            BOARD_Y - i * 3,
            BOARD_SIZE + i * 6,
            BOARD_SIZE + i * 6
        )

        surface = pygame.Surface(
            (glow_rect.width, glow_rect.height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            surface,
            (*BOARD_GLOW_COLOR, alpha),
            (0, 0, glow_rect.width, glow_rect.height),
            width=2,
            border_radius=10
        )

        screen.blit(surface, (glow_rect.x, glow_rect.y))

    board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)

    pygame.draw.rect(
        screen,
        BOARD_BORDER_COLOR,
        board_rect,
        width=2,
        border_radius=6
    )

    grid_surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)

    for row in range(ROWS + 1):

        y = row * CELL_SIZE

        pygame.draw.line(
            grid_surface,
            (*BOARD_GRID_COLOR, 90),
            (0, y),
            (BOARD_SIZE, y),
            1
        )

    for col in range(COLS + 1):

        x = col * CELL_SIZE

        pygame.draw.line(
            grid_surface,
            (*BOARD_GRID_COLOR, 90),
            (x, 0),
            (x, BOARD_SIZE),
            1
        )

    screen.blit(grid_surface, (BOARD_X, BOARD_Y))


# ==================== 绘制火箭 ====================

def draw_rocket(x, y, direction, body_color, tip_color, fin_color,
                flame_length=0, hit=False):

    x = int(x)
    y = int(y)

    body = [
        (-16, -11), (-4, -13), (6, -12), (14, -7),
        (14, 7), (6, 12), (-4, 13), (-16, 11),
    ]

    body_shadow = [
        (-16, 3), (6, 4), (14, 3), (14, 7),
        (6, 12), (-4, 13), (-16, 11),
    ]

    tip = [(14, -7), (24, 0), (14, 7)]

    fin_top = [(-14, -10), (-22, -22), (-8, -12), (-4, -12)]
    fin_bottom = [(-14, 10), (-22, 22), (-8, 12), (-4, 12)]

    window_center = (-2, 0)
    window_radius = 4

    def transform(points):
        result = []
        for px, py in points:
            if direction == "right":
                rx, ry = px, py
            elif direction == "left":
                rx, ry = -px, -py
            elif direction == "down":
                rx, ry = -py, px
            else:
                rx, ry = py, -px
            result.append((x + rx, y + ry))
        return result

    def transform_point(px, py):
        if direction == "right":
            rx, ry = px, py
        elif direction == "left":
            rx, ry = -px, -py
        elif direction == "down":
            rx, ry = -py, px
        else:
            rx, ry = py, -px
        return x + rx, y + ry

    if flame_length > 0:

        flame_outer = [(-16, -9), (-16 - flame_length * 1.0, 0), (-16, 9)]
        flame_mid = [(-16, -6), (-16 - flame_length * 0.7, 0), (-16, 6)]
        flame_inner = [(-16, -3), (-16 - flame_length * 0.4, 0), (-16, 3)]

        pygame.draw.polygon(screen, FLAME_COLOR_OUTER, transform(flame_outer))
        pygame.draw.polygon(screen, FLAME_COLOR_MID, transform(flame_mid))
        pygame.draw.polygon(screen, FLAME_COLOR_INNER, transform(flame_inner))

    pygame.draw.polygon(screen, fin_color, transform(fin_top))
    pygame.draw.polygon(screen, fin_color, transform(fin_bottom))

    pygame.draw.polygon(screen, body_color, transform(body))

    shadow_color = lerp_color(body_color, (0, 0, 0), 0.25)
    pygame.draw.polygon(screen, shadow_color, transform(body_shadow))

    pygame.draw.polygon(screen, tip_color, transform(tip))

    wx, wy = transform_point(*window_center)

    pygame.draw.circle(screen, ROCKET_WINDOW_RIM, (int(wx), int(wy)), window_radius + 1)
    pygame.draw.circle(screen, ROCKET_WINDOW_COLOR, (int(wx), int(wy)), window_radius)


def draw_arrow(arrow, color=None):

    if arrow.x is None or arrow.y is None:
        return

    body_color = ROCKET_BODY_COLOR
    tip_color = ROCKET_TIP_COLOR
    fin_color = ROCKET_FIN_COLOR

    if color is not None:
        body_color = color
        tip_color = color
        fin_color = color

    if arrow.flying:
        flame_length = 22 + random.randint(-3, 3)
    else:
        flame_length = 10

    offset_x = 0
    if arrow.hit_timer > 0:
        offset_x = random.choice([-2, 2])

    draw_rocket(
        arrow.x + offset_x,
        arrow.y,
        arrow.direction,
        body_color,
        tip_color,
        fin_color,
        flame_length,
        hit=(arrow.hit_timer > 0)
    )


# ==================== 获取点击箭头 ====================

def get_clicked_arrow(pos):

    mouse_x, mouse_y = pos

    for arrow in arrows:

        if arrow.flying:
            continue

        distance_x = abs(mouse_x - arrow.x)
        distance_y = abs(mouse_y - arrow.y)

        if distance_x <= CELL_SIZE // 2:
            if distance_y <= CELL_SIZE // 2:
                return arrow

    return None


# ==================== 开始飞行动画 ====================

def start_flying(arrow):

    if arrow.flying:
        return

    arrow.flying = True

    if board.grid[arrow.row][arrow.col] is arrow:
        board.grid[arrow.row][arrow.col] = None


# ==================== 更新箭头动画 ====================

def update_arrow(arrow):

    if not arrow.flying:
        return

    speed = 12

    if arrow.direction == "right":
        arrow.x += speed
    elif arrow.direction == "left":
        arrow.x -= speed
    elif arrow.direction == "down":
        arrow.y += speed
    elif arrow.direction == "up":
        arrow.y -= speed

    if (
        arrow.x < -50
        or arrow.x > SCREEN_WIDTH + 50
        or arrow.y < -50
        or arrow.y > SCREEN_HEIGHT + 50
    ):
        if arrow in arrows:
            arrows.remove(arrow)


# ==================== 判断关卡是否完成 ====================

def is_level_complete():
    return len(arrows) == 0


# ==================== 失败界面 ====================

def draw_failed_screen():

    title = title_font.render("挑战失败", True, HIT_COLOR)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 180))
    screen.blit(title, title_rect)

    message = font.render("错误次数已经用完", True, TEXT_DIM_COLOR)
    message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, 240))
    screen.blit(message, message_rect)

    # 显示本关耗时
    elapsed = get_elapsed_ms()
    time_text = font.render(f"本关耗时：{format_time(elapsed)}", True, TEXT_DIM_COLOR)
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
    screen.blit(time_text, time_rect)

    restart_button = pygame.Rect(300, 340, 200, 60)
    draw_button("重新开始本关", restart_button)


# ==================== 胜利界面 ====================

def draw_won_screen():

    title = title_font.render("恭喜通关！", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 160))
    screen.blit(title, title_rect)

    if current_level < len(LEVELS) - 1:
        message = font.render("准备进入下一关", True, TEXT_DIM_COLOR)
    else:
        message = font.render("你已经完成所有关卡！", True, TEXT_DIM_COLOR)

    message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, 220))
    screen.blit(message, message_rect)

    # 显示本关耗时
    elapsed = get_elapsed_ms()
    time_text = font.render(f"本关耗时：{format_time(elapsed)}", True, TIMER_TEXT_COLOR)
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 270))
    screen.blit(time_text, time_rect)

    next_button = pygame.Rect(300, 330, 200, 60)

    if current_level < len(LEVELS) - 1:
        draw_button("下一关", next_button)
    else:
        draw_button("重新开始", next_button)


# ============================================================
#                       教程部分
# ============================================================

def create_tutorial_arrows():

    global tutorial_arrows

    tutorial_arrows = []

    positions = [(1, 1), (1, 3), (1, 5)]

    for row, col in positions:

        arrow = Arrow(row, col, "right")

        x, y = get_cell_center(row, col)
        arrow.set_position(x, y)

        tutorial_arrows.append(arrow)


def draw_tutorial_board():
    draw_board()


def draw_tutorial_success():

    title = large_font.render(
        "先看看火箭是怎么飞出去的",
        True,
        TEXT_COLOR
    )
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 20))
    screen.blit(title, title_rect)

    draw_board()

    x = tutorial_arrow_x
    y = BOARD_Y + 3 * CELL_SIZE + CELL_SIZE // 2

    draw_rocket(
        x, y, "right",
        ROCKET_BODY_COLOR,
        ROCKET_TIP_COLOR,
        ROCKET_FIN_COLOR,
        flame_length=22
    )

    if tutorial_timer < 120:
        message = "前方没有阻挡，可以飞出。"
    else:
        message = "看到没有？没有阻挡时，火箭就可以飞出去。"

    text = font.render(message, True, TEXT_DIM_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 582))
    screen.blit(text, text_rect)


def draw_tutorial_blocked():

    title = large_font.render(
        "再看看什么情况下不能飞出",
        True,
        TEXT_COLOR
    )
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 20))
    screen.blit(title, title_rect)

    draw_tutorial_board()

    y = BOARD_Y + 3 * CELL_SIZE + CELL_SIZE // 2

    first_x = BOARD_X + 2 * CELL_SIZE + CELL_SIZE // 2
    second_x = BOARD_X + 5 * CELL_SIZE + CELL_SIZE // 2

    first_arrow = Arrow(3, 2, "right")
    first_arrow.set_position(first_x, y)

    second_arrow = Arrow(3, 5, "right")
    second_arrow.set_position(second_x, y)

    draw_arrow(second_arrow)

    if tutorial_timer < 30:
        offset = -3
    elif tutorial_timer < 60:
        offset = 3
    else:
        offset = 0

    first_arrow.x += offset

    if tutorial_timer >= 60:
        draw_arrow(first_arrow, HIT_COLOR)
    else:
        draw_arrow(first_arrow)

    if tutorial_timer < 60:
        message = "前方有火箭阻挡，无法飞出。"
    else:
        message = "错误操作会消耗一次机会。"

    text = font.render(message, True, TEXT_DIM_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 582))
    screen.blit(text, text_rect)


def draw_tutorial_play():

    title = large_font.render("轮到你了", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 20))
    screen.blit(title, title_rect)

    draw_tutorial_board()

    for arrow in tutorial_arrows:

        if arrow.flying:
            continue

        if arrow.hit_timer > 0:
            draw_arrow(arrow, HIT_COLOR)
        else:
            draw_arrow(arrow)

    message = "试试看，哪个火箭可以先飞出去？"

    text = font.render(message, True, TEXT_DIM_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 582))
    screen.blit(text, text_rect)


def update_tutorial_success():

    global tutorial_timer
    global tutorial_arrow_x
    global game_state

    tutorial_timer += 1

    if tutorial_timer < 30:
        tutorial_arrow_x = BOARD_X + 2 * CELL_SIZE + CELL_SIZE // 2
    elif tutorial_timer < 100:
        tutorial_arrow_x += 8
    elif tutorial_timer < 150:
        pass
    else:
        tutorial_timer = 0
        game_state = "tutorial_blocked"


def update_tutorial_blocked():

    global tutorial_timer
    global game_state

    tutorial_timer += 1

    if tutorial_timer >= 150:
        tutorial_timer = 0
        create_tutorial_arrows()
        game_state = "tutorial_play"


def update_tutorial_play():

    global tutorial_arrows
    global tutorial_timer
    global game_state

    tutorial_timer += 1

    for arrow in tutorial_arrows:
        if arrow.hit_timer > 0:
            arrow.hit_timer -= 1

    for arrow in tutorial_arrows:

        if not arrow.flying:
            continue

        speed = 12

        if arrow.direction == "right":
            arrow.x += speed
        elif arrow.direction == "left":
            arrow.x -= speed
        elif arrow.direction == "down":
            arrow.y += speed
        elif arrow.direction == "up":
            arrow.y -= speed

    remaining = []

    for arrow in tutorial_arrows:

        if (
            arrow.x < -50
            or arrow.x > SCREEN_WIDTH + 50
            or arrow.y < -50
            or arrow.y > SCREEN_HEIGHT + 50
        ):
            continue

        remaining.append(arrow)

    tutorial_arrows = remaining

    if len(tutorial_arrows) == 0:
        game_state = "tutorial_complete"
        tutorial_timer = 0


def draw_tutorial_complete():

    title = title_font.render("教学完成！", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 170))
    screen.blit(title, title_rect)

    message = font.render("你已经掌握基本玩法。", True, TEXT_DIM_COLOR)
    message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, 240))
    screen.blit(message, message_rect)

    message2 = small_font.render(
        "接下来，试试真正的关卡吧！",
        True,
        TEXT_DIM_COLOR
    )
    message2_rect = message2.get_rect(center=(SCREEN_WIDTH // 2, 280))
    screen.blit(message2, message2_rect)

    start_button = pygame.Rect(300, 340, 200, 60)
    draw_button("开始第一关", start_button)


# ============================================================
#                       主程序
# ============================================================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = event.pos

            if game_state == "start":

                start_button = pygame.Rect(300, 320, 200, 60)

                if start_button.collidepoint(mouse_pos):
                    game_state = "tutorial_success"
                    tutorial_timer = 0
                    tutorial_arrow_x = BOARD_X + 2 * CELL_SIZE + CELL_SIZE // 2

            elif game_state == "tutorial_play":

                clicked_arrow = None

                for arrow in tutorial_arrows:

                    if arrow.flying:
                        continue

                    distance_x = abs(mouse_pos[0] - arrow.x)
                    distance_y = abs(mouse_pos[1] - arrow.y)

                    if (
                        distance_x <= CELL_SIZE // 2
                        and distance_y <= CELL_SIZE // 2
                    ):
                        clicked_arrow = arrow
                        break

                if clicked_arrow is not None:

                    temp_board = Board(ROWS, COLS)

                    for other in tutorial_arrows:
                        if other is not clicked_arrow:
                            temp_board.add_arrow(other)

                    if temp_board.can_exit(clicked_arrow):
                        clicked_arrow.flying = True
                    else:
                        clicked_arrow.hit_timer = 18

            elif game_state == "tutorial_complete":

                start_button = pygame.Rect(300, 340, 200, 60)

                if start_button.collidepoint(mouse_pos):
                    current_level = 0
                    load_level(current_level)
                    game_state = "playing"

            elif game_state == "playing":

                clicked_arrow = get_clicked_arrow(mouse_pos)

                if clicked_arrow is not None:

                    if board.can_exit(clicked_arrow):
                        start_flying(clicked_arrow)
                    else:
                        clicked_arrow.hit_timer = 18
                        mistakes -= 1

                        if mistakes <= 0:
                            stop_timer()
                            game_state = "failed"

            elif game_state == "failed":

                restart_button = pygame.Rect(300, 340, 200, 60)

                if restart_button.collidepoint(mouse_pos):
                    load_level(current_level)
                    game_state = "playing"

            elif game_state == "won":

                next_button = pygame.Rect(300, 330, 200, 60)

                if next_button.collidepoint(mouse_pos):

                    if current_level < len(LEVELS) - 1:
                        current_level += 1
                        load_level(current_level)
                        game_state = "playing"
                    else:
                        current_level = 0
                        load_level(current_level)
                        game_state = "playing"

    if game_state == "tutorial_success":
        update_tutorial_success()
    elif game_state == "tutorial_blocked":
        update_tutorial_blocked()
    elif game_state == "tutorial_play":
        update_tutorial_play()
    elif game_state == "playing":

        for arrow in arrows:
            update_arrow(arrow)

        for arrow in arrows:
            if arrow.hit_timer > 0:
                arrow.hit_timer -= 1

        if is_level_complete():
            stop_timer()
            game_state = "won"

    # ==================== 绘制 ====================

    time_s = pygame.time.get_ticks() / 1000.0

    screen.fill(BG_COLOR)

    draw_starfield(time_s)

    if game_state == "start":
        draw_start_screen()
    elif game_state == "tutorial_success":
        draw_tutorial_success()
    elif game_state == "tutorial_blocked":
        draw_tutorial_blocked()
    elif game_state == "tutorial_play":
        draw_tutorial_play()
    elif game_state == "tutorial_complete":
        draw_tutorial_complete()
    elif game_state == "playing":

        draw_game_info()
        draw_board()
        draw_timer()

        for arrow in arrows:
            if arrow.hit_timer > 0:
                draw_arrow(arrow, HIT_COLOR)
            else:
                draw_arrow(arrow)

    elif game_state == "failed":
        draw_failed_screen()
    elif game_state == "won":
        draw_won_screen()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()