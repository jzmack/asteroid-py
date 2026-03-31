from circleshape import CircleShape
import pygame
from constants import *
import random
from pathlib import Path

class Asteroid(CircleShape):
    _base_image = None

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-60, 60)

        if Asteroid._base_image is None:
            asset_path = Path(__file__).resolve().parent / ASTEROID_IMAGE_PATH
            try:
                raw_image = pygame.image.load(asset_path).convert_alpha()
            except pygame.error:
                raw_image = None

            if raw_image is not None:
                bounding = raw_image.get_bounding_rect()
                if bounding.width and bounding.height:
                    raw_image = raw_image.subsurface(bounding).copy()
                Asteroid._base_image = raw_image

        self.original_image = None
        if Asteroid._base_image is not None:
            diameter = self.radius * 2
            image_width, image_height = Asteroid._base_image.get_size()
            scale = min(diameter / image_width, diameter / image_height)
            if scale != 1:
                size = (
                    max(1, int(image_width * scale)),
                    max(1, int(image_height * scale)),
                )
                self.original_image = pygame.transform.smoothscale(Asteroid._base_image, size)
            else:
                self.original_image = Asteroid._base_image.copy()

    def draw(self, screen):
        if self.original_image is not None:
            rotated = pygame.transform.rotate(self.original_image, -self.rotation)
            rect = rotated.get_rect(center=self.position)
            screen.blit(rotated, rect)
        else:
            pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation = (self.rotation + self.rotation_speed * dt) % 360

    def point_value(self):
        value = int(ASTEROID_SCORE_BASE * ASTEROID_MAX_RADIUS / self.radius)
        return max(value, 1)
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        split_angle = random.uniform(20, 50)
        split_asteroid_a = self.velocity.rotate(split_angle)
        split_asteroid_b = self.velocity.rotate(-split_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = split_asteroid_a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = split_asteroid_b * 1.2