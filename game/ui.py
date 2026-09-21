"""
通用 UI 组件：按钮
"""

import pygame

from game.settings import (
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR,
    BUTTON_DISABLED_COLOR, BUTTON_DISABLED_BORDER,
    TEXT_DISABLED_COLOR,
    WHITE,
)

import game.settings as settings


def draw_button(screen, text, rect, enabled=True):
    """绘制按钮，enabled=False 时变灰不可点"""

    mouse_pos = pygame.mouse.get_pos()

    if not enabled:
        color = BUTTON_DISABLED_COLOR
        border = BUTTON_DISABLED_BORDER
    elif rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
        border = BUTTON_BORDER_COLOR
    else:
        color = BUTTON_COLOR
        border = BUTTON_BORDER_COLOR

    pygame.draw.rect(screen, color, rect, border_radius=8)

    pygame.draw.rect(
        screen,
        border,
        rect,
        width=2,
        border_radius=8
    )

    text_color = WHITE if enabled else TEXT_DISABLED_COLOR

    text_surface = settings.font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center

    screen.blit(text_surface, text_rect)