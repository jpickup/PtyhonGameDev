import pygame, os
from enum import Enum

dir_path = os.path.dirname(os.path.realpath(__file__))
assets_path = os.path.join(dir_path, "assets")

WHITE = (255, 255, 255)

class GameState(Enum):
    START = 1
    PLAYING = 2
    GAME_OVER = 3

class Menu():
    def __init__(self, display_surface):
        self.screen_width, self.screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        #Load font
        self.menu_font = pygame.font.Font(os.path.join(assets_path,"Sterion.ttf"), 64)
        #Render text
        self.title_text = self.menu_font.render("ASTEROIDS", True, WHITE)
        self.start_text = self.menu_font.render("PRESS SPACE TO BEGIN", True, WHITE)

        #Set game over text
        self.game_over_text = self.menu_font.render("GAME OVER", True, WHITE)
        self.game_over_rect = self.game_over_text.get_rect()
        self.game_over_rect.center = (self.screen_width // 2, self.screen_height // 2 - 100)
        self.game_over_text2 = self.menu_font.render("Press space to continue", True, WHITE)
        self.game_over_rect2 = self.game_over_text2.get_rect()
        self.game_over_rect2.center = (self.screen_width // 2, self.screen_height // 2 + 40)

        self.display_surface = display_surface

        self.game_state = GameState.START

    def draw_menu(self):
        if self.game_state == GameState.START:
            #Blit text
            self.display_surface.blit(self.title_text, (self.screen_width//2 - self.title_text.get_width()/2, self.screen_height//2 - 250))
            self.display_surface.blit(self.start_text, (self.screen_width//2 - self.start_text.get_width()/2, self.screen_height//2))

        if self.game_state == GameState.GAME_OVER:
            #Blit text
            self.display_surface.blit(self.game_over_text, self.game_over_rect)
            self.display_surface.blit(self.game_over_text2, self.game_over_rect2)

    def start_game(self):
        self.game_state = GameState.PLAYING

    def game_over(self):
        self.game_state = GameState.GAME_OVER
    
    def key_pressed(self, key):
         if key == pygame.K_SPACE:
            if self.game_state == GameState.START:
                self.start_game()

            if self.game_state == GameState.GAME_OVER:
                self.start_game()

    def playing(self):
        return self.game_state == GameState.PLAYING