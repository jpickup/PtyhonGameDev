import pygame, random

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
FPS = 150
clock = pygame.time.Clock()

score = 0
lives = 5

current_velocity = 1
clown_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT //2)
clown_velocity = (1,1)

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Basic")

background_image = pygame.image.load("catch-the-clown/background.png")
background_image_image_rect = background_image.get_rect()

clown_image = pygame.image.load("catch-the-clown/clown-64.png")
clown_image_rect = clown_image.get_rect()

hit_sound = pygame.mixer.Sound("catch-the-clown/clang.wav")
hit_sound.set_volume(0.3)
miss_sound = pygame.mixer.Sound("catch-the-clown/fart.wav")
miss_sound.set_volume(1)
game_over_sound = pygame.mixer.Sound("catch-the-clown/wah-wah.mp3")
game_over_sound.set_volume(1)

font = pygame.font.SysFont('comicsansms', 64)
score_text = font.render("Score: " + str(score), True, YELLOW, BLACK)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

lives_text = font.render("Lives: " + str(lives), True, MAGENTA, BLACK)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10,10)

large_font = pygame.font.SysFont('comicsansms', 128)
game_over_text = large_font.render("GAME OVER", True, CYAN, YELLOW)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Press any key to play again", True, YELLOW, CYAN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 120)

def random_velocity(velocity):
    x = (random.randint(0,1) * 2 -1) * velocity
    y = (random.randint(0,1) * 2 -1) * velocity
    return (x,y)

def move_clown(clown_pos, clown_velocity):
    return (clown_pos[0] + clown_velocity[0], clown_pos[1] + clown_velocity[1])

def bounce_clown(clown_rect, clown_velocity):
    if (clown_rect.right >= WINDOW_WIDTH or clown_rect.left <= 0):
        clown_velocity = (-clown_velocity[0], clown_velocity[1])
    if (clown_rect.bottom >= WINDOW_HEIGHT or clown_rect.top <= 0):
        clown_velocity = (clown_velocity[0], -clown_velocity[1])
    return clown_velocity

def rect_contains_point(rect, point):
    return point[0] > rect.left and point[0] < rect.right and point[1] > rect.top and point[1] < rect.bottom

def game_over():
    return lives <= 0

def dodge_cursor(mouse_pos, clown_rect, clown_pos):
    if (rect_contains_point(clown_rect, mouse_pos)):
        if mouse_pos[0] > WINDOW_WIDTH // 2:
            return (mouse_pos[0] - clown_rect.width, mouse_pos[1])
        else:    
            return (mouse_pos[0] + clown_rect.width, mouse_pos[1])
    else:
        return clown_pos

pygame.mixer.music.load("catch-the-clown/circus.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1,0)


running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.MOUSEBUTTONDOWN and not(game_over())):
            if rect_contains_point(clown_image_rect,event.pos):
                score += 1
                current_velocity = (score + 4) // 5
                clown_velocity = random_velocity(current_velocity)
                hit_sound.play()
            else:
                lives -= 1
                if game_over():
                    pygame.mixer.music.stop()
                    game_over_sound.play()
                else:
                    miss_sound.play()
        if (event.type == pygame.KEYDOWN):
            if game_over():
                score = 0
                lives = 5
                current_velocity = 1
                pygame.mixer.music.play(-1,0)
        if (event.type == pygame.MOUSEMOTION):
            if (score >= 5):
                clown_pos = dodge_cursor(event.pos, clown_image_rect, clown_pos)    

    display_surface.blit(background_image, background_image_image_rect)

    if game_over():
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
    else:    
        clown_pos = move_clown(clown_pos, clown_velocity)
        clown_image_rect.center = clown_pos
        score_text = font.render("Score: " + str(score), True, YELLOW, BLACK)
        lives_text = font.render("Lives: " + str(lives), True, MAGENTA, BLACK)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(clown_image, clown_image_rect)
        clown_velocity = bounce_clown(clown_image_rect, clown_velocity)

    clock.tick(FPS)

pygame.quit()