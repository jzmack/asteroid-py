from circleshape import *
from constants import *
from pathlib import Path
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

        asset_path = Path(__file__).resolve().parent / PLAYER_IMAGE_PATH
        try:
            self.original_image = pygame.image.load(asset_path).convert_alpha()
        except pygame.error:
            self.original_image = None

        if self.original_image is not None:
            bounding = self.original_image.get_bounding_rect()
            if bounding.width and bounding.height:
                self.original_image = self.original_image.subsurface(bounding).copy()
                self.original_image = pygame.transform.rotate(self.original_image, 180)

            diameter = PLAYER_RADIUS * 2
            image_width, image_height = self.original_image.get_size()
            scale = min(diameter / image_width, diameter / image_height)
            if scale != 1:
                size = (
                    max(1, int(image_width * scale)),
                    max(1, int(image_height * scale)),
                )
                self.original_image = pygame.transform.smoothscale(self.original_image, size)
            self.image = self.original_image
        else:
            self.image = None

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        if self.image is not None:
            rotated = pygame.transform.rotate(self.original_image, -self.rotation)
            rect = rotated.get_rect(center=self.position)
            screen.blit(rotated, rect)
        else:
            pygame.draw.polygon(screen, color="white", points=self.triangle(), width=2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return
        self.timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.rotation = self.rotation  # offset for 180° player image rotation
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED