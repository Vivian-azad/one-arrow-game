class Arrow:
    """表示棋盘上的一个箭头"""

    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction

        # 动画时使用的屏幕坐标
        self.x = None
        self.y = None

        # 是否正在飞出
        self.flying = False

        # 碰撞反馈计时器
        self.hit_timer = 0

    def set_position(self, x, y):
        """设置箭头在屏幕上的位置"""

        self.x = x
        self.y = y