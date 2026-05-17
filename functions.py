from __future__ import annotations

import pygame
import json
import sys

from pathlib import Path
from typing import Any
import pytmx
from pytmx.util_pygame import load_pygame

from constants import *

if __name__ == "__main__":
    raise CapybaraConquestError("This file is not meant to be run directly, it contains utility functions for the game. Please run main.py instead.")


def resolve_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path

def load_font(path: str, font_size: int) -> pygame.font.Font:
    try:
        return pygame.font.Font(resolve_path(path), font_size)
    except FileNotFoundError:
        print(f"{resolve_path(path)} not found, defaulting to system font.")
        return pygame.font.SysFont(None, font_size)
    except Exception as exc:
        raise RuntimeError(f"Failed loading font from {path}, {exc}") from exc

def load_image(path: str, alpha: bool) -> pygame.Surface:
    try:
        if alpha is True:
            return pygame.image.load(resolve_path(path)).convert_alpha()
        return pygame.image.load(resolve_path(path)).convert()
    except FileNotFoundError:
        raise FileNotFoundError(f"{resolve_path(path)} not found!") from FileNotFoundError
    except Exception as exc:
        raise RuntimeError(f"Failed loading image from {path}, {exc}") from exc

def load_sound(path: str) -> pygame.mixer.Sound:
    try:
        return pygame.mixer.Sound(resolve_path(path))
    except FileNotFoundError:
        raise FileNotFoundError(f"{resolve_path(path)} not found!") from FileNotFoundError
    except Exception as exc:
        raise RuntimeError(f"Failed loading Sound from: {path}, {exc}") from exc

def open_json(path: str) -> Any:
    try:
        with open(resolve_path(path), "r") as f:
            return json.load(f)
    except OSError as exc:
        raise OSError(f"Failed to open {path}, {exc}") from exc

def draw_tmx(screen,name: str,offset_x: int, offset_y: int):
    tmx_data = load_pygame(f"assets/tiles/{name}.tmx")
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_image = tmx_data.get_tile_image_by_gid(gid)
                if tile_image:
                    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
                    screen.blit(tile_image, (x * tmx_data.tilewidth * (TILE_SIZE / tmx_data.tilewidth) + offset_x,
                                             y * tmx_data.tileheight * (TILE_SIZE / tmx_data.tileheight) + offset_y))