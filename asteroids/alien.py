import pygame, math, image_utils, random
from alien_bullet import AlienBullet

BULLET_VELOCITY = 5

ufo_image = pygame.image.load("asteroids/assets/UFO.png")
blank_image = pygame.image.load("asteroids/assets/blank.png")

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hit_sound = pygame.mixer.Sound("asteroids/assets/UFO_explosion.mp3")
        self.hit_sound.set_volume(1)
        self.visible = False
        self.screen_width, self.screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.velocity = [0, 0]
        self.pos = [0, 0]
        self.tick = 0
        self.start_y = 0
        self.end_y = 0
        self.slope = 0
        self.image = blank_image
        self.rect = blank_image.get_rect()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def shoot(self, ship):
        if self.visible:
            delta_x = ship.pos[0] - self.pos[0]
            delta_y = ship.pos[1] - self.pos[1]
            distance = math.sqrt(delta_x * delta_x + delta_y * delta_y)
            angle = math.atan(delta_x/delta_y) * 180 / math.pi
            velocity = [delta_x / distance * BULLET_VELOCITY, delta_y / distance * BULLET_VELOCITY]
            bullet = AlienBullet(self.pos, angle, velocity)
            return bullet
        else:
            return None

    def new_alien(self):
        self.tick = 0
        self.start_y = random.randint(50, self.screen_height - 50)
        self.end_y = random.randint(50, self.screen_height - 50)
        self.slope = (self.end_y - self.start_y)/self.screen_width
        if random.random() > 0.5:
            self.pos = [1, self.start_y]
            self.velocity = [2, self.slope]
        else:
            self.pos = [self.screen_width - 1, self.start_y]
            self.velocity = [-2, self.slope]
        self.show()

    def off_screen(self):
        return self.pos[0] < 0 or self.pos[0] > self.screen_width or self.pos[1] < 0 or self.pos[1] > self.screen_height

    def update(self):
        self.tick += 1
        self.pos = ((self.pos[0] + self.velocity[0]), 
                    (self.start_y + self.tick * self.velocity[1]))
        
        if self.off_screen():
            self.hide()

        if self.visible:
            self.rect = ufo_image.get_rect()
            self.rect.center = self.pos

            self.image = ufo_image
        else:
            self.image = blank_image
            self.rect = blank_image.get_rect()
    
    def dead(self):
        self.hide()
        self.hit_sound.play()
