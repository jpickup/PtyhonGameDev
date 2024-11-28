import pygame, random, math, image_utils

bullet1_image = pygame.image.load("asteroids/assets/bullet1.png")
bullet2_image = pygame.image.load("asteroids/assets/bullet2.png")
bullet3_image = pygame.image.load("asteroids/assets/bullet3.png")

bullet_images = [bullet1_image, bullet2_image, bullet3_image]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, velocity, level = 0):
        super().__init__()
        self.pos = pos
        self.angle = angle
        self.velocity = velocity
        self.level = level
        self.screen_width, self.screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.original_image = bullet_images[level % 3]
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect = self.image.get_rect()
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
            self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    def intersects(self, other):
        ''' check if the visible parts of this sprite intersect with the other sprite '''
        offset = (
            other.rect.left - self.rect.left,
            other.rect.top - self.rect.top)
        return self.mask.overlap(other.mask, offset)
