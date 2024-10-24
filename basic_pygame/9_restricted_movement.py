import pygame

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Continuous Keyboard with restrictions")

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
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        dragon_rect.x -= VELOCITY
        dragon_image = dragon_left
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        dragon_rect.x += VELOCITY
        dragon_image = dragon_right
    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        dragon_rect.y -= VELOCITY
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
        dragon_rect.y += VELOCITY

    if (dragon_rect.left < 0):
        dragon_rect.left = 0
    if (dragon_rect.right > WINDOW_WIDTH):
        dragon_rect.right = WINDOW_WIDTH
    if (dragon_rect.top < 0):
        dragon_rect.top = 0
    if (dragon_rect.bottom > WINDOW_HEIGHT):
        dragon_rect.bottom = WINDOW_HEIGHT


    display_surface.fill((0,0,0))
    display_surface.blit(dragon_image, dragon_rect)

    clock.tick(FPS)

pygame.quit()