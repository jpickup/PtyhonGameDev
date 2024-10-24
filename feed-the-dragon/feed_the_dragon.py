import pygame, random, math

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon")

FPS=100
clock= pygame.time.Clock()
score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY
coin_direction = -1

GREEN = (0,255,0)
DARK_GREEN = (10,50,10)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

font = pygame.font.SysFont('savoyelet', 32)
large_font = pygame.font.SysFont('savoyelet', 60)

score_text = font.render("Score: " + str(score), True, GREEN, BLACK)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

title_text = large_font.render("Feed the Dragon", True, RED, BLACK)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.top = 4

lives_text = font.render("Lives: " + str(player_lives), True, GREEN, BLACK)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10,10)

game_over_text = large_font.render("GAME OVER", True, GREEN, DARK_GREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Press any key to play again", True, GREEN, DARK_GREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 48)

coin_sound = pygame.mixer.Sound("coin_sound.wav")
coin_sound.set_volume(0.3)
miss_sound = pygame.mixer.Sound("miss_sound.wav")
miss_sound.set_volume(1)
roar_sound = pygame.mixer.Sound("roar.wav")
roar_sound.set_volume(1)

player_image_left = pygame.image.load("Dragon_Left_64.png")
player_image_right = pygame.image.load("Dragon_Right_64.png")
player_image = player_image_right
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT // 2

coin_image = pygame.image.load("coin_64.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 64)

fire_blank = pygame.image.load("blank.png")
fire_image1_R = pygame.image.load("fire1R.png")
fire_image2_R = pygame.image.load("fire2R.png")
fire_image3_R = pygame.image.load("fire3R.png")
fire_image4_R = pygame.image.load("fire4R.png")
fire_image1_L = pygame.image.load("fire1L.png")
fire_image2_L = pygame.image.load("fire2L.png")
fire_image3_L = pygame.image.load("fire3L.png")
fire_image4_L = pygame.image.load("fire4L.png")
fire_images_R = [fire_blank, fire_image1_R, fire_image2_R, fire_image3_R, fire_image4_R]
fire_images_L = [fire_blank, fire_image1_L, fire_image2_L, fire_image3_L, fire_image4_L]
fire_index = 0
fire_rect = fire_blank.get_rect()

pygame.mixer.music.load("BossBattle.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0)

def reset_coin():
    if coin_direction == -1:
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 64)
    else:
        coin_rect.x = - BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 64)


running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN):
            if player_lives == 0:
                pygame.mixer.music.load("BossBattle.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1,0)
                score = 0
                player_lives = PLAYER_STARTING_LIVES
                coin_velocity = COIN_STARTING_VELOCITY
                player_image = player_image_right
                reset_coin()
            elif event.key == pygame.K_SPACE:
                fire_index = 1
                roar_sound.play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.top -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.top += PLAYER_VELOCITY
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.left -= PLAYER_VELOCITY
        player_image = player_image_left
    if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
        player_rect.left += PLAYER_VELOCITY
        player_image = player_image_right

    if player_lives > 0:
        if (coin_direction == -1 and coin_rect.x < 0) or (coin_direction == 1 and coin_rect.x > WINDOW_WIDTH):
            player_lives -= 1
            miss_sound.play()
            reset_coin()
        else:
            coin_rect.x += coin_velocity * coin_direction

        if player_rect.colliderect(coin_rect) or fire_rect.colliderect(coin_rect):
            score += 1
            coin_sound.play()
            coin_velocity += COIN_ACCELERATION
            coin_direction = ((score // 5) % 2) * 2 - 1
            reset_coin()

    score_text = font.render("Score: " + str(score), True, GREEN, BLACK)
    lives_text = font.render("Lives: " + str(player_lives), True, GREEN, BLACK)

    display_surface.fill(BLACK)

    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)    

    if player_lives <= 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
    else:    
        display_surface.blit(player_image, player_rect)
        if player_image == player_image_left:
            fire_image = fire_images_L[math.trunc(fire_index)]
            fire_rect = fire_image.get_rect()
            fire_rect.topright = player_rect.topleft
        else:
            fire_image = fire_images_R[math.trunc(fire_index)]
            fire_rect = fire_image.get_rect()
            fire_rect.topleft = player_rect.topright
        display_surface.blit(fire_image, fire_rect)
        display_surface.blit(coin_image, coin_rect)

    if (fire_index > 0): 
        fire_index += 0.25
    if (fire_index >= len(fire_images_L)):
        fire_index = 0
    
    pygame.draw.line(display_surface, WHITE, (0,64), (WINDOW_WIDTH, 64), 2)

    clock.tick(FPS)

pygame.quit()