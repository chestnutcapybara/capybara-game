"""
 --- main.py ---
This is the main file for Capybara Conquest.

Requires pygame-ce:
pip install pygame-ce
"""

from __future__ import annotations

# Imports
import pygame  # type: ignore
import pymunk
import pymunk.pygame_util

import assets
import widgets
import terrain

from constants import *
from assets import AssetManager, SpriteSheet
from animation import Animation
from player import Player


# =========================
# Initialization
# =========================

pygame.init()
pygame.display.init()

FPS = 60
clock = pygame.time.Clock()

window = pygame.window.Window(
    title="Capybara Conquest",
    size=(SCREEN_WIDTH, SCREEN_HEIGHT),
    resizable=True
)

screen = window.get_surface()

# Icon
icon = pygame.image.load("icon.ico")
window.set_icon(icon)
window.maximize()

# Physics
level = pymunk.Space()
level.gravity = (0, 900)

draw_options = pymunk.pygame_util.DrawOptions(screen)

# Floor collision
floor = pymunk.Segment(
    level.static_body,
    (0, SCREEN_HEIGHT - 50),
    (SCREEN_WIDTH, SCREEN_HEIGHT - 50),
    5
)

floor.friction = 1.0
level.add(floor)


# =========================
# Scene Constants
# =========================

MENU = 0
GAME = 1

scene_state = MENU


# =========================
# Asset Loading
# =========================

asset_manager = AssetManager()

# Backgrounds
menu_bg_original = asset_manager.load_image(
    "menu_bg",
    "assets/images/Forest-Background.png"
)

game_bg_original = asset_manager.load_image(
    "game_bg",
    "assets/images/capybara-conquest-field-background.png"
)

# Player animation sheets
walk_sheet = asset_manager.load_image(
    "walk_sheet",
    "assets/images/walk.png"
)

idle_sheet = asset_manager.load_image(
    "idle_sheet",
    "assets/images/idle.png"
)

# Slice animations
walk_frames = SpriteSheet(walk_sheet).cut_strip(
    0, 0, 63, 63, 8
)

idle_frames = SpriteSheet(idle_sheet).cut_strip(
    0, 0, 63, 63, 8
)

# Animation dictionary
player_animations = {
    "walk": Animation(walk_frames, 0.1),
    "idle": Animation(idle_frames, 0.7)
}

# Create player
player = Player(
    400,
    300,
    100,
    player_animations,
    level
)


# =========================
# World Platforms
# =========================

WORLD_PLATFORMS = [
    ("flat-platform-chunk", 0, 0),
    ("ladder-platform-chunk", 300, 300)
]


# =========================
# UI
# =========================

title = FONT.render(
    "Capybara Conquest",
    True,
    (0, 0, 0)
)


def create_menu_buttons():
    center_x = screen.get_width() / 2 - 150

    play_button = widgets.Button(
        center_x,
        400,
        400,
        120,
        "Play",
        FONT,
        BACKGROUNDCOLOR
    )

    quit_button = widgets.Button(
        center_x,
        550,
        400,
        120,
        "Quit",
        FONT,
        BACKGROUNDCOLOR
    )

    return play_button, quit_button


play_button, quit_button = create_menu_buttons()


# =========================
# Helper Functions
# =========================

def get_scaled_background(
    image: pygame.Surface
) -> pygame.Surface:

    return pygame.transform.scale(
        image,
        (
            screen.get_width(),
            screen.get_height()
        )
    )


# =========================
# Main Loop
# =========================

running = True

while running:

    dt = clock.tick(FPS) / 1000

    mouse_pos = pygame.mouse.get_pos()

    # =====================
    # Events
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:

            # Recreate menu buttons
            play_button, quit_button = create_menu_buttons()

            # Recreate floor
            level.remove(floor)

            floor = pymunk.Segment(
                level.static_body,
                (0, screen.get_height() - 50),
                (screen.get_width(), screen.get_height() - 50),
                5
            )

            floor.friction = 1.0
            level.add(floor)

        if scene_state == MENU:

            if play_button.is_clicked(event):
                scene_state = GAME

            if quit_button.is_clicked(event):
                running = False

    # =====================
    # MENU
    # =====================

    if scene_state == MENU:

        background = get_scaled_background(
            menu_bg_original
        )

        play_button.update(mouse_pos)
        quit_button.update(mouse_pos)

        screen.blit(background, (0, 0))

        screen.blit(
            icon,
            (
                screen.get_width() / 2
                - icon.get_width() / 2,
                -40
            )
        )

        screen.blit(
            title,
            (
                screen.get_width() / 2
                - title.get_width() / 2,
                150
            )
        )

        play_button.draw(screen)
        quit_button.draw(screen)

    # =====================
    # GAME
    # =====================

    elif scene_state == GAME:

        background = get_scaled_background(
            game_bg_original
        )

        screen.blit(background, (0, 0))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.movement("left")

        if keys[pygame.K_RIGHT]:
            player.movement("right")

        if keys[pygame.K_UP]:
            player.movement("up")

        # Physics
        level.step(dt)

        # Update player
        player.update(dt)

        # Draw world
        level.debug_draw(draw_options)

        for tmx_data, offset_x, offset_y in WORLD_PLATFORMS:

            terrain.draw_tmx(
                screen,
                tmx_data,
                offset_x,
                offset_y
            )

        # Draw player
        player.draw(screen)

    # =====================
    # Render
    # =====================

    window.flip()

pygame.quit()