"""
Game 类：管理游戏状态机、事件、更新、绘制
"""

import random

import pygame

from game.arrow import Arrow
from game.board import Board
from levels.levels import LEVELS

import game.settings as settings
from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    ROWS, COLS, BOARD_SIZE, CELL_SIZE,
    BOARD_X, BOARD_Y,
    BOARD_GRID_COLOR, BOARD_BORDER_COLOR, BOARD_GLOW_COLOR,
    ROCKET_BODY_COLOR, ROCKET_TIP_COLOR, ROCKET_FIN_COLOR,
    ROCKET_WINDOW_COLOR, ROCKET_WINDOW_RIM,
    FLAME_COLOR_OUTER, FLAME_COLOR_MID, FLAME_COLOR_INNER,
    HIT_COLOR,
    TEXT_COLOR, TEXT_DIM_COLOR,
    TIMER_BG_COLOR, TIMER_BG_ALPHA,
    TIMER_BORDER_COLOR, TIMER_TEXT_COLOR,
    PAUSE_BUTTON_COLOR, PAUSE_BUTTON_HOVER, PAUSE_BUTTON_BORDER,
    OVERLAY_COLOR, PAUSE_PANEL_COLOR, PAUSE_PANEL_BORDER,
    WHITE,
)

from game.ui import draw_button
from game.starfield import draw_starfield
from game import save_system


def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


class Game:

    def __init__(self, screen, starfield_surface, stars):

        self.screen = screen
        self.starfield_surface = starfield_surface
        self.stars = stars

        # 状态
        self.game_state = "start"
        self.current_level = 0

        self.board = None
        self.arrows = []
        self.mistakes = 3

        # 计时
        self.level_start_ticks = 0
        self.level_elapsed_ms = 0
        self.timer_running = False
        self.paused_elapsed_ms = 0

        # 教程
        self.tutorial_timer = 0
        self.tutorial_arrow_x = 0
        self.tutorial_arrows = []

        # 暂停按钮
        self.pause_button_rect = pygame.Rect(
            SCREEN_WIDTH - 130 - 20,
            64,
            130,
            32
        )

    # ==================== 存档代理 ====================

    def has_save(self):
        return save_system.has_save()

    def write_save(self):
        save_system.write_save(
            self.current_level,
            self.get_elapsed_ms(),
            self.mistakes,
            self.arrows,
        )

    # ==================== 计时 ====================

    def stop_timer(self):
        if self.timer_running:
            self.level_elapsed_ms = pygame.time.get_ticks() - self.level_start_ticks
            self.timer_running = False

    def get_elapsed_ms(self):
        if self.timer_running:
            return pygame.time.get_ticks() - self.level_start_ticks
        else:
            return self.level_elapsed_ms

    @staticmethod
    def format_time(ms):
        total_seconds = ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    # ==================== 关卡 ====================

    def load_level(self, level_index):

        self.board = Board(ROWS, COLS)
        self.arrows = []

        for row, col, direction in LEVELS[level_index]:

            arrow = Arrow(row, col, direction)

            self.board.add_arrow(arrow)
            self.arrows.append(arrow)

        self.mistakes = 3

        for arrow in self.arrows:
            x, y = self.get_cell_center(arrow.row, arrow.col)
            arrow.set_position(x, y)

        self.level_start_ticks = pygame.time.get_ticks()
        self.level_elapsed_ms = 0
        self.timer_running = True

    def load_save_state(self, save_data):

        self.current_level = save_data["level_index"]

        self.board = Board(ROWS, COLS)
        self.arrows = []

        for item in save_data["arrows"]:

            arrow = Arrow(item["row"], item["col"], item["direction"])

            self.board.add_arrow(arrow)
            self.arrows.append(arrow)

            x, y = self.get_cell_center(arrow.row, arrow.col)
            arrow.set_position(x, y)

        self.mistakes = save_data["mistakes"]

        self.level_elapsed_ms = save_data["elapsed_ms"]
        self.level_start_ticks = pygame.time.get_ticks() - self.level_elapsed_ms
        self.timer_running = True

    def get_cell_center(self, row, col):

        x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

        return x, y

    # ==================== 事件处理 ====================

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        mouse_pos = event.pos

        if self.game_state == "start":
            self.handle_start_click(mouse_pos)
        elif self.game_state == "tutorial_play":
            self.handle_tutorial_play_click(mouse_pos)
        elif self.game_state == "tutorial_complete":
            self.handle_tutorial_complete_click(mouse_pos)
        elif self.game_state == "playing":
            self.handle_playing_click(mouse_pos)
        elif self.game_state == "paused":
            self.handle_paused_click(mouse_pos)
        elif self.game_state == "failed":
            self.handle_failed_click(mouse_pos)
        elif self.game_state == "won":
            self.handle_won_click(mouse_pos)

    def handle_start_click(self, mouse_pos):

        new_game_button = pygame.Rect(0, 0, 220, 60)
        new_game_button.center = (SCREEN_WIDTH // 2, 330)

        continue_button = pygame.Rect(0, 0, 220, 60)
        continue_button.center = (SCREEN_WIDTH // 2, 410)

        if new_game_button.collidepoint(mouse_pos):

            save_system.delete_save()

            self.current_level = 0
            self.load_level(self.current_level)
            self.game_state = "tutorial_success"
            self.tutorial_timer = 0
            self.tutorial_arrow_x = BOARD_X + 2 * CELL_SIZE + CELL_SIZE // 2

        elif continue_button.collidepoint(mouse_pos) and self.has_save():

            save_data = save_system.read_save()

            if save_data is not None:
                self.load_save_state(save_data)
                self.game_state = "playing"

    def handle_tutorial_play_click(self, mouse_pos):

        clicked_arrow = None

        for arrow in self.tutorial_arrows:

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

            for other in self.tutorial_arrows:
                if other is not clicked_arrow:
                    temp_board.add_arrow(other)

            if temp_board.can_exit(clicked_arrow):
                clicked_arrow.flying = True
            else:
                clicked_arrow.hit_timer = 18

    def handle_tutorial_complete_click(self, mouse_pos):

        start_button = pygame.Rect(0, 0, 200, 60)
        start_button.center = (SCREEN_WIDTH // 2, 370)

        if start_button.collidepoint(mouse_pos):
            self.current_level = 0
            self.load_level(self.current_level)
            self.game_state = "playing"

    def handle_playing_click(self, mouse_pos):

        if self.pause_button_rect.collidepoint(mouse_pos):

            self.stop_timer()
            self.paused_elapsed_ms = self.level_elapsed_ms
            self.game_state = "paused"
            return

        clicked_arrow = self.get_clicked_arrow(mouse_pos)

        if clicked_arrow is not None:

            if self.board.can_exit(clicked_arrow):
                self.start_flying(clicked_arrow)
            else:
                clicked_arrow.hit_timer = 18
                self.mistakes -= 1

                if self.mistakes <= 0:
                    self.stop_timer()
                    self.game_state = "failed"

    def handle_paused_click(self, mouse_pos):

        panel_width = 320
        panel_height = 260
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2

        resume_button = pygame.Rect(0, 0, 220, 52)
        resume_button.center = (SCREEN_WIDTH // 2, panel_y + 130)

        save_button = pygame.Rect(0, 0, 220, 52)
        save_button.center = (SCREEN_WIDTH // 2, panel_y + 200)

        if resume_button.collidepoint(mouse_pos):

            self.level_start_ticks = pygame.time.get_ticks() - self.paused_elapsed_ms
            self.timer_running = True
            self.game_state = "playing"

        elif save_button.collidepoint(mouse_pos):

            self.write_save()
            self.game_state = "start"

    def handle_failed_click(self, mouse_pos):

        restart_button = pygame.Rect(0, 0, 200, 60)
        restart_button.center = (SCREEN_WIDTH // 2, 360)

        if restart_button.collidepoint(mouse_pos):
            self.load_level(self.current_level)
            self.game_state = "playing"

    def handle_won_click(self, mouse_pos):

        next_button = pygame.Rect(0, 0, 200, 60)
        next_button.center = (SCREEN_WIDTH // 2, 350)

        if next_button.collidepoint(mouse_pos):

            if self.current_level < len(LEVELS) - 1:
                self.current_level += 1
                self.load_level(self.current_level)
                self.game_state = "playing"
            else:
                self.current_level = 0
                self.load_level(self.current_level)
                self.game_state = "playing"

    # ==================== 更新 ====================

    def update(self):

        if self.game_state == "tutorial_success":
            self.update_tutorial_success()
        elif self.game_state == "tutorial_blocked":
            self.update_tutorial_blocked()
        elif self.game_state == "tutorial_play":
            self.update_tutorial_play()
        elif self.game_state == "playing":

            for arrow in self.arrows:
                self.update_arrow(arrow)

            for arrow in self.arrows:
                if arrow.hit_timer > 0:
                    arrow.hit_timer -= 1

            if self.is_level_complete():
                self.stop_timer()
                self.game_state = "won"

    def update_tutorial_success(self):

        self.tutorial_timer += 1

        if self.tutorial_timer < 30:
            self.tutorial_arrow_x = BOARD_X + 2 * CELL_SIZE + CELL_SIZE // 2
        elif self.tutorial_timer < 100:
            self.tutorial_arrow_x += 8
        elif self.tutorial_timer < 150:
            pass
        else:
            self.tutorial_timer = 0
            self.game_state = "tutorial_blocked"

    def update_tutorial_blocked(self):

        self.tutorial_timer += 1

        if self.tutorial_timer >= 150:
            self.tutorial_timer = 0
            self.create_tutorial_arrows()
            self.game_state = "tutorial_play"

    def update_tutorial_play(self):

        self.tutorial_timer += 1

        for arrow in self.tutorial_arrows:
            if arrow.hit_timer > 0:
                arrow.hit_timer -= 1

        for arrow in self.tutorial_arrows:

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

        for arrow in self.tutorial_arrows:

            if (
                arrow.x < -50
                or arrow.x > SCREEN_WIDTH + 50
                or arrow.y < -50
                or arrow.y > SCREEN_HEIGHT + 50
            ):
                continue

            remaining.append(arrow)

        self.tutorial_arrows = remaining

        if len(self.tutorial_arrows) == 0:
            self.game_state = "tutorial_complete"
            self.tutorial_timer = 0

    def update_arrow(self, arrow):

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
            if arrow in self.arrows:
                self.arrows.remove(arrow)

    def is_level_complete(self):
        return len(self.arrows) == 0

    # ==================== 游戏内小工具 ====================

    def create_tutorial_arrows(self):

        self.tutorial_arrows = []

        positions = [(1, 1), (1, 3), (1, 5)]

        for row, col in positions:

            arrow = Arrow(row, col, "right")

            x, y = self.get_cell_center(row, col)
            arrow.set_position(x, y)

            self.tutorial_arrows.append(arrow)

    def get_clicked_arrow(self, pos):

        mouse_x, mouse_y = pos

        for arrow in self.arrows:

            if arrow.flying:
                continue

            distance_x = abs(mouse_x - arrow.x)
            distance_y = abs(mouse_y - arrow.y)

            if distance_x <= CELL_SIZE // 2:
                if distance_y <= CELL_SIZE // 2:
                    return arrow

        return None

    def start_flying(self, arrow):

        if arrow.flying:
            return

        arrow.flying = True

        if self.board.grid[arrow.row][arrow.col] is arrow:
            self.board.grid[arrow.row][arrow.col] = None

    # ==================== 绘制 ====================

    def draw(self):

        time_s = pygame.time.get_ticks() / 1000.0

        draw_starfield(self.screen, self.starfield_surface, self.stars, time_s)

        if self.game_state == "start":
            self.draw_start_screen()
        elif self.game_state == "tutorial_success":
            self.draw_tutorial_success()
        elif self.game_state == "tutorial_blocked":
            self.draw_tutorial_blocked()
        elif self.game_state == "tutorial_play":
            self.draw_tutorial_play()
        elif self.game_state == "tutorial_complete":
            self.draw_tutorial_complete()
        elif self.game_state == "playing":
            self.draw_playing_scene()
        elif self.game_state == "paused":
            self.draw_playing_scene()
            self.draw_pause_overlay()
        elif self.game_state == "failed":
            self.draw_failed_screen()
        elif self.game_state == "won":
            self.draw_won_screen()

    def draw_playing_scene(self):
        """绘制游戏中的画面（棋盘、计时器、暂停按钮、火箭）"""

        self.draw_game_info()
        self.draw_board()
        self.draw_timer()
        self.draw_pause_button()

        for arrow in self.arrows:
            if arrow.hit_timer > 0:
                self.draw_arrow(arrow, HIT_COLOR)
            else:
                self.draw_arrow(arrow)

    def draw_button(self, text, rect, enabled=True):
        draw_button(self.screen, text, rect, enabled=enabled)

    def draw_start_screen(self):

        title = settings.title_font.render("一箭又一箭", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        subtitle = settings.font.render(
            "点击火箭，让它们依次飞出棋盘",
            True,
            TEXT_DIM_COLOR
        )
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)

        new_game_button = pygame.Rect(0, 0, 220, 60)
        new_game_button.center = (SCREEN_WIDTH // 2, 330)
        self.draw_button("新游戏", new_game_button)

        continue_button = pygame.Rect(0, 0, 220, 60)
        continue_button.center = (SCREEN_WIDTH // 2, 410)
        self.draw_button("继续游戏", continue_button, enabled=self.has_save())

    def draw_game_info(self):

        level_text = settings.font.render(f"第 {self.current_level + 1} 关", True, TEXT_COLOR)
        mistake_text = settings.font.render(f"剩余机会：{self.mistakes}", True, TEXT_COLOR)

        self.screen.blit(level_text, (30, 14))
        self.screen.blit(mistake_text, (250, 14))

    def draw_board(self):

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

            self.screen.blit(surface, (glow_rect.x, glow_rect.y))

        board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)

        pygame.draw.rect(
            self.screen,
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

        self.screen.blit(grid_surface, (BOARD_X, BOARD_Y))

    def draw_timer(self):

        timer_width = 130
        timer_height = 44
        timer_x = SCREEN_WIDTH - timer_width - 20
        timer_y = 10

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

        self.screen.blit(bg_surface, (timer_x, timer_y))

        pygame.draw.rect(
            self.screen,
            TIMER_BORDER_COLOR,
            (timer_x, timer_y, timer_width, timer_height),
            width=2,
            border_radius=10
        )

        elapsed = self.get_elapsed_ms()
        time_str = self.format_time(elapsed)

        time_text = settings.font.render(time_str, True, TIMER_TEXT_COLOR)
        time_rect = time_text.get_rect(
            center=(timer_x + timer_width // 2, timer_y + timer_height // 2)
        )

        self.screen.blit(time_text, time_rect)

    def draw_pause_button(self):

        mouse_pos = pygame.mouse.get_pos()

        if self.pause_button_rect.collidepoint(mouse_pos):
            color = PAUSE_BUTTON_HOVER
        else:
            color = PAUSE_BUTTON_COLOR

        pygame.draw.rect(self.screen, color, self.pause_button_rect, border_radius=8)

        pygame.draw.rect(
            self.screen,
            PAUSE_BUTTON_BORDER,
            self.pause_button_rect,
            width=2,
            border_radius=8
        )

        text_surface = settings.small_font.render("暂停", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = self.pause_button_rect.center

        self.screen.blit(text_surface, text_rect)

    def draw_rocket(self, x, y, direction, body_color, tip_color, fin_color,
                    flame_length=0):

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

            pygame.draw.polygon(self.screen, FLAME_COLOR_OUTER, transform(flame_outer))
            pygame.draw.polygon(self.screen, FLAME_COLOR_MID, transform(flame_mid))
            pygame.draw.polygon(self.screen, FLAME_COLOR_INNER, transform(flame_inner))

        pygame.draw.polygon(self.screen, fin_color, transform(fin_top))
        pygame.draw.polygon(self.screen, fin_color, transform(fin_bottom))

        pygame.draw.polygon(self.screen, body_color, transform(body))

        shadow_color = lerp_color(body_color, (0, 0, 0), 0.25)
        pygame.draw.polygon(self.screen, shadow_color, transform(body_shadow))

        pygame.draw.polygon(self.screen, tip_color, transform(tip))

        wx, wy = transform_point(*window_center)

        pygame.draw.circle(self.screen, ROCKET_WINDOW_RIM, (int(wx), int(wy)), window_radius + 1)
        pygame.draw.circle(self.screen, ROCKET_WINDOW_COLOR, (int(wx), int(wy)), window_radius)

    def draw_arrow(self, arrow, color=None):

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

        self.draw_rocket(
            arrow.x + offset_x,
            arrow.y,
            arrow.direction,
            body_color,
            tip_color,
            fin_color,
            flame_length,
        )

    def draw_pause_overlay(self):

        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA
        )
        overlay.fill(OVERLAY_COLOR)
        self.screen.blit(overlay, (0, 0))

        panel_width = 320
        panel_height = 260
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2

        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        pygame.draw.rect(
            self.screen,
            PAUSE_PANEL_COLOR,
            panel_rect,
            border_radius=14
        )

        pygame.draw.rect(
            self.screen,
            PAUSE_PANEL_BORDER,
            panel_rect,
            width=2,
            border_radius=14
        )

        title = settings.large_font.render("游戏暂停", True, TEXT_COLOR)
        title_rect = title.get_rect(
            center=(SCREEN_WIDTH // 2, panel_y + 50)
        )
        self.screen.blit(title, title_rect)

        resume_button = pygame.Rect(0, 0, 220, 52)
        resume_button.center = (SCREEN_WIDTH // 2, panel_y + 130)
        self.draw_button("继续游戏", resume_button)

        save_button = pygame.Rect(0, 0, 220, 52)
        save_button.center = (SCREEN_WIDTH // 2, panel_y + 200)
        self.draw_button("存档并退出", save_button)

    def draw_failed_screen(self):

        center_x = SCREEN_WIDTH // 2

        title = settings.title_font.render("挑战失败", True, HIT_COLOR)
        title_rect = title.get_rect(center=(center_x, 180))
        self.screen.blit(title, title_rect)

        message = settings.font.render("错误次数已经用完", True, TEXT_DIM_COLOR)
        message_rect = message.get_rect(center=(center_x, 240))
        self.screen.blit(message, message_rect)

        elapsed = self.get_elapsed_ms()
        time_text = settings.font.render(f"本关耗时：{self.format_time(elapsed)}", True, TEXT_DIM_COLOR)
        time_rect = time_text.get_rect(center=(center_x, 280))
        self.screen.blit(time_text, time_rect)

        restart_button = pygame.Rect(0, 0, 200, 60)
        restart_button.center = (center_x, 360)
        self.draw_button("重新开始本关", restart_button)

    def draw_won_screen(self):

        center_x = SCREEN_WIDTH // 2

        title = settings.title_font.render("恭喜通关！", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(center_x, 160))
        self.screen.blit(title, title_rect)

        if self.current_level < len(LEVELS) - 1:
            message = settings.font.render("准备进入下一关", True, TEXT_DIM_COLOR)
        else:
            message = settings.font.render("你已经完成所有关卡！", True, TEXT_DIM_COLOR)

        message_rect = message.get_rect(center=(center_x, 220))
        self.screen.blit(message, message_rect)

        elapsed = self.get_elapsed_ms()
        time_text = settings.font.render(f"本关耗时：{self.format_time(elapsed)}", True, TIMER_TEXT_COLOR)
        time_rect = time_text.get_rect(center=(center_x, 270))
        self.screen.blit(time_text, time_rect)

        next_button = pygame.Rect(0, 0, 200, 60)
        next_button.center = (center_x, 350)

        if self.current_level < len(LEVELS) - 1:
            self.draw_button("下一关", next_button)
        else:
            self.draw_button("重新开始", next_button)

    # ==================== 教程绘制 ====================

    def draw_tutorial_success(self):

        title = settings.large_font.render(
            "先看看火箭是怎么飞出去的",
            True,
            TEXT_COLOR
        )
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(title, title_rect)

        self.draw_board()

        x = self.tutorial_arrow_x
        y = BOARD_Y + 3 * CELL_SIZE + CELL_SIZE // 2

        self.draw_rocket(
            x, y, "right",
            ROCKET_BODY_COLOR,
            ROCKET_TIP_COLOR,
            ROCKET_FIN_COLOR,
            flame_length=22
        )

        if self.tutorial_timer < 120:
            message = "前方没有阻挡，可以飞出。"
        else:
            message = "看到没有？没有阻挡时，火箭就可以飞出去。"

        text = settings.font.render(message, True, TEXT_DIM_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 582))
        self.screen.blit(text, text_rect)

    def draw_tutorial_blocked(self):

        title = settings.large_font.render(
            "再看看什么情况下不能飞出",
            True,
            TEXT_COLOR
        )
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(title, title_rect)

        self.draw_board()

        y = BOARD_Y + 3 * CELL_SIZE + CELL_SIZE // 2

        first_x = BOARD_X + 2 * CELL_SIZE + CELL_SIZE // 2
        second_x = BOARD_X + 5 * CELL_SIZE + CELL_SIZE // 2

        first_arrow = Arrow(3, 2, "right")
        first_arrow.set_position(first_x, y)

        second_arrow = Arrow(3, 5, "right")
        second_arrow.set_position(second_x, y)

        self.draw_arrow(second_arrow)

        if self.tutorial_timer < 30:
            offset = -3
        elif self.tutorial_timer < 60:
            offset = 3
        else:
            offset = 0

        first_arrow.x += offset

        if self.tutorial_timer >= 60:
            self.draw_arrow(first_arrow, HIT_COLOR)
        else:
            self.draw_arrow(first_arrow)

        if self.tutorial_timer < 60:
            message = "前方有火箭阻挡，无法飞出。"
        else:
            message = "错误操作会消耗一次机会。"

        text = settings.font.render(message, True, TEXT_DIM_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 582))
        self.screen.blit(text, text_rect)

    def draw_tutorial_play(self):

        title = settings.large_font.render("轮到你了", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(title, title_rect)

        self.draw_board()

        for arrow in self.tutorial_arrows:

            if arrow.flying:
                continue

            if arrow.hit_timer > 0:
                self.draw_arrow(arrow, HIT_COLOR)
            else:
                self.draw_arrow(arrow)

        message = "试试看，哪个火箭可以先飞出去？"

        text = settings.font.render(message, True, TEXT_DIM_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 582))
        self.screen.blit(text, text_rect)

    def draw_tutorial_complete(self):

        title = settings.title_font.render("教学完成！", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 170))
        self.screen.blit(title, title_rect)

        message = settings.font.render("你已经掌握基本玩法。", True, TEXT_DIM_COLOR)
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, 240))
        self.screen.blit(message, message_rect)

        message2 = settings.small_font.render(
            "接下来，试试真正的关卡吧！",
            True,
            TEXT_DIM_COLOR
        )
        message2_rect = message2.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(message2, message2_rect)

        start_button = pygame.Rect(0, 0, 200, 60)
        start_button.center = (SCREEN_WIDTH // 2, 370)
        self.draw_button("开始第一关", start_button)