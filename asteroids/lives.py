import pygame, random, math, image_utils

INITIAL_LIVES = 3

class Lives(pygame.sprite.Sprite):
    def __init__(self, surface, topright):
        self.surface = surface
        self.topright = topright
        self.lives = INITIAL_LIVES
        self.level = 0
        self.ship_images = [
            pygame.image.load("asteroids/assets/ship1-64-stop.png"), 
            pygame.image.load("asteroids/assets/ship2-64-stop.png"),
            pygame.image.load("asteroids/assets/ship3-64-stop.png")]
    
        self.die_sound = pygame.mixer.Sound("asteroids/assets/ShipDie.mp3")
        self.die_sound.set_volume(1)

        self.game_over_sound = pygame.mixer.Sound("asteroids/assets/GameOver.mp3")
        self.game_over_sound.set_volume(1)

        self.level_up_sound = pygame.mixer.Sound("asteroids/assets/LevelUp.mp3")
        self.level_up_sound.set_volume(1)


    def reset(self):
        self.lives = INITIAL_LIVES
        self.level = 0

    def life_lost(self):
        self.lives -= 1
        if self.game_over():
            self.game_over_sound.play()
        else:
            self.die_sound.play()

    def bonus_life(self):
        self.lives += 1
        self.level_up_sound.play()

    def game_over(self):
        return self.lives < 1

    def draw(self):
        pos = self.topright
        ship_image = self.ship_images[self.level % 3]
        rect = ship_image.get_rect()
        rect.top = pos[1]
        for i in range(0, self.lives):
            rect.right = pos[0] - (i * (rect.width + 5))
            self.surface.blit(ship_image, rect)
