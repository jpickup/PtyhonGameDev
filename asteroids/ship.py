import pygame, random, math, image_utils
from bullet import Bullet

ROTATE_SPEED = 3
MAX_VELOCITY = 15
MAX_VELOCITY_SQUARED = MAX_VELOCITY * MAX_VELOCITY
ACCEL = 0.25
BULLET_VELOCITY = 6

ship1_go_image = pygame.image.load("asteroids/assets/ship1-64-go.png")
ship1_stop_image = pygame.image.load("asteroids/assets/ship1-64-stop.png")
ship2_go_image = pygame.image.load("asteroids/assets/ship2-64-go.png")
ship2_stop_image = pygame.image.load("asteroids/assets/ship2-64-stop.png")
ship3_go_image = pygame.image.load("asteroids/assets/ship3-64-go.png")
ship3_stop_image = pygame.image.load("asteroids/assets/ship3-64-stop.png")
blank_image = pygame.image.load("asteroids/assets/blank.png")

ship1_images = [ship1_go_image, ship1_stop_image]
ship2_images = [ship2_go_image, ship2_stop_image]
ship3_images = [ship3_go_image, ship3_stop_image]

ship_images = [ship1_images, ship2_images, ship3_images]

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos, level):
        super().__init__()
        self.screen_width, self.screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.image = ship_images[0][0]
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        w, h = self.image.get_size()
        self.centre = w // 2, h // 2
        self.thrust = False
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.velocity = (0, 0)
        self.angle = 0
        self.level = level
        self.initial_pos = pos
        self.pos = pos
        self.visible = True

    def upgrade(self):
        self.level += 1

    def set_level(self, level):
        self.level = level

    def turn_left(self):
        self.angle = (self.angle - ROTATE_SPEED) % 360

    def turn_right(self):
        self.angle = (self.angle + ROTATE_SPEED) % 360

    def reset(self):
        self.thrust = False
        self.angle = 0
        self.pos = self.initial_pos
        self.velocity = (0, 0)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def accelerate(self):
        radangle = math.radians(self.angle)
        self.velocity = (self.velocity[0] + math.sin(radangle) * ACCEL, 
                         self.velocity[1] - math.cos(radangle) * ACCEL)
        if ((self.velocity[0] * self.velocity[0]) + (self.velocity[1] * self.velocity[1]) > MAX_VELOCITY_SQUARED):
            excess = math.sqrt(self.velocity[0] * self.velocity[0] + (self.velocity[1] * self.velocity[1])) / MAX_VELOCITY
            self.velocity = (self.velocity[0] / excess, 
                             self.velocity[1] / excess)
        self.thrust = True

    def update(self):
        if self.visible:
            if self.thrust:
                self.original_image = ship_images[self.level % 3][0]
            else:
                self.original_image = ship_images[self.level % 3][1]
            self.thrust = False

            self.pos = ((self.pos[0] + self.velocity[0]) % self.screen_width, 
                        (self.pos[1] + self.velocity[1]) % self.screen_height)

            (img, rect) = image_utils.rotate(self.original_image, self.pos, self.centre, -self.angle)

            self.image = img
            self.rect = rect
        else:
            self.image = blank_image
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    def shoot(self):
        radangle = math.radians(self.angle)
        bullet_velocity = (self.velocity[0] + math.sin(radangle) * BULLET_VELOCITY, 
                         self.velocity[1] - math.cos(radangle) * BULLET_VELOCITY)
        return Bullet(self.pos, self.angle, bullet_velocity, self.level)

    def intersects(self, other):
        offset = (
            other.rect.left - self.rect.left,
            other.rect.top - self.rect.top)
        return self.mask.overlap(other.mask, offset)
