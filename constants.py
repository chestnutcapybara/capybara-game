'''
 --- constants.py ---
This module includes constants that are used throughout the game, such as colors, screen dimensions, and other important values.
It also includes a custom error class CapybaraConquestError which is used to raise errors
'''
from __future__ import annotations
import pygame
import pymunk

pygame.font.init()

class CapybaraConquestError(Exception):
    ''' Custom error class for Capybara Conquest, inherits from the standard Exception class. '''
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

if __name__ == "__main__":
    raise CapybaraConquestError("This file is not meant to be run directly, it contains constants for the game. Please run main.py instead.")

BACKGROUNDCOLOR = (237, 199, 154)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FIELD_BACKGROUND = pygame.transform.scale(pygame.image.load("assets/images/capybara-conquest-field-background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font("assets/fonts/Capybara.ttf", 96)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Other
TILE_SIZE = 32

# Physics

level = pymunk.Space()
level.gravity = (0, 200)
floor_body = level.static_body
floor_shape = pymunk.Segment(floor_body, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 100)
floor_shape.friction = 75.0
level.add(floor_shape)