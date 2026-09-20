from game.arrow import Arrow


class Board:
    """表示游戏棋盘"""

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # None 表示这个格子没有箭头
        self.grid = [
            [None for _ in range(cols)]
            for _ in range(rows)
        ]

    def add_arrow(self, arrow):
        """向棋盘中添加一个箭头"""
        self.grid[arrow.row][arrow.col] = arrow

    def can_exit(self, arrow):
        """判断箭头前方是否有其他箭头"""

        row = arrow.row
        col = arrow.col

        if arrow.direction == "right":
            for c in range(col + 1, self.cols):
                if self.grid[row][c] is not None:
                    return False

        elif arrow.direction == "left":
            for c in range(col - 1, -1, -1):
                if self.grid[row][c] is not None:
                    return False

        elif arrow.direction == "down":
            for r in range(row + 1, self.rows):
                if self.grid[r][col] is not None:
                    return False

        elif arrow.direction == "up":
            for r in range(row - 1, -1, -1):
                if self.grid[r][col] is not None:
                    return False

        return True