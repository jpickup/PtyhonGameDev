import pygame, random, math, image_utils

bullet_image = pygame.image.load("asteroids/assets/bullet.png")

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, velocity):
        super().__init__()
        self.pos = pos
        self.angle = angle
        self.velocity = velocity
        self.screen_width, self.screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.original_image = bullet_image
        self.image = bullet_image
        self.rect = bullet_image.get_rect()
        w, h = self.original_image.get_size()
        self.centre = w // 2, h // 2

    def update(self):
            self.pos = ((self.pos[0] + self.velocity[0]), 
                        (self.pos[1] + self.velocity[1]))
            
            # check if we are outside the screen
            if self.pos[0] < 0 or self.pos[0] > self.screen_width or self.pos[1] < 0 or self.pos[1] > self.screen_height:
                self.kill()
            (img, rect) = image_utils.rotate(self.original_image, self.pos, self.centre, -self.angle)
            self.image = img
            self.rect = rect