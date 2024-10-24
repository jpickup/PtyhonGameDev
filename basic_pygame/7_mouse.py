import pygame

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mouse")

dragon_left = pygame.image.load("Dragon_Left_64.png")
dragon_right = pygame.image.load("Dragon_Right_64.png")
dragon_image = dragon_right
dragon_rect = dragon_image.get_rect()
dragon_rect.centerx = WINDOW_WIDTH // 2
dragon_rect.bottom = WINDOW_HEIGHT


running = True
clicking = False
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.MOUSEBUTTONDOWN):
            print(event)
            dragon_rect.center = event.pos
            clicking = True
        if (event.type == pygame.MOUSEBUTTONUP):
            print(event)
            clicking = False
        if (event.type == pygame.MOUSEMOTION):
            if (clicking):
                dragon_rect.center = event.pos

    display_surface.fill((0,0,0))
    display_surface.blit(dragon_image, dragon_rect)

pygame.quit()