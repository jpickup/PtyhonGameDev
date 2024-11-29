import pygame, random, image_utils
from ship import Ship
from asteroid import Asteroid
from lives import Lives

pygame.init()

display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
FPS = 60
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
LEVEL_BONUS = 10

level = 0
lives = Lives(display_surface, (WINDOW_WIDTH - 10, 10))
score = 0

font = pygame.font.SysFont('callibri', 48)
large_font = pygame.font.SysFont('callibri', 60)
score_text = font.render("Score: " + str(score), True, GREEN, BLACK)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

game_over_text = large_font.render("GAME OVER", True, RED, BLACK)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
game_over_text2 = font.render("Press space to continue", True, RED, BLACK)
game_over_rect2 = game_over_text2.get_rect()
game_over_rect2.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)

def create_asteroids(level): 
    ''' create a list of asteroids for the specified level '''
    asteroids = pygame.sprite.Group()
    for i in range(level+1):
        asteroid = Asteroid((random.randrange(0, WINDOW_WIDTH), random.randrange(0, WINDOW_HEIGHT)), 2)
        asteroids.add(asteroid)
    return asteroids

asteroids_group = create_asteroids(level)

ship = Ship((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), level)
ship_group = pygame.sprite.GroupSingle(ship)
bullets_group = pygame.sprite.Group()

def ship_asteroid_collision(asteroids, ship_group):
    ''' check if the ship has collided with an asteroid '''
    collisions = pygame.sprite.groupcollide(asteroids, ship_group, False, False, image_utils.intersects)
    collided = False
    for ast, shp in collisions.items():
        collided = collided or shp 
    return collided

def bullet_asteroid_collision(asteroids, bullets):
    ''' check if any asteroid has been hit by a bullet, if it has remove the bullet and return the asteroid that has hit '''
    collisions = pygame.sprite.groupcollide(asteroids, bullets, False, True, image_utils.intersects)
    for ast, blt in collisions.items():
        if blt:
            return ast
    return None

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                if lives.game_over():
                    lives.reset()
                    level = 0
                    score = 0
                    asteroids_group = create_asteroids(level)
                    bullets_group = pygame.sprite.Group()
                    ship.set_level(0)
                else:    
                    if ship.visible:
                        bullets_group.add(ship.shoot())
            if (event.key == pygame.K_ESCAPE):
                pygame.quit()
                    
        keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT]):
        ship.turn_left()
    if (keys[pygame.K_RIGHT]):
        ship.turn_right()
    if (keys[pygame.K_UP]):
        ship.accelerate()

    collided = ship_asteroid_collision(asteroids_group, ship_group)
    if collided:
        if ship.visible:
            lives.life_lost()
        ship.reset()
    
    ast_hit = bullet_asteroid_collision(asteroids_group, bullets_group)
    if ast_hit:
        score += 1
        asteroids_group.add(ast_hit.break_up())  # add any fragments that the astreoid creates when it's destroyed

    if lives.game_over() or collided:
        ship.hide()
    else:
        ship.show()    

    # level complete?
    if not asteroids_group:
        level += 1
        score += LEVEL_BONUS
        lives.bonus_life()
        ship.upgrade()
        asteroids_group = create_asteroids(level)
        bullets_group = pygame.sprite.Group()

    display_surface.fill((0,0,0))

    score_text = font.render("Score: " + str(score), True, GREEN, BLACK)
    display_surface.blit(score_text, score_rect)
    lives.draw()

    asteroids_group.update()
    asteroids_group.draw(display_surface)
    bullets_group.update()
    bullets_group.draw(display_surface)
    ship_group.update()
    ship_group.draw(display_surface)

    if lives.game_over():
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(game_over_text2, game_over_rect2)

    pygame.display.update()

pygame.quit()