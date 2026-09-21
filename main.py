import pygame

from game.arrow import Arrow
from game.board import Board


pygame.init()


# 游戏窗口
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("一箭又一箭")

clock = pygame.time.Clock()


# 棋盘参数
BOARD_SIZE = 480
ROWS = 8
COLS = 8
CELL_SIZE = BOARD_SIZE // COLS

BOARD_X = (WIDTH - BOARD_SIZE) // 2
BOARD_Y = (HEIGHT - BOARD_SIZE) // 2


# 创建棋盘
board = Board(ROWS, COLS)

# 创建测试箭头
arrow = Arrow(3, 3, "left")
board.add_arrow(arrow)


def get_cell_center(row, col):
    """根据棋盘行列计算格子中心位置"""

    x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

    return x, y


def draw_arrow(screen, arrow):
    """绘制一个箭头"""

    # 如果箭头还没有设置屏幕坐标，就根据棋盘位置计算
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

    # 点击是否在棋盘范围内
    if not (
        BOARD_X <= mouse_x < BOARD_X + BOARD_SIZE
        and BOARD_Y <= mouse_y < BOARD_Y + BOARD_SIZE
    ):
        return None

    # 将鼠标坐标转换成棋盘坐标
    col = (mouse_x - BOARD_X) // CELL_SIZE
    row = (mouse_y - BOARD_Y) // CELL_SIZE

    # 获取对应棋盘格
    return board.grid[row][col]


def start_flying(arrow):
    """开始箭头飞出动画"""

    # 获取箭头当前所在的格子中心
    x, y = get_cell_center(
        arrow.row,
        arrow.col
    )

    arrow.set_position(x, y)

    # 标记箭头正在飞出
    arrow.flying = True


def update_arrow(arrow):
    """更新箭头的飞行动画"""

    if not arrow.flying:
        return

    speed = 8

    # 根据方向移动
    if arrow.direction == "right":
        arrow.x += speed

    elif arrow.direction == "left":
        arrow.x -= speed

    elif arrow.direction == "down":
        arrow.y += speed

    elif arrow.direction == "up":
        arrow.y -= speed

    # 判断箭头是否已经飞出窗口
    if (
        arrow.x < -50
        or arrow.x > WIDTH + 50
        or arrow.y < -50
        or arrow.y > HEIGHT + 50
    ):
        # 从棋盘中删除
        board.grid[arrow.row][arrow.col] = None

        arrow.flying = False


running = True

while running:

    # 处理事件
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # 鼠标点击
        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            clicked_arrow = get_clicked_arrow(
                mouse_x,
                mouse_y
            )

            # 点击到了箭头，并且箭头没有正在飞
            if (
                clicked_arrow is not None
                and not clicked_arrow.flying
            ):

                # 判断是否可以出去
                if board.can_exit(clicked_arrow):

                    print("箭头可以出去！")

                    # 开始飞行动画
                    start_flying(clicked_arrow)

                else:

                    print("箭头被挡住了！")

    # 更新箭头位置
    update_arrow(arrow)

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

    # 箭头没有飞出时才绘制
    if arrow.flying or board.grid[arrow.row][arrow.col] is not None:
        draw_arrow(screen, arrow)

    # 更新画面
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)


pygame.quit()