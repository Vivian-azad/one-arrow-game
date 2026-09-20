from game.arrow import Arrow
from game.board import Board


def test_right():
    board = Board(5, 5)

    arrow = Arrow(2, 2, "right")
    board.add_arrow(arrow)

    print("→ 无障碍：", board.can_exit(arrow))

    blocker = Arrow(2, 4, "up")
    board.add_arrow(blocker)

    print("→ 有障碍：", board.can_exit(arrow))


def test_left():
    board = Board(5, 5)

    arrow = Arrow(2, 2, "left")
    board.add_arrow(arrow)

    print("← 无障碍：", board.can_exit(arrow))

    blocker = Arrow(2, 0, "up")
    board.add_arrow(blocker)

    print("← 有障碍：", board.can_exit(arrow))


def test_down():
    board = Board(5, 5)

    arrow = Arrow(2, 2, "down")
    board.add_arrow(arrow)

    print("↓ 无障碍：", board.can_exit(arrow))

    blocker = Arrow(4, 2, "left")
    board.add_arrow(blocker)

    print("↓ 有障碍：", board.can_exit(arrow))


def test_up():
    board = Board(5, 5)

    arrow = Arrow(2, 2, "up")
    board.add_arrow(arrow)

    print("↑ 无障碍：", board.can_exit(arrow))

    blocker = Arrow(0, 2, "right")
    board.add_arrow(blocker)

    print("↑ 有障碍：", board.can_exit(arrow))


test_right()
test_left()
test_down()
test_up()

def test_boundary():
    board = Board(5, 5)

    right_arrow = Arrow(2, 4, "right")
    left_arrow = Arrow(2, 0, "left")
    down_arrow = Arrow(4, 2, "down")
    up_arrow = Arrow(0, 2, "up")

    board.add_arrow(right_arrow)
    board.add_arrow(left_arrow)
    board.add_arrow(down_arrow)
    board.add_arrow(up_arrow)

    print("→ 边界：", board.can_exit(right_arrow))
    print("← 边界：", board.can_exit(left_arrow))
    print("↓ 边界：", board.can_exit(down_arrow))
    print("↑ 边界：", board.can_exit(up_arrow))


test_boundary()