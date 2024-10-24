import pygame

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sound")

zap_sound = pygame.mixer.Sound("zap.wav")
power_up_sound = pygame.mixer.Sound("power_up.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

zap_sound.set_volume(0.1)
power_up_sound.set_volume(0.1)
explosion_sound.set_volume(0.1)

pygame.mixer.music.load("encounter.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0)

zap_sound.play()
pygame.time.delay(1000)
power_up_sound.play()
pygame.time.delay(1000)
explosion_sound.play()
pygame.time.delay(1000)


running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

pygame.quit()