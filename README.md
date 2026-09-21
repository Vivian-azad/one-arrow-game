# 一箭又一箭（One Arrow Game）

一款使用 **Python + Pygame** 开发的点击式箭头解谜小游戏。

玩家需要观察箭头的方向和相互阻挡关系，按照合适的顺序点击箭头，让所有箭头依次飞出棋盘。游戏使用深蓝宇宙星空主题，箭头以**小火箭**造型呈现，并包含新手教学、关卡计时、暂停与存档等完整流程。

> 软件工程课程第二次个人作业

---
### 1. 开始界面

<img src="https://img2024.cnblogs.com/blog/3849039/202609/3849039-20260921200408650-1010175912.png" alt="测试面板和箭头" width="60%">

开始界面提供两个入口：

- **新游戏**：从第 1 关开始，清空旧存档
- **继续游戏**：从上次存档的关卡继续（无存档时按钮变灰不可点）

背景是深蓝星空，包含星云、银河、自转星球和闪烁星星。

### 2. 新手教学

<img src="https://img2024.cnblogs.com/blog/3849039/202609/3849039-20260921202549011-1400293838.png" alt="成功演示" width="60%">
<img src="https://img2024.cnblogs.com/blog/3849039/202609/3849039-20260921202905103-534819678.png" alt="阻挡演示" width="60%">
<img src="https://img2024.cnblogs.com/blog/3849039/202609/3849039-20260921202611605-1949283640.png" alt="教学试玩" width="60%">

正式关卡前有一段教学流程：

1. **成功演示**：展示火箭前方无阻挡时飞出
2. **阻挡演示**：展示前方有火箭时无法飞出
3. **教学试玩**：让玩家自己尝试点出正确的火箭

### 3. 游戏界面

<img src="https://img2024.cnblogs.com/blog/3849039/202609/3849039-20260921202720664-1792227950.png" alt="游戏界面" width="60%">

游戏界面包含：

- **左上**：当前关卡、剩余机会
- **右上**：计时器（淡黄窗口）、暂停按钮
- **中央**：全息投影风格的棋盘
- **棋盘内**：小火箭造型的箭头，带尾焰

### 4. 暂停与存档

<img src="https://img2024.cnblogs.com/blog/3849039/202609/3849039-20260921202836454-613408782.png" alt="暂停和存档" width="60%">


游戏中点击右上角"暂停"按钮：

- 计时冻结
- 弹出居中面板，遮罩下方仍可见棋盘
- 两个按钮：**继续游戏**、**存档并退出**

### 5. 通关界面

<img src="https://img2024.cnblogs.com/blog/3849039/202609/3849039-20260921202746472-1867742635.png" alt="通关界面" width="60%">

清空全部火箭后进入通关界面：

- 显示"本关耗时 XX:XX"
- 点击"下一关"进入下一关

### 6. 失败界面

<img src="https://img2024.cnblogs.com/blog/3849039/202609/3849039-20260921202809154-936953173.png" alt="教学试玩" width="60%">

失误次数耗尽时进入失败界面：

- 显示"本关耗时 XX:XX"
- 点击"重新开始本关"重置当前关卡

---

## 🎮 游戏简介

"一箭又一箭"是一类点击式箭头解谜游戏，规则简单但需要一定观察和推理：

- 棋盘上分布着若干朝向上、下、左、右的火箭
- 点击一个火箭，程序检查它前进方向上是否有其他火箭阻挡
- **前方无阻挡**：火箭飞出棋盘并消失
- **前方有阻挡**：火箭不能飞出，变红并抖动，扣除一次失误机会
- 清空全部火箭 → 通关
- 失误次数耗尽 → 失败，可重新开始

---

## ✨ 功能特色

- 🚀 四种方向的小火箭箭头，带尾焰动画
- 🌌 深蓝宇宙星空背景：星云、银河、闪烁星星、自转星球
- 🎯 全息投影风格的棋盘
- 👨‍🏫 新手教学流程（成功演示 + 阻挡演示 + 教学试玩）
- ⏱️ 关卡计时器（右上角淡黄圆角窗口，显示 `MM:SS`）
- ⏸️ 暂停功能（计时冻结，弹出居中面板）
- 💾 存档与继续游戏（保存关卡、棋盘、机会数、已耗时）
- 🎉 通关 / 失败界面，显示本关耗时
- 🧩 代码结构清晰，模块职责分离

---

## 🖥️ 开发环境

| 项目 | 版本 |
| --- | --- |
| 操作系统 | Windows 10 / 11 |
| Python | 3.11 |
| Pygame | 2.6.1 |

---

## 📦 安装与运行

### 1. 克隆仓库

```bash
git clone https://github.com/Vivian-azad/one-arrow-game.git
cd one-arrow-game
```

### 2. 安装依赖

建议使用虚拟环境：

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS / Linux
```

安装依赖：

```bash
pip install -r requirements.txt
```

### 3. 运行游戏

```bash
python main.py
```

---

## 🕹️ 游戏操作说明

| 操作 | 说明 |
| --- | --- |
| 鼠标左键点击火箭 | 尝试让火箭飞出 |
| 点击右上角"暂停"按钮 | 暂停游戏（计时冻结） |
| 暂停面板"继续游戏" | 恢复游戏，计时继续 |
| 暂停面板"存档并退出" | 保存当前进度并返回开始界面 |
| 开始界面"新游戏" | 从第 1 关开始（清空旧存档） |
| 开始界面"继续游戏" | 从上次存档的关卡继续 |

**玩法提示**：优先点击那些"前方没有其他火箭"的火箭，它们飞出后会为后面的火箭让出通道。

---

## 📁 项目结构

```
one-arrow-game/
├── main.py                 入口，约 40 行
├── requirements.txt
├── README.md
├── .gitignore
├── images/                 游戏截图
├── game/
│   ├── __init__.py
│   ├── settings.py         常量配置 + 字体初始化
│   ├── starfield.py        星空、星云、银河、星星、星球
│   ├── ui.py               通用 UI 组件（按钮）
│   ├── game.py             Game 类：状态机、事件、更新、绘制
│   ├── save_system.py      存档读写
│   ├── arrow.py            Arrow 数据类
│   └── board.py            Board 数据类（路径检测）
├── levels/
│   ├── __init__.py
│   └── levels.py           关卡数据
└── tests/
    ├── test_arrow.py
    ├── test_board.py
    └── test_game.py
```

---

## 🧠 核心实现思路

### 1. 箭头和方向的表示

每个箭头用 `Arrow` 类表示，`row/col` 是逻辑坐标，`x/y` 是屏幕坐标：

```python
class Arrow:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.x = None
        self.y = None
        self.flying = False
        self.hit_timer = 0
```

### 2. 路径检测

用 `DIRECTIONS` 字典把四个方向统一成 `(行增量, 列增量)`，沿方向逐格扫描：

```python
DIRECTIONS = {
    "right": (0, 1),
    "left":  (0, -1),
    "down":  (1, 0),
    "up":    (-1, 0)
}

def can_exit(self, arrow):
    row_step, col_step = self.DIRECTIONS[arrow.direction]
    row = arrow.row + row_step
    col = arrow.col + col_step

    while 0 <= row < self.rows and 0 <= col < self.cols:
        if self.grid[row][col] is not None:
            return False
        row += row_step
        col += col_step

    return True
```

### 3. 状态同步

箭头起飞时**立即**从棋盘逻辑层移除，避免"飞行中仍被当作障碍物"的问题：

```python
def start_flying(self, arrow):
    if arrow.flying:
        return
    arrow.flying = True

    if self.board.grid[arrow.row][arrow.col] is arrow:
        self.board.grid[arrow.row][arrow.col] = None
```

### 4. 计时器

```python
self.level_start_ticks = 0
self.level_elapsed_ms = 0
self.timer_running = False
```

- 运行中：`elapsed = now - level_start_ticks`
- 停表：`level_elapsed_ms = now - level_start_ticks`
- 暂停恢复：`level_start_ticks = now - paused_elapsed_ms`

### 5. 存档

存档为 `save.json`：

```json
{
  "level_index": 2,
  "elapsed_ms": 45000,
  "mistakes": 2,
  "arrows": [
    {"row": 0, "col": 0, "direction": "right"}
  ]
}
```

只保存静止的箭头，飞行中的箭头丢弃（它们本来就会消失）。

---

## 🧪 测试

### 手工测试

| 编号 | 测试内容 | 预期结果 |
| --- | --- | --- |
| T01 | 点击前方无阻挡的箭头 | 箭头飞出棋盘并消失 |
| T02 | 点击前方有阻挡的箭头 | 箭头不飞出，失误次数 -1 |
| T03 | 点击位于边缘且朝向棋盘外的箭头 | 箭头正常消失，不发生越界错误 |
| T04 | 消除本关全部箭头 | 显示通关并进入下一关 |
| T05 | 失误次数耗尽 | 显示失败并允许重新开始 |
| T06 | 游戏进行中重新开始 | 箭头布局和失误次数恢复 |

### 自动化测试

```bash
python -m pytest tests/
```

---

## 🔧 AIGC 使用说明

本项目在开发过程中使用了 AIGC 工具（ChatGPT，DeepSeek）辅助完成部分功能的设计、代码理解和问题排查。主要使用场景包括：

- 路径检测逻辑设计
- 箭头飞出动画方案
- 碰撞反馈与失败机制
- 关卡设计与边界测试
- 隐藏 Bug 排查（飞行中箭头被误判为障碍物）
- 星空 UI 视觉迭代
- 代码结构重构建议

AI 生成的代码均经过本人理解、修改和实际测试后才进入项目。

---

## 📄 许可证

本项目为课程作业，仅供学习交流使用。

---

## 🙏 致谢

- 游戏玩法参考：微信小游戏《一箭又一箭》
- 开发工具：Python、Pygame
- AIGC 辅助：ChatGPT,DeepSeek
