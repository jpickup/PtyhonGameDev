import pygame

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Continuous Keyboard")

VELOCITY = 1
dragon_left = pygame.image.load("Dragon_Left_64.png")
dragon_right = pygame.image.load("Dragon_Right_64.png")
dragon_image = dragon_right
dragon_rect = dragon_image.get_rect()
dragon_rect.bottom = WINDOW_HEIGHT
dragon_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

FPS = 150
clock = pygame.time.Clock()

running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT]):
        dragon_rect.x -= VELOCITY
        dragon_image = dragon_left
    if (keys[pygame.K_RIGHT]):
        dragon_rect.x += VELOCITY
        dragon_image = dragon_right
    if (keys[pygame.K_UP]):
        dragon_rect.y -= VELOCITY
    if (keys[pygame.K_DOWN]):
        dragon_rect.y += VELOCITY

    display_surface.fill((0,0,0))
    display_surface.blit(dragon_image, dragon_rect)

    clock.tick(FPS)

pygame.quit()