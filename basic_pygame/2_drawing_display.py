import pygame

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Drawing")

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)

display_surface.fill(BLUE)

pygame.draw.line(display_surface, RED, (0,0), (WINDOW_WIDTH, WINDOW_HEIGHT), 2)
pygame.draw.line(display_surface, YELLOW, (WINDOW_WIDTH,0), (0, WINDOW_HEIGHT), 2)

pygame.draw.circle(display_surface, GREEN, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), 100, 0)
pygame.draw.circle(display_surface, BLACK, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), 80, 0)

pygame.draw.rect(display_surface, RED, (50,50, 100, 40), 0)

running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

pygame.quit()