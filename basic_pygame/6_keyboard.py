import pygame

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Keyboard")

VELOCITY = 10

dragon_left = pygame.image.load("Dragon_Left_64.png")
dragon_right = pygame.image.load("Dragon_Right_64.png")
dragon = dragon_right
dragon_rect = dragon.get_rect()
dragon_rect.centerx = WINDOW_WIDTH // 2
dragon_rect.bottom = WINDOW_HEIGHT

running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN):
            print(event)
            if (event.key == pygame.K_LEFT):
                dragon_rect.x -= VELOCITY
                dragon = dragon_left

            if (event.key == pygame.K_RIGHT):
                dragon_rect.x += VELOCITY
                dragon = dragon_right

            if (event.key == pygame.K_UP):
                dragon_rect.y -= VELOCITY

            if (event.key == pygame.K_DOWN):
                dragon_rect.y += VELOCITY


    display_surface.fill((0,0,0))
    display_surface.blit(dragon, dragon_rect)

pygame.quit()