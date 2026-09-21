"""
editor: Lai Yanran
date: 2026-09-21
task: 一箭又一箭
"""

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
BOARD_Y = 70


# ==================== 颜色 ====================

BG_COLOR = (245, 245, 245)
BOARD_COLOR = (225, 225, 225)
GRID_COLOR = (190, 190, 190)

ARROW_COLOR = (60, 60, 60)
FLY_COLOR = (80, 130, 220)
HIT_COLOR = (220, 70, 70)

TEXT_COLOR = (40, 40, 40)

BUTTON_COLOR = (70, 120, 200)
BUTTON_HOVER_COLOR = (90, 140, 220)

WHITE = (255, 255, 255)


# ==================== 字体 ====================

font_path = "C:/Windows/Fonts/msyh.ttc"

title_font = pygame.font.Font(font_path, 42)
large_font = pygame.font.Font(font_path, 32)
font = pygame.font.Font(font_path, 24)
small_font = pygame.font.Font(font_path, 20)


# ==================== 游戏变量 ====================

# 游戏状态
#
# start
# tutorial_success
# tutorial_blocked
# tutorial_play
# tutorial_complete
# playing
# failed
# won

game_state = "start"

current_level = 0

board = None
arrows = []

mistakes = 3


# ==================== 教程变量 ====================

# 成功演示中的箭头位置
tutorial_timer = 0

tutorial_arrow_x = 0

# 教学试玩中的箭头
tutorial_arrows = []


# ==================== 基本函数 ====================

def load_level(level_index):
    """加载正式关卡"""

    global board
    global arrows
    global mistakes

    board = Board(ROWS, COLS)

    arrows = []

    for row, col, direction in LEVELS[level_index]:

        arrow = Arrow(
            row,
            col,
            direction
        )

        board.add_arrow(arrow)

        arrows.append(arrow)

    mistakes = 3

    for arrow in arrows:

        x, y = get_cell_center(
            arrow.row,
            arrow.col
        )

        arrow.set_position(x, y)


def get_cell_center(row, col):
    """获取棋盘格中心坐标"""

    x = (
        BOARD_X
        + col * CELL_SIZE
        + CELL_SIZE // 2
    )

    y = (
        BOARD_Y
        + row * CELL_SIZE
        + CELL_SIZE // 2
    )

    return x, y


# ==================== 绘制按钮 ====================

def draw_button(text, rect):
    """绘制按钮"""

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=8
    )

    text_surface = font.render(
        text,
        True,
        WHITE
    )

    text_rect = text_surface.get_rect()

    text_rect.center = rect.center

    screen.blit(
        text_surface,
        text_rect
    )


# ==================== 开始界面 ====================

def draw_start_screen():
    """绘制开始界面"""

    screen.fill(BG_COLOR)

    title = title_font.render(
        "一箭又一箭",
        True,
        TEXT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            170
        )
    )

    screen.blit(
        title,
        title_rect
    )

    subtitle = font.render(
        "点击箭头，让它们依次飞出棋盘",
        True,
        TEXT_COLOR
    )

    subtitle_rect = subtitle.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            240
        )
    )

    screen.blit(
        subtitle,
        subtitle_rect
    )

    start_button = pygame.Rect(
        300,
        320,
        200,
        60
    )

    draw_button(
        "开始游戏",
        start_button
    )


# ==================== 游戏信息 ====================

def draw_game_info():
    """绘制正式游戏中的信息"""

    level_text = font.render(
        f"第 {current_level + 1} 关",
        True,
        TEXT_COLOR
    )

    mistake_text = font.render(
        f"剩余机会：{mistakes}",
        True,
        TEXT_COLOR
    )

    arrow_text = font.render(
        f"剩余箭头：{len(arrows)}",
        True,
        TEXT_COLOR
    )

    screen.blit(
        level_text,
        (30, 20)
    )

    screen.blit(
        mistake_text,
        (250, 20)
    )

    screen.blit(
        arrow_text,
        (500, 20)
    )


# ==================== 绘制棋盘 ====================

def draw_board():
    """绘制棋盘"""

    board_rect = pygame.Rect(
        BOARD_X,
        BOARD_Y,
        BOARD_SIZE,
        BOARD_SIZE
    )

    pygame.draw.rect(
        screen,
        BOARD_COLOR,
        board_rect
    )

    # 横线
    for row in range(ROWS + 1):

        y = BOARD_Y + row * CELL_SIZE

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (BOARD_X, y),
            (
                BOARD_X + BOARD_SIZE,
                y
            ),
            1
        )

    # 竖线
    for col in range(COLS + 1):

        x = BOARD_X + col * CELL_SIZE

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, BOARD_Y),
            (
                x,
                BOARD_Y + BOARD_SIZE
            ),
            1
        )


# ==================== 绘制箭头 ====================

def draw_arrow(arrow, color=None):
    """绘制一个箭头"""

    if color is None:
        color = ARROW_COLOR

    if arrow.x is None or arrow.y is None:
        return

    x = int(arrow.x)
    y = int(arrow.y)

    if arrow.direction == "right":

        points = [
            (x - 20, y - 12),
            (x + 5, y - 12),
            (x + 5, y - 22),
            (x + 24, y),
            (x + 5, y + 22),
            (x + 5, y + 12),
            (x - 20, y + 12)
        ]

    elif arrow.direction == "left":

        points = [
            (x + 20, y - 12),
            (x - 5, y - 12),
            (x - 5, y - 22),
            (x - 24, y),
            (x - 5, y + 22),
            (x - 5, y + 12),
            (x + 20, y + 12)
        ]

    elif arrow.direction == "down":

        points = [
            (x - 12, y - 20),
            (x - 12, y + 5),
            (x - 22, y + 5),
            (x, y + 24),
            (x + 22, y + 5),
            (x + 12, y + 5),
            (x + 12, y - 20)
        ]

    else:

        points = [
            (x - 12, y + 20),
            (x - 12, y - 5),
            (x - 22, y - 5),
            (x, y - 24),
            (x + 22, y - 5),
            (x + 12, y - 5),
            (x + 12, y + 20)
        ]

    pygame.draw.polygon(
        screen,
        color,
        points
    )


# ==================== 获取点击箭头 ====================

def get_clicked_arrow(pos):
    """判断鼠标点击的是哪个箭头"""

    mouse_x, mouse_y = pos

    for arrow in arrows:

        if arrow.flying:
            continue

        distance_x = abs(
            mouse_x - arrow.x
        )

        distance_y = abs(
            mouse_y - arrow.y
        )

        if distance_x <= CELL_SIZE // 2:

            if distance_y <= CELL_SIZE // 2:
                return arrow

    return None


# ==================== 开始飞行动画 ====================

def start_flying(arrow):
    """让箭头开始飞出"""

    arrow.flying = True


# ==================== 更新箭头动画 ====================

def update_arrow(arrow):
    """更新箭头飞行动画"""

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

    # 判断箭头是否飞出屏幕
    if (
        arrow.x < -50
        or arrow.x > SCREEN_WIDTH + 50
        or arrow.y < -50
        or arrow.y > SCREEN_HEIGHT + 50
    ):

        if arrow in arrows:
            arrows.remove(arrow)

            if board.grid[arrow.row][arrow.col] is arrow:
                board.grid[arrow.row][arrow.col] = None


# ==================== 判断关卡是否完成 ====================

def is_level_complete():
    """判断当前关卡是否完成"""

    return len(arrows) == 0


# ==================== 失败界面 ====================

def draw_failed_screen():
    """绘制失败界面"""

    screen.fill(BG_COLOR)

    title = title_font.render(
        "挑战失败",
        True,
        HIT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            180
        )
    )

    screen.blit(
        title,
        title_rect
    )

    message = font.render(
        "错误次数已经用完",
        True,
        TEXT_COLOR
    )

    message_rect = message.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            250
        )
    )

    screen.blit(
        message,
        message_rect
    )

    restart_button = pygame.Rect(
        300,
        330,
        200,
        60
    )

    draw_button(
        "重新开始本关",
        restart_button
    )


# ==================== 胜利界面 ====================

def draw_won_screen():
    """绘制通关界面"""

    screen.fill(BG_COLOR)

    title = title_font.render(
        "恭喜通关！",
        True,
        TEXT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            170
        )
    )

    screen.blit(
        title,
        title_rect
    )

    if current_level < len(LEVELS) - 1:

        message = font.render(
            "准备进入下一关",
            True,
            TEXT_COLOR
        )

    else:

        message = font.render(
            "你已经完成所有关卡！",
            True,
            TEXT_COLOR
        )

    message_rect = message.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            240
        )
    )

    screen.blit(
        message,
        message_rect
    )

    next_button = pygame.Rect(
        300,
        330,
        200,
        60
    )

    if current_level < len(LEVELS) - 1:

        draw_button(
            "下一关",
            next_button
        )

    else:

        draw_button(
            "重新开始",
            next_button
        )


# ============================================================
#                       教程部分
# ============================================================

def create_tutorial_arrows():
    """创建教学试玩中的三个箭头"""

    global tutorial_arrows

    tutorial_arrows = []

    # 三个箭头从左到右排列
    #
    # 玩家需要自己发现：
    # 最右边的箭头可以先飞出去

    positions = [
        (1, 1),
        (1, 3),
        (1, 5)
    ]

    for row, col in positions:

        arrow = Arrow(
            row,
            col,
            "right"
        )

        x, y = get_cell_center(
            row,
            col
        )

        arrow.set_position(
            x,
            y
        )

        tutorial_arrows.append(
            arrow
        )


def draw_tutorial_board():
    """绘制教程棋盘"""

    draw_board()


# ==================== 成功演示 ====================

def draw_tutorial_success():
    """绘制成功飞出动画"""

    screen.fill(BG_COLOR)

    title = large_font.render(
        "先看看箭头是怎么飞出去的",
        True,
        TEXT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            35
        )
    )

    screen.blit(
        title,
        title_rect
    )

    # 棋盘
    pygame.draw.rect(
        screen,
        BOARD_COLOR,
        (
            BOARD_X,
            BOARD_Y,
            BOARD_SIZE,
            BOARD_SIZE
        )
    )

    # 横线
    for row in range(ROWS + 1):

        y = BOARD_Y + row * CELL_SIZE

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (BOARD_X, y),
            (
                BOARD_X + BOARD_SIZE,
                y
            )
        )

    # 竖线
    for col in range(COLS + 1):

        x = BOARD_X + col * CELL_SIZE

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, BOARD_Y),
            (
                x,
                BOARD_Y + BOARD_SIZE
            )
        )

    # 教程箭头
    x = tutorial_arrow_x

    y = (
        BOARD_Y
        + 3 * CELL_SIZE
        + CELL_SIZE // 2
    )

    pygame.draw.polygon(
        screen,
        FLY_COLOR,
        [
            (x - 30, y - 12),
            (x + 5, y - 12),
            (x + 5, y - 23),
            (x + 28, y),
            (x + 5, y + 23),
            (x + 5, y + 12),
            (x - 30, y + 12)
        ]
    )

    if tutorial_timer < 120:

        message = "前方没有阻挡，可以飞出。"

    else:

        message = "看到没有？没有阻挡时，箭头就可以飞出去。"

    text = font.render(
        message,
        True,
        TEXT_COLOR
    )

    text_rect = text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            555
        )
    )

    screen.blit(
        text,
        text_rect
    )


# ==================== 阻挡演示 ====================

def draw_tutorial_blocked():
    """绘制被阻挡的演示"""

    screen.fill(BG_COLOR)

    title = large_font.render(
        "再看看什么情况下不能飞出",
        True,
        TEXT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            35
        )
    )

    screen.blit(
        title,
        title_rect
    )

    draw_tutorial_board()

    y = (
        BOARD_Y
        + 3 * CELL_SIZE
        + CELL_SIZE // 2
    )

    first_x = (
        BOARD_X
        + 2 * CELL_SIZE
        + CELL_SIZE // 2
    )

    second_x = (
        BOARD_X
        + 5 * CELL_SIZE
        + CELL_SIZE // 2
    )

    first_arrow = Arrow(
        3,
        2,
        "right"
    )

    first_arrow.set_position(
        first_x,
        y
    )

    second_arrow = Arrow(
        3,
        5,
        "right"
    )

    second_arrow.set_position(
        second_x,
        y
    )

    draw_arrow(
        second_arrow
    )

    # 前面的箭头轻微晃动
    if tutorial_timer < 30:

        offset = -3

    elif tutorial_timer < 60:

        offset = 3

    else:

        offset = 0

    first_arrow.x += offset

    if tutorial_timer >= 60:

        draw_arrow(
            first_arrow,
            HIT_COLOR
        )

    else:

        draw_arrow(
            first_arrow
        )

    if tutorial_timer < 60:

        message = "前方有箭头阻挡，无法飞出。"

    else:

        message = "错误操作会消耗一次机会。"

    text = font.render(
        message,
        True,
        TEXT_COLOR
    )

    text_rect = text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            555
        )
    )

    screen.blit(
        text,
        text_rect
    )


# ==================== 教学试玩 ====================

def draw_tutorial_play():
    """绘制教学试玩"""

    screen.fill(BG_COLOR)

    title = large_font.render(
        "轮到你了",
        True,
        TEXT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            35
        )
    )

    screen.blit(
        title,
        title_rect
    )

    draw_tutorial_board()

    for arrow in tutorial_arrows:

        if arrow.flying:
            continue

        if arrow.hit_timer > 0:

            draw_arrow(
                arrow,
                HIT_COLOR
            )

        else:

            draw_arrow(
                arrow
            )

    message = "试试看，哪个箭头可以先飞出去？"

    text = font.render(
        message,
        True,
        TEXT_COLOR
    )

    text_rect = text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            555
        )
    )

    screen.blit(
        text,
        text_rect
    )


# ==================== 更新成功演示 ====================

def update_tutorial_success():
    """更新成功演示"""

    global tutorial_timer
    global tutorial_arrow_x
    global game_state

    tutorial_timer += 1

    if tutorial_timer < 30:

        tutorial_arrow_x = (
            BOARD_X
            + 2 * CELL_SIZE
            + CELL_SIZE // 2
        )

    elif tutorial_timer < 100:

        tutorial_arrow_x += 8

    elif tutorial_timer < 150:

        pass

    else:

        tutorial_timer = 0

        game_state = "tutorial_blocked"


# ==================== 更新阻挡演示 ====================

def update_tutorial_blocked():
    """更新阻挡演示"""

    global tutorial_timer
    global game_state

    tutorial_timer += 1

    if tutorial_timer >= 150:

        tutorial_timer = 0

        create_tutorial_arrows()

        game_state = "tutorial_play"


# ==================== 更新教学试玩 ====================

def update_tutorial_play():
    """更新教学试玩"""

    global tutorial_arrows
    global tutorial_timer
    global game_state

    tutorial_timer += 1

    # 更新碰撞反馈
    for arrow in tutorial_arrows:

        if arrow.hit_timer > 0:
            arrow.hit_timer -= 1

    # 更新飞行动画
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

    # 删除飞出棋盘的箭头
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

    # 全部飞出
    if len(tutorial_arrows) == 0:

        game_state = "tutorial_complete"

        tutorial_timer = 0


# ==================== 教学完成界面 ====================

def draw_tutorial_complete():
    """绘制教学完成界面"""

    screen.fill(BG_COLOR)

    title = title_font.render(
        "教学完成！",
        True,
        TEXT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            170
        )
    )

    screen.blit(
        title,
        title_rect
    )

    message = font.render(
        "你已经掌握基本玩法。",
        True,
        TEXT_COLOR
    )

    message_rect = message.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            240
        )
    )

    screen.blit(
        message,
        message_rect
    )

    message2 = small_font.render(
        "接下来，试试真正的关卡吧！",
        True,
        TEXT_COLOR
    )

    message2_rect = message2.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            280
        )
    )

    screen.blit(
        message2,
        message2_rect
    )

    start_button = pygame.Rect(
        300,
        340,
        200,
        60
    )

    draw_button(
        "开始第一关",
        start_button
    )


# ============================================================
#                       主程序
# ============================================================

running = True

while running:

    # ==================== 事件处理 ====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = event.pos

            # ==================== 开始界面 ====================

            if game_state == "start":

                start_button = pygame.Rect(
                    300,
                    320,
                    200,
                    60
                )

                if start_button.collidepoint(
                    mouse_pos
                ):

                    game_state = "tutorial_success"

                    tutorial_timer = 0

                    tutorial_arrow_x = (
                        BOARD_X
                        + 2 * CELL_SIZE
                        + CELL_SIZE // 2
                    )

            # ==================== 教学试玩 ====================

            elif game_state == "tutorial_play":

                clicked_arrow = None

                for arrow in tutorial_arrows:

                    if arrow.flying:
                        continue

                    distance_x = abs(
                        mouse_pos[0] - arrow.x
                    )

                    distance_y = abs(
                        mouse_pos[1] - arrow.y
                    )

                    if (
                        distance_x <= CELL_SIZE // 2
                        and distance_y <= CELL_SIZE // 2
                    ):

                        clicked_arrow = arrow
                        break

                if clicked_arrow is not None:

                    # 临时创建棋盘
                    # 只用于判断教学阶段的阻挡关系

                    temp_board = Board(
                        ROWS,
                        COLS
                    )

                    for other in tutorial_arrows:

                        if other is not clicked_arrow:

                            temp_board.add_arrow(
                                other
                            )

                    if temp_board.can_exit(
                        clicked_arrow
                    ):

                        clicked_arrow.flying = True

                    else:

                        # 教学阶段不扣机会
                        clicked_arrow.hit_timer = 18

            # ==================== 教学完成 ====================

            elif game_state == "tutorial_complete":

                start_button = pygame.Rect(
                    300,
                    340,
                    200,
                    60
                )

                if start_button.collidepoint(
                    mouse_pos
                ):

                    current_level = 0

                    load_level(
                        current_level
                    )

                    game_state = "playing"

            # ==================== 正式游戏 ====================

            elif game_state == "playing":

                clicked_arrow = get_clicked_arrow(
                    mouse_pos
                )

                if clicked_arrow is not None:

                    if board.can_exit(
                        clicked_arrow
                    ):

                        start_flying(
                            clicked_arrow
                        )

                    else:

                        clicked_arrow.hit_timer = 18

                        mistakes -= 1

                        if mistakes <= 0:

                            game_state = "failed"

            # ==================== 失败界面 ====================

            elif game_state == "failed":

                restart_button = pygame.Rect(
                    300,
                    330,
                    200,
                    60
                )

                if restart_button.collidepoint(
                    mouse_pos
                ):

                    load_level(
                        current_level
                    )

                    game_state = "playing"

            # ==================== 通关界面 ====================

            elif game_state == "won":

                next_button = pygame.Rect(
                    300,
                    330,
                    200,
                    60
                )

                if next_button.collidepoint(
                    mouse_pos
                ):

                    if current_level < len(LEVELS) - 1:

                        current_level += 1

                        load_level(
                            current_level
                        )

                        game_state = "playing"

                    else:

                        current_level = 0

                        load_level(
                            current_level
                        )

                        game_state = "playing"

    # ==================== 更新 ====================

    if game_state == "tutorial_success":

        update_tutorial_success()

    elif game_state == "tutorial_blocked":

        update_tutorial_blocked()

    elif game_state == "tutorial_play":

        update_tutorial_play()

    elif game_state == "playing":

        # 更新飞行中的箭头
        for arrow in arrows:

            update_arrow(
                arrow
            )

        # 更新碰撞反馈
        for arrow in arrows:

            if arrow.hit_timer > 0:

                arrow.hit_timer -= 1

        # 判断关卡是否完成
        if is_level_complete():

            game_state = "won"

    # ==================== 绘制 ====================

    screen.fill(BG_COLOR)

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

        for arrow in arrows:

            if arrow.hit_timer > 0:

                draw_arrow(
                    arrow,
                    HIT_COLOR
                )

            else:

                draw_arrow(
                    arrow
                )

    elif game_state == "failed":

        draw_failed_screen()

    elif game_state == "won":

        draw_won_screen()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()