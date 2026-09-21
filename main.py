"""
editor: Lai Yanran
date: 2026-09-21
task: 一箭又一箭
"""

import pygame

import game.settings as settings
from game.starfield import build_starfield_surface, build_stars
from game.game import Game


# ==================== 初始化 ====================

pygame.init()

settings.init_fonts()

screen = pygame.display.set_mode(
    (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
)
pygame.display.set_caption("一箭又一箭")

clock = pygame.time.Clock()

starfield_surface = build_starfield_surface()
stars = build_stars()

game = Game(screen, starfield_surface, stars)


# ==================== 主循环 ====================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        else:
            game.handle_event(event)

    game.update()

    screen.fill(settings.BG_COLOR)

    game.draw()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()