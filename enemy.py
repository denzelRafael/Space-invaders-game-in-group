
import pygame
import random

class Enemy:
    def __init__(self, x, y, image, speed_multiplier=1):
        self.x = float(x)
        self.y = float(y)

        self.image = pygame.transform.scale(image, (40, 40))
        self.width = 40
        self.height = 40

        self.rect = self.image.get_rect(
            topleft=(x, y)
        )

        # Each alien gets its own direction and speed
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.8, 1.5)*speed_multiplier
        self.speed_y = random.choice([-1, 1]) * random.uniform(0.2, 0.7)*speed_multiplier

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):

        # Move independently
        self.x += self.speed_x
        self.y += self.speed_y

        # LEFT boundary
        if self.x <= 0:
            self.x = 0
            self.speed_x = abs(self.speed_x)

        # RIGHT boundary
        elif self.x + self.width >= 800:
            self.x = 800 - self.width
            self.speed_x = -abs(self.speed_x)

        # TOP boundary
        if self.y <= 30:
            self.y = 30
            self.speed_y = abs(self.speed_y)

        # BOTTOM boundary
        elif self.y + self.height >= 430:
            self.y = 430 - self.height
            self.speed_y = -abs(self.speed_y)

        # Update the rectangle's position
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
