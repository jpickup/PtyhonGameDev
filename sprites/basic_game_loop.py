import pygame

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FPS = 60

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Basic")
clock = pygame.time.Clock()


running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

    clock.tick(FPS)

pygame.quit()