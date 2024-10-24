import pygame
import random

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Collision detection")

font = pygame.font.SysFont('calibri', 20)

VELOCITY = 1
dragon_left = pygame.image.load("Dragon_Left_64.png")
dragon_right = pygame.image.load("Dragon_Right_64.png")
dragon_image = dragon_right
dragon_rect = dragon_image.get_rect()
dragon_rect.topleft = (25,25)

coin_image = pygame.image.load("Coin_64.png")
coin_rect = coin_image.get_rect()
coin_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

collision_sound = pygame.mixer.Sound("zap.wav")
collision_sound.set_volume(0.1)

FPS = 150
clock = pygame.time.Clock()

score = 0

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

    if (dragon_rect.left < 0):
        dragon_rect.left = 0
    if (dragon_rect.right > WINDOW_WIDTH):
        dragon_rect.right = WINDOW_WIDTH
    if (dragon_rect.top < 0):
        dragon_rect.top = 0
    if (dragon_rect.bottom > WINDOW_HEIGHT):
        dragon_rect.bottom = WINDOW_HEIGHT

    if (dragon_rect.colliderect(coin_rect)):
        coin_rect.center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
        score += 1
        collision_sound.play()

    score_text = "Score : " + str(score)
    custom_text = font.render(score_text, True, (255,0,0))
    custom_text_rect = custom_text.get_rect()
    custom_text_rect.center = (WINDOW_WIDTH//2, 12)

    display_surface.fill((0,0,0))
    display_surface.blit(dragon_image, dragon_rect)
    display_surface.blit(coin_image, coin_rect)

    display_surface.blit(custom_text, custom_text_rect)

    clock.tick(FPS)

pygame.quit()