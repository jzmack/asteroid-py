from circleshape import CircleShape
import pygame
from constants import *
from pathlib import Path
import random

class Shot(CircleShape):
    _base_image = None

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

        if Shot._base_image is None:
            asset_path = Path(__file__).resolve().parent / SHOT_IMAGE_PATH
            try:
                raw_image = pygame.image.load(asset_path).convert_alpha()
            except pygame.error:
                raw_image = None

            if raw_image is not None:
                bounding = raw_image.get_bounding_rect()
                if bounding.width and bounding.height:
                    raw_image = raw_image.subsurface(bounding).copy()
                Shot._base_image = raw_image

        self.original_image = None
        if Shot._base_image is not None:
            diameter = self.radius * 2
            image_w, image_h = Shot._base_image.get_size()
            scale = min(diameter / image_w, diameter / image_h)
            if scale != 1:
                size = (max(1, int(image_w * scale)), max(1, int(image_h * scale)))
                self.original_image = pygame.transform.smoothscale(Shot._base_image, size)
            else:
                self.original_image = Shot._base_image.copy()

    def draw(self, screen):
        if self.original_image is not None:
            rotated = pygame.transform.rotate(self.original_image, -self.rotation)
            rect = rotated.get_rect(center=self.position)
            screen.blit(rotated, rect)
        else:
            pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt