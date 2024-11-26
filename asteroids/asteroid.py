import pygame, random, image_utils

asteroid1_small_image = pygame.image.load("asteroids/assets/asteroid1-64.png")
asteroid2_small_image = pygame.image.load("asteroids/assets/asteroid2-64.png")
asteroid3_small_image = pygame.image.load("asteroids/assets/asteroid3-64.png")
asteroid1_med_image = pygame.image.load("asteroids/assets/asteroid1-128.png")
asteroid2_med_image = pygame.image.load("asteroids/assets/asteroid2-128.png")
asteroid3_med_image = pygame.image.load("asteroids/assets/asteroid3-128.png")
asteroid1_large_image = pygame.image.load("asteroids/assets/asteroid1-256.png")
asteroid2_large_image = pygame.image.load("asteroids/assets/asteroid2-256.png")
asteroid3_large_image = pygame.image.load("asteroids/assets/asteroid3-256.png")

asteroid_small_images = [asteroid1_small_image, asteroid2_small_image, asteroid3_small_image]
asteroid_med_images = [asteroid1_med_image, asteroid2_med_image, asteroid3_med_image]
asteroid_large_images = [asteroid1_large_image, asteroid2_large_image, asteroid3_large_image]

asteroid_images = [asteroid_small_images, asteroid_med_images, asteroid_large_images]

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()        
        self.screen_width, self.screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.original_image = asteroid_images[size][random.randint(0, 2)]
        self.image = self.original_image
        w, h = self.image.get_size()
        self.centre = w // 2, h // 2
        self.thrust = False
        self.spin = random.randint(-3, 3)
        self.angle = random.randint(0, 360)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.velocity = [random.randint(-5,5), random.randint(-5,5)]

    def update(self):
        self.angle = (self.angle + self.spin) % 360
        self.pos = ((self.pos[0] + self.velocity[0]) % self.screen_width, (self.pos[1] + self.velocity[1]) % self.screen_height)

        (img, rect) = image_utils.rotate(self.original_image, self.pos, self.centre, self.angle)
        #todo
        self.image = img
        self.rect = rect
