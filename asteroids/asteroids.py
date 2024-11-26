import pygame, random, os
from ship import Ship
from asteroid import Asteroid

pygame.init()

FPS = 60

#WINDOW_WIDTH = 1000
#WINDOW_HEIGHT = 1000
#display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

level = 0

asteroids = pygame.sprite.Group()
for i in range(4):
    asteroid = Asteroid((random.randrange(0, WINDOW_WIDTH), random.randrange(0, WINDOW_HEIGHT)), 2)
    asteroids.add(asteroid)

ships = pygame.sprite.Group()
ship = Ship((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), level)
ships.add(ship)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT]):
        ship.turn_left()
    if (keys[pygame.K_RIGHT]):
        ship.turn_right()
    if (keys[pygame.K_UP]):
        ship.accelerate()

    if (keys[pygame.K_SPACE]):
        pass  #fire bullet

    display_surface.fill((0,0,0))

    asteroids.update()
    asteroids.draw(display_surface)
    ships.update()
    ships.draw(display_surface)

    pygame.display.flip()

pygame.quit()