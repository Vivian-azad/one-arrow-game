import pygame

from game.arrow import Arrow
from game.board import Board
from levels.levels import LEVELS


pygame.init()


# 游戏窗口
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("一箭又一箭")

clock = pygame.time.Clock()


# 游戏界面字体
font = pygame.font.Font(
    "C:/Windows/Fonts/msyh.ttc",
    32
)


# 棋盘参数
BOARD_SIZE = 480
ROWS = 8
COLS = 8
CELL_SIZE = BOARD_SIZE // COLS

BOARD_X = (WIDTH - BOARD_SIZE) // 2
BOARD_Y = (HEIGHT - BOARD_SIZE) // 2


# 当前关卡
current_level = 0

# 每一关允许的失误次数
MAX_MISTAKES = 3
mistakes = MAX_MISTAKES

# 游戏状态
game_state = "playing"


# 创建棋盘
board = Board(ROWS, COLS)

# 保存当前关卡的所有箭头
arrows = []


def load_level(level_index):
    """加载指定关卡"""

    global board, arrows, mistakes

    board = Board(ROWS, COLS)
    arrows = []
    mistakes = MAX_MISTAKES

    level_data = LEVELS[level_index]

    for row, col, direction in level_data:

        arrow = Arrow(
            row,
            col,
            direction
        )

        board.add_arrow(arrow)
        arrows.append(arrow)


def get_cell_center(row, col):
    """根据棋盘行列计算格子中心位置"""

    x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

    return x, y


def draw_game_info():
    """绘制当前关卡和游戏状态"""

    level_text = font.render(
        f"第 {current_level + 1} 关",
        True,
        (40, 40, 40)
    )

    arrow_count = sum(
        1
        for arrow in arrows
        if board.grid[arrow.row][arrow.col] is not None
    )

    arrow_text = font.render(
        f"剩余箭头：{arrow_count}",
        True,
        (40, 40, 40)
    )

    mistake_text = font.render(
        f"剩余失误：{mistakes}",
        True,
        (40, 40, 40)
    )

    screen.blit(level_text, (40, 40))
    screen.blit(arrow_text, (40, 80))
    screen.blit(mistake_text, (40, 120))


def draw_failed_screen():
    """绘制失败界面"""

    title = font.render(
        "游戏失败",
        True,
        (180, 50, 50)
    )

    message = font.render(
        "失误次数已经用完",
        True,
        (40, 40, 40)
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            170
        )
    )

    screen.blit(
        message,
        (
            WIDTH // 2 - message.get_width() // 2,
            230
        )
    )

    # 重新开始按钮
    button_rect = pygame.Rect(
        WIDTH // 2 - 100,
        300,
        200,
        60
    )

    pygame.draw.rect(
        screen,
        (80, 120, 200),
        button_rect,
        border_radius=10
    )

    button_text = font.render(
        "重新开始",
        True,
        (255, 255, 255)
    )

    screen.blit(
        button_text,
        (
            WIDTH // 2 - button_text.get_width() // 2,
            310
        )
    )


def draw_arrow(screen, arrow):
    """绘制一个箭头"""

    if arrow.x is None or arrow.y is None:

        center_x, center_y = get_cell_center(
            arrow.row,
            arrow.col
        )

    else:

        center_x = arrow.x
        center_y = arrow.y

    color = (40, 40, 40)

    # 向右
    if arrow.direction == "right":

        pygame.draw.line(
            screen,
            color,
            (center_x - 20, center_y),
            (center_x + 20, center_y),
            6
        )

        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x + 25, center_y),
                (center_x + 10, center_y - 12),
                (center_x + 10, center_y + 12)
            ]
        )

    # 向左
    elif arrow.direction == "left":

        pygame.draw.line(
            screen,
            color,
            (center_x + 20, center_y),
            (center_x - 20, center_y),
            6
        )

        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x - 25, center_y),
                (center_x - 10, center_y - 12),
                (center_x - 10, center_y + 12)
            ]
        )

    # 向下
    elif arrow.direction == "down":

        pygame.draw.line(
            screen,
            color,
            (center_x, center_y - 20),
            (center_x, center_y + 20),
            6
        )

        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x, center_y + 25),
                (center_x - 12, center_y + 10),
                (center_x + 12, center_y + 10)
            ]
        )

    # 向上
    elif arrow.direction == "up":

        pygame.draw.line(
            screen,
            color,
            (center_x, center_y + 20),
            (center_x, center_y - 20),
            6
        )

        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x, center_y - 25),
                (center_x - 12, center_y - 10),
                (center_x + 12, center_y - 10)
            ]
        )


def get_clicked_arrow(mouse_x, mouse_y):
    """根据鼠标位置找到被点击的箭头"""

    if not (
        BOARD_X <= mouse_x < BOARD_X + BOARD_SIZE
        and BOARD_Y <= mouse_y < BOARD_Y + BOARD_SIZE
    ):
        return None

    col = (mouse_x - BOARD_X) // CELL_SIZE
    row = (mouse_y - BOARD_Y) // CELL_SIZE

    return board.grid[row][col]


def start_flying(arrow):
    """开始箭头飞出动画"""

    x, y = get_cell_center(
        arrow.row,
        arrow.col
    )

    arrow.set_position(x, y)
    arrow.flying = True


def update_arrow(arrow):
    """更新箭头的飞行动画"""

    if not arrow.flying:
        return

    speed = 8

    if arrow.direction == "right":
        arrow.x += speed

    elif arrow.direction == "left":
        arrow.x -= speed

    elif arrow.direction == "down":
        arrow.y += speed

    elif arrow.direction == "up":
        arrow.y -= speed

    # 箭头飞出窗口
    if (
        arrow.x < -50
        or arrow.x > WIDTH + 50
        or arrow.y < -50
        or arrow.y > HEIGHT + 50
    ):

        board.grid[arrow.row][arrow.col] = None
        arrow.flying = False


def is_level_complete():
    """判断当前关卡是否已经清空"""

    for arrow in arrows:

        if arrow.flying:
            return False

        if board.grid[arrow.row][arrow.col] is not None:
            return False

    return True


# 加载第一关
load_level(current_level)


running = True

while running:

    # 处理事件
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            # 失败状态下点击重新开始按钮
            if game_state == "failed":

                button_rect = pygame.Rect(
                    WIDTH // 2 - 100,
                    300,
                    200,
                    60
                )

                if button_rect.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    load_level(current_level)
                    game_state = "playing"

                continue

            # 非游戏状态下不处理其他点击
            if game_state != "playing":
                continue

            clicked_arrow = get_clicked_arrow(
                mouse_x,
                mouse_y
            )

            if (
                clicked_arrow is not None
                and not clicked_arrow.flying
            ):

                if board.can_exit(clicked_arrow):

                    print(
                        "箭头可以出去：",
                        clicked_arrow.direction
                    )

                    start_flying(clicked_arrow)

                else:

                    mistakes -= 1

                    print(
                        "箭头被挡住：",
                        clicked_arrow.direction
                    )

                    print(
                        "剩余失误次数：",
                        mistakes
                    )

                    if mistakes <= 0:

                        game_state = "failed"

                        print("游戏失败！")

    # 只有游戏进行中才更新箭头
    if game_state == "playing":

        for arrow in arrows:
            update_arrow(arrow)

    # 判断关卡是否完成
    if (
        game_state == "playing"
        and is_level_complete()
    ):

        # 还有下一关
        if current_level < len(LEVELS) - 1:

            current_level += 1

            print(
                "进入第",
                current_level + 1,
                "关"
            )

            load_level(current_level)

        # 所有关卡完成
        else:

            print("所有关卡完成！")

            game_state = "won"

    # 绘制背景
    screen.fill((240, 240, 240))

    # 绘制棋盘
    for row in range(ROWS):
        for col in range(COLS):

            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + row * CELL_SIZE

            pygame.draw.rect(
                screen,
                (220, 220, 220),
                (x, y, CELL_SIZE, CELL_SIZE),
                1
            )

    # 绘制所有箭头
    for arrow in arrows:

        if (
            arrow.flying
            or board.grid[arrow.row][arrow.col] is not None
        ):
            draw_arrow(screen, arrow)

    # 绘制游戏信息
    if game_state == "playing":

        draw_game_info()

    elif game_state == "failed":

        draw_failed_screen()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()