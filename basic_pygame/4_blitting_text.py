import pygame

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 300

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Text")

GREEN = (0,255,0)
DARK_GREEN = (10,50,10)
BLACK = (0,0,0)

fonts = pygame.font.get_fonts()
for font in fonts:
    print(font)

system_font = pygame.font.SysFont('damascus', 64)
custom_font = pygame.font.Font('StreetfunkGraffiti-woBdn.otf', 48)

system_text = system_font.render("Dragons Rule!", True, GREEN, DARK_GREEN)
system_text_rect = system_text.get_rect()
system_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

custom_text = custom_font.render("Move the dragon", True, GREEN)
custom_text_rect = custom_text.get_rect()
custom_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100)

font_idx = 0
FPS=1
clock= pygame.time.Clock()

running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
    system_font = pygame.font.SysFont(str(font), 64)
    system_text = system_font.render(str(font), True, GREEN, DARK_GREEN)
    system_text_rect = system_text.get_rect()
    system_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    display_surface.fill((0,0,0))

    display_surface.blit(system_text, system_text_rect)
    display_surface.blit(custom_text, custom_text_rect)

    font = fonts[font_idx]
    font_idx += 1


    clock.tick(FPS)

pygame.quit()