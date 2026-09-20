from game.arrow import Arrow


class Board:
    """表示游戏棋盘"""

    DIRECTIONS = {
        "right": (0, 1),
        "left": (0, -1),
        "down": (1, 0),
        "up": (-1, 0)
    }

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.grid = [
            [None for _ in range(cols)]
            for _ in range(rows)
        ]

    def add_arrow(self, arrow):
        """向棋盘中添加一个箭头"""
        self.grid[arrow.row][arrow.col] = arrow

    def can_exit(self, arrow):
        """判断箭头前方是否有其他箭头"""

        row_step, col_step = self.DIRECTIONS[arrow.direction]

        row = arrow.row + row_step
        col = arrow.col + col_step

        while 0 <= row < self.rows and 0 <= col < self.cols:
            if self.grid[row][col] is not None:
                return False

            row += row_step
            col += col_step

        return True