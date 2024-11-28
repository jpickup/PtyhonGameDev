import pygame, random, math, image_utils

INITIAL_LIVES = 3


class Lives(pygame.sprite.Sprite):
    def __init__(self, surface, topright):
        self.surface = surface
        self.topright = topright
        self.lives = INITIAL_LIVES
        self.ship_image = pygame.image.load("asteroids/assets/ship1-64-stop.png")
        self.ship_rect = self.ship_image.get_rect()

    def reset(self):
        self.lives = INITIAL_LIVES

    def life_lost(self):
        self.lives -= 1

    def bonus_life(self):
        self.lives += 1

    def game_over(self):
        return self.lives < 0

    def draw(self):
        pos = self.topright
        rect = self.ship_rect
        rect.top = pos[1]
        for i in range(0, self.lives):
            rect.right = pos[0] - (i * (rect.width + 5))
            self.surface.blit(self.ship_image, rect)
