'''
 --- assets.py ---
This module includes the classes SpriteSheet and AssetManager which are used to manage assets such as images and animations.
AssetManager is used to load and store images in a cache, so that they can be easily reused without having to load them from disk multiple times.
'''

# Imports
from __future__ import annotations
from typing import cast
from unicodedata import name
import pygame
from pathlib import Path

class SpriteSheet:
    ''' The SpriteSheet class which is used to slice and dice sprite sheets into individual sprites '''
    def __init__(self, image: pygame.Surface):
        self.sheet = image

    def cut(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> pygame.Surface:
        ''' Cuts a sprite from the sprite sheet (most basic cutting method) '''
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        sprite.blit(
            self.sheet,
            (0, 0),
            (x, y, width, height),
        )

        return sprite.convert_alpha()

    def cut_strip(
        self,
        start_x: int,
        y: int,
        width: int,
        height: int,
        amount: int,
    ) -> list[pygame.Surface]:
        """ Cuts sprites lined up horizontally: ie, [capybara1, capybara2, capybara3, ...] """

        sprites = []

        for i in range(amount):
            x = start_x + (i * width)

            sprite = self.cut(
                x,
                y,
                width,
                height,
            )

            sprites.append(sprite)

        return sprites

##################
## Asset Manager #
##################

class AssetManager:
    ''' ### Grandmaster class of Asset Management, used to load and store images in a cache.

        METHODS: load_image, get_image, unload_image, clear

    '''
    def __init__(self):
        # Stores already-loaded images
        self.assets: dict[str, pygame.Surface | list[pygame.Surface]] = {}

    ######################
    ## Image Management ##
    ######################

    def load_image(
        self,
        name: str,
        path: str | Path,
        convert_alpha: bool = True,
    ) -> pygame.Surface:
        ''' Most fundemental function of Asset Manager. Checks if image is already loaded, if not, loads it and stores it in the cache. '''

        # Return cached version if already loaded
        if name in self.assets:
            return self.assets[name]

        image = pygame.image.load(path)

        # performance
        if convert_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()

        self.assets[name] = image
        return image

    def get_image(self, name: str) -> pygame.Surface | list[pygame.Surface]:
        ''' Acquires an image or animation frames from the cache and raises KeyError if the asset is not in cache.'''

        if name not in self.assets:
            raise KeyError(f'Image "{name}" has not been loaded.')

        return self.assets[name]

    def unload_image(self, name: str) -> None:
        ''' Unloads an image from the cache, making the RAM usage less after it is garbage collected by Python. '''

        if name in self.assets:
            del self.assets[name]

    def flip(
    self,
    source,
    name: str,
    flip_x: bool = True,
    flip_y: bool = False,
) -> pygame.Surface | list[pygame.Surface]:
        ''' Flips and caches images or animation frames '''

        flipped_name = f'{name}_flip_{flip_x}_{flip_y}'

        # Return cached version
        if flipped_name in self.assets:
            return self.assets[flipped_name]

        # Single image
        if isinstance(source, pygame.Surface):
            flipped = pygame.transform.flip(
            source,
            flip_x,
            flip_y,
            )

        # Animation frames
        elif isinstance(source, list):
            flipped = [
            pygame.transform.flip(
                frame,
                flip_x,
                flip_y,
            )
            for frame in source
            ]

        else:
            raise TypeError(
                'Source must be pygame.Surface or list[pygame.Surface]'
            )

        # Cache result
        self.assets[flipped_name] = flipped

        return flipped


    #####################
    ## Utility Methods ##
    #####################

    def clear(self) -> None:
        ''' Kicks everything out of the cache. Use at your own risk!!! >:) '''

        self.assets.clear()