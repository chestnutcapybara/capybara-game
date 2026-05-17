import pygame
import pymunk
from animation import Animation
from constants import SCREEN_HEIGHT

class Player:
    def __init__(self, x, y, hp, animations: dict[str, Animation], space):
        self.hp = hp
        self.animations = animations
        self.current_state = "walk"
        self.facing_right = True

        # PhEsics
        self.mass = 1
        self.body = pymunk.Body(self.mass, float('inf'))
        self.body.position = (x, y)

        self.shape = pymunk.Poly.create_box(self.body, (100, 100))
        self.shape.friction = 0.75

        space.add(self.body, self.shape)

    def update(self, dt):
        if abs(self.body.velocity.x) > 10:
            self.current_state = "walk"
        else:
            self.current_state = "idle"
        self.animations[self.current_state].update(dt)
        if self.body.velocity.x > 5:
            self.facing_right = False
        elif self.body.velocity.x < -5:
            self.facing_right = True

    def draw(self, screen):
        image = pygame.transform.scale(self.animations[self.current_state].get_frame(), (128, 128))
        pos = self.body.position
        draw_x = pos.x
        draw_y = pos.y

        rect = image.get_rect(center=(draw_x, draw_y))

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        screen.blit(image, rect)


    def movement(self, direction):
        force = 500
        if direction == "left":
            self.body.apply_force_at_local_point((-force, 0))
        elif direction == "right":
            self.body.apply_force_at_local_point((force, 0))
        elif direction == "up":
            if self.body.velocity.y > -10:
                self.body.apply_impulse_at_local_point((0, -200))
