class Arrow:
    """表示棋盘上的一个箭头"""

    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction