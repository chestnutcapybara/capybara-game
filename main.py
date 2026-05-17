'''
 --- main.py ---
This is the main file for Capybara Conquest. It is the heart and soul of the game.
'''

# Imports
from __future__ import annotations

from pymunk import space
from constants import *

import pygame #type:ignore
import assets
import widgets
import terrain
import animation
import pymunk.pygame_util
from player import Player as _player
from assets import AssetManager, SpriteSheet
from animation import Animation

# Variables
title = FONT.render("Capybara Conquest", True, (0, 0, 0))

pygame.init()
pygame.display.init()

# Load icon first
icon = pygame.image.load("icon.ico")

win = pygame.window.Window(
    title="Capybara Conquest",
    size=(SCREEN_WIDTH, SCREEN_HEIGHT),
    resizable=True
)

# Set the window icon
win.set_icon(icon)
win.maximize()

screen = win.get_surface()
clock = pygame.time.Clock()
FPS = 60

SCREEN_HEIGHT = screen.get_height()
SCREEN_WIDTH = screen.get_width()

# Load TMX maps
WORLD_PLATFORMS = []
WORLD_PLATFORMS.append(("flat-platform-chunk", 0, 0))
WORLD_PLATFORMS.append(("ladder-platform-chunk", 300, 300))

# asset manager stuf
asset_manager = assets.AssetManager()
player_walk_spritesheet = asset_manager.load_image("Capybara Walking SpriteSheet", "assets/images/walk.png")

#player

draw_options = pymunk.pygame_util.DrawOptions(screen)
asset_manager = AssetManager()
walk_sheet_img = asset_manager.load_image("walk_sheet", "assets/images/walk.png")
sheet_slicer = SpriteSheet(walk_sheet_img)
walk_frames = sheet_slicer.cut_strip(0, 0, 63, 63, 8) 
idle_sheet_img = asset_manager.load_image("idle_sheet", "assets/images/idle.png")
idle_slicer = SpriteSheet(idle_sheet_img)
idle_frames = idle_slicer.cut_strip(0, 0, 63, 63, 8) 
player_anims = {
    "walk": Animation(walk_frames, 0.1),
    "idle": Animation(idle_frames, 0.7)
}
Player = _player(0,0,100, player_anims, level)


running = True

scene_state = "menu"

PLAYBUTTON = widgets.Button(SCREEN_WIDTH/2 - 150, 400, 400, 120, "Play", FONT, BACKGROUNDCOLOR)
QUITBUTTON = widgets.Button(SCREEN_WIDTH/2 - 150, 550, 400, 120, "Quit", FONT, BACKGROUNDCOLOR)

while running:

    dt = clock.tick(FPS) / 1000  # Delta time in seconds.

    if scene_state == "menu":
        SCREEN_HEIGHT = screen.get_height()
        SCREEN_WIDTH = screen.get_width()
        PLAYBUTTON = widgets.Button(SCREEN_WIDTH/2 - 150, 400, 400, 120, "Play", FONT, BACKGROUNDCOLOR) #Keep this there so it updates to the new screen width
        QUITBUTTON = widgets.Button(SCREEN_WIDTH/2 - 150, 550, 400, 120, "Quit", FONT, BACKGROUNDCOLOR)
        #Keep the following line for resizablitlty reasons
        FIELD_BACKGROUND = pygame.transform.scale(asset_manager.load_image("Forest Background","assets/images/Forest-Background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        PLAYBUTTON.update(pygame.mouse.get_pos())
        QUITBUTTON.update(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif scene_state == "menu":
            if PLAYBUTTON.is_clicked(event):
                scene_state = "game"
            if QUITBUTTON.is_clicked(event):
                running = False

    if scene_state == "menu":
        screen.blit(FIELD_BACKGROUND, (0, 0))
        screen.blit(icon, (SCREEN_WIDTH/2 - icon.get_width()/2, -40))
        screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, 150))
        PLAYBUTTON.draw(screen)
        QUITBUTTON.draw(screen)

    elif scene_state == "game":
        FIELD_BACKGROUND = pygame.transform.scale(asset_manager.load_image("Field Background", "assets/images/capybara-conquest-field-background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(FIELD_BACKGROUND, (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            Player.movement("up")
        if keys[pygame.K_LEFT]:
            Player.movement("left")
        if keys[pygame.K_RIGHT]:
            Player.movement("right")
        level.step(dt)
        level.debug_draw(draw_options)
        Player.update(dt)
        Player.draw(screen)
        # game things here now...?
        for tmx_data, offset_x, offset_y in WORLD_PLATFORMS:
            terrain.draw_tmx(screen, tmx_data, offset_x, offset_y)

    win.flip()

pygame.quit()