"""
星空背景：星云、银河、星星、星球
"""

import math
import random

import pygame

from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BG_COLOR,
    NEBULA_PALETTE,
    GALAXY_CORE_COLOR, GALAXY_INNER_COLOR, GALAXY_MID_COLOR,
    GALAXY_OUTER_COLOR, GALAXY_DUST_COLOR,
    STAR_COLOR_BRIGHT, STAR_COLOR_DIM,
    WHITE,
)

STAR_SEED = 20260921


def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def multi_stop_gradient(stops, t):
    t = max(0.0, min(1.0, t))

    for i in range(len(stops) - 1):

        p1, c1 = stops[i]
        p2, c2 = stops[i + 1]

        if p1 <= t <= p2:
            local_t = (t - p1) / (p2 - p1) if p2 > p1 else 0
            return lerp_color(c1, c2, local_t)

    return stops[-1][1]


def build_starfield_surface():
    """预渲染星云 + 银河"""

    rng = random.Random(STAR_SEED)

    surface = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )

    # ---------- 星云 ----------

    nebula_centers = [
        (-60, 520, 340, 0),
        (760, 100, 320, 1),
        (80, -40, 280, 2),
        (820, 560, 300, 3),
        (400, 620, 260, 4),
    ]

    for cx, cy, radius, palette_index in nebula_centers:

        base_color = NEBULA_PALETTE[palette_index]

        for _ in range(180):

            angle = rng.uniform(0, math.pi * 2)
            dist = rng.uniform(0, 1) ** 0.7 * radius

            px = cx + math.cos(angle) * dist
            py = cy + math.sin(angle) * dist

            r = rng.uniform(15, 55) * (1 - dist / radius * 0.6)
            r = max(8, r)

            a = int(28 * (1 - dist / radius) + rng.uniform(0, 10))
            a = max(4, min(40, a))

            tint = rng.uniform(0, 1) * 0.4
            color = lerp_color(base_color, WHITE, tint)

            pygame.draw.circle(
                surface,
                (*color, a),
                (int(px), int(py)),
                int(r)
            )

    # ---------- 银河 ----------

    def galaxy_point(t):
        x = SCREEN_WIDTH * 1.05 - t * SCREEN_WIDTH * 1.25
        y = SCREEN_HEIGHT * 0.95 - t * SCREEN_HEIGHT * 1.1
        y += math.sin(t * math.pi) * 40
        return x, y

    def galaxy_tangent(t):
        dx = -SCREEN_WIDTH * 1.25
        dy = -SCREEN_HEIGHT * 1.1 + math.cos(t * math.pi) * 40 * math.pi
        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        return dx / length, dy / length

    def galaxy_normal(t):
        tx, ty = galaxy_tangent(t)
        return -ty, tx

    galaxy_stops = [
        (0.0, GALAXY_CORE_COLOR),
        (0.12, GALAXY_INNER_COLOR),
        (0.35, GALAXY_MID_COLOR),
        (0.7, GALAXY_OUTER_COLOR),
        (1.0, (30, 35, 80)),
    ]

    for _ in range(220):

        t = rng.uniform(0, 1)
        cx, cy = galaxy_point(t)
        nx, ny = galaxy_normal(t)

        offset = rng.gauss(0, 45)

        px = cx + nx * offset
        py = cy + ny * offset

        dist_factor = min(1.0, abs(offset) / 90)

        color = multi_stop_gradient(galaxy_stops, dist_factor)

        r = rng.randint(6, 14)
        a = int(12 * (1 - dist_factor) + rng.uniform(0, 4))
        a = max(2, min(16, a))

        pygame.draw.circle(surface, (*color, a), (int(px), int(py)), r)

    for _ in range(700):

        t = rng.uniform(0, 1)
        cx, cy = galaxy_point(t)
        nx, ny = galaxy_normal(t)

        offset = rng.gauss(0, 18)

        px = cx + nx * offset
        py = cy + ny * offset

        dist_factor = min(1.0, abs(offset) / 45)

        color = multi_stop_gradient(galaxy_stops, dist_factor)

        r = rng.randint(1, 3)
        a = int(28 * (1 - dist_factor) + rng.uniform(0, 8))
        a = max(4, min(40, a))

        pygame.draw.circle(surface, (*color, a), (int(px), int(py)), r)

    for _ in range(260):

        t = rng.uniform(0, 1)
        cx, cy = galaxy_point(t)
        nx, ny = galaxy_normal(t)

        offset = rng.gauss(0, 12)

        px = cx + nx * offset
        py = cy + ny * offset

        dist_factor = min(1.0, abs(offset) / 30)

        r = rng.randint(2, 5)
        a = int(26 * (1 - dist_factor) + rng.uniform(0, 6))
        a = max(6, min(32, a))

        pygame.draw.circle(
            surface,
            (*GALAXY_DUST_COLOR, a),
            (int(px), int(py)),
            r
        )

    for _ in range(60):

        t = rng.uniform(0, 1)
        cx, cy = galaxy_point(t)
        nx, ny = galaxy_normal(t)

        offset = rng.gauss(0, 22)

        px = cx + nx * offset
        py = cy + ny * offset

        color = GALAXY_INNER_COLOR
        r = rng.choice([1, 1, 2])
        a = rng.randint(80, 160)

        pygame.draw.circle(surface, (*color, a), (int(px), int(py)), r)

    return surface


# ---------- 星星 ----------

def build_stars():
    rng = random.Random(STAR_SEED + 100)

    stars = []

    for _ in range(140):

        x = rng.randint(0, SCREEN_WIDTH)
        y = rng.randint(0, SCREEN_HEIGHT)

        radius = rng.choice([1, 1, 1, 2, 2, 3])

        base_brightness = rng.uniform(0.5, 1.0)
        phase = rng.uniform(0, math.pi * 2)

        if rng.random() < 0.3:
            speed = rng.uniform(0.06, 0.10)
            flicker_amp = 0.45
        else:
            speed = rng.uniform(0.02, 0.05)
            flicker_amp = 0.2

        has_cross = radius >= 3 and base_brightness > 0.85

        stars.append(
            (x, y, radius, base_brightness, phase, speed, flicker_amp, has_cross)
        )

    return stars


# ---------- 星球 ----------

def build_planet_texture(seed_offset, count):
    rng = random.Random(STAR_SEED + seed_offset)

    points = []

    for _ in range(count):

        lon = rng.uniform(0, math.pi * 2)
        lat = rng.uniform(-math.radians(75), math.radians(75))

        size = rng.uniform(0.08, 0.18)
        alpha = rng.randint(30, 70)

        points.append((lon, lat, size, alpha))

    return points


PLANET_SMALL = {
    "x": 90,
    "y": 130,
    "radius": 26,
    "base_color": (60, 70, 110),
    "light_color": (120, 140, 190),
    "texture": build_planet_texture(1, 40),
    "rot_speed": 0.15,
    "ring": False,
}

PLANET_LARGE = {
    "x": 720,
    "y": 500,
    "radius": 48,
    "base_color": (70, 60, 100),
    "light_color": (150, 130, 180),
    "texture": build_planet_texture(2, 70),
    "rot_speed": 0.08,
    "ring": True,
    "ring_color": (140, 130, 180),
    "ring_tilt": 0.35,
}


def draw_planet(screen, planet, time_s):
    """绘制一颗自转星球"""

    cx = planet["x"]
    cy = planet["y"]
    radius = planet["radius"]

    base_color = planet["base_color"]
    light_color = planet["light_color"]

    if planet["ring"]:

        ring_color = planet["ring_color"]

        ring_rx = int(radius * 1.9)
        ring_ry = int(radius * 0.55)

        ring_surface = pygame.Surface(
            (ring_rx * 2 + 4, ring_ry * 2 + 4),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            ring_surface,
            (*ring_color, 90),
            (2, 2, ring_rx * 2, ring_ry * 2),
            width=3
        )

        pygame.draw.ellipse(
            ring_surface,
            (*ring_color, 40),
            (2, 2, ring_rx * 2, ring_ry * 2),
            width=6
        )

        screen.blit(
            ring_surface,
            (cx - ring_rx - 2, cy - ring_ry - 2)
        )

    light_dir_x = -0.4
    light_dir_y = -0.4

    steps = 18

    for i in range(steps, 0, -1):

        t = i / steps

        r = int(radius * t)

        offset = (1 - t) * radius * 0.35
        ox = int(cx + light_dir_x * offset)
        oy = int(cy + light_dir_y * offset)

        color_t = 1 - t
        color = lerp_color(base_color, light_color, color_t)

        pygame.draw.circle(screen, color, (ox, oy), r)

    rotation = time_s * planet["rot_speed"]

    texture_surface = pygame.Surface(
        (radius * 2, radius * 2),
        pygame.SRCALPHA
    )

    for lon, lat, size, alpha in planet["texture"]:

        cur_lon = lon + rotation

        cos_lat = math.cos(lat)
        px3 = cos_lat * math.cos(cur_lon)
        py3 = math.sin(lat)
        pz3 = cos_lat * math.sin(cur_lon)

        if pz3 <= 0:
            continue

        sx = radius + px3 * radius
        sy = radius + py3 * radius

        edge_factor = pz3

        r = max(1, int(size * radius))
        a = int(alpha * edge_factor)
        if a <= 0:
            continue

        tex_color = lerp_color(base_color, (0, 0, 0), 0.4)

        pygame.draw.circle(
            texture_surface,
            (*tex_color, a),
            (int(sx), int(sy)),
            r
        )

    mask_surface = pygame.Surface(
        (radius * 2, radius * 2),
        pygame.SRCALPHA
    )
    pygame.draw.circle(mask_surface, (255, 255, 255, 255), (radius, radius), radius)

    texture_surface.blit(
        mask_surface,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MIN
    )

    screen.blit(texture_surface, (cx - radius, cy - radius))

    if planet["ring"]:

        ring_color = planet["ring_color"]

        ring_rx = int(radius * 1.9)
        ring_ry = int(radius * 0.55)

        front_surface = pygame.Surface(
            (ring_rx * 2 + 4, ring_ry + 4),
            pygame.SRCALPHA
        )

        pygame.draw.arc(
            front_surface,
            (*ring_color, 110),
            (2, 2, ring_rx * 2, ring_ry * 2),
            math.pi,
            math.pi * 2,
            3
        )

        screen.blit(
            front_surface,
            (cx - ring_rx - 2, cy - 2)
        )

    glow_surface = pygame.Surface(
        (radius * 2 + 20, radius * 2 + 20),
        pygame.SRCALPHA
    )

    glow_center = radius + 10

    for i in range(4):

        glow_r = radius + 2 + i * 3
        a = max(0, 30 - i * 8)

        pygame.draw.circle(
            glow_surface,
            (*light_color, a),
            (glow_center, glow_center),
            glow_r,
            width=1
        )

    screen.blit(glow_surface, (cx - glow_center, cy - glow_center))


def draw_star_cross(screen, ix, iy, color, brightness):
    """十字光芒"""

    arm_length = 6

    for offset in range(-arm_length, arm_length + 1):

        if offset == 0:
            continue

        rel = abs(offset) / arm_length

        a = int(120 * (1 - rel) ** 2 * brightness)
        if a <= 2:
            continue

        pygame.draw.circle(screen, (*color, a), (ix + offset, iy), 1)

    for offset in range(-arm_length, arm_length + 1):

        if offset == 0:
            continue

        rel = abs(offset) / arm_length

        a = int(120 * (1 - rel) ** 2 * brightness)
        if a <= 2:
            continue

        pygame.draw.circle(screen, (*color, a), (ix, iy + offset), 1)


def draw_starfield(screen, starfield_surface, stars, time_s):
    """绘制完整星空"""

    screen.blit(starfield_surface, (0, 0))

    draw_planet(screen, PLANET_SMALL, time_s)
    draw_planet(screen, PLANET_LARGE, time_s)

    t = time_s

    for x, y, radius, base_brightness, phase, speed, flicker_amp, has_cross in stars:

        flicker = base_brightness + math.sin(phase + t * speed * 10) * flicker_amp
        flicker = max(0.15, min(1.0, flicker))

        color = (
            int(STAR_COLOR_DIM[0] + (STAR_COLOR_BRIGHT[0] - STAR_COLOR_DIM[0]) * flicker),
            int(STAR_COLOR_DIM[1] + (STAR_COLOR_BRIGHT[1] - STAR_COLOR_DIM[1]) * flicker),
            int(STAR_COLOR_DIM[2] + (STAR_COLOR_BRIGHT[2] - STAR_COLOR_DIM[2]) * flicker),
        )

        ix = int(x)
        iy = int(y)

        if has_cross:
            draw_star_cross(screen, ix, iy, color, flicker)

        pygame.draw.circle(screen, color, (ix, iy), radius)