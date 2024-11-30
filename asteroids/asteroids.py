import pygame, random, image_utils, math
from ship import Ship
from asteroid import Asteroid
from lives import Lives
from menu import Menu
from alien import Alien

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
ALIEN_BONUS = 5
ALIEN_FREQUENCY = 10
ALIEN_BULLET_INTERVAL = 60
MINIMUM_SPACE_DISTANCE = 200
INITIAL_POS = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

#Mouse cursor invisible
pygame.mouse.set_visible(False)

#Set starting values
level = 0
lives = Lives(display_surface, (WINDOW_WIDTH - 10, 10))
score = 0
frame = 0
waiting_to_spawn = True

gameMenu = Menu(display_surface)

#Crash sound effect
crash_sound = pygame.mixer.Sound("asteroids/assets/Crash.mp3")
crash_sound.set_volume(1)

pygame.mixer_music.load("asteroids/assets/Flying_saucer.mp3")

#Set font and score text
font = pygame.font.SysFont('callibri', 48)
large_font = pygame.font.SysFont('callibri', 60)
score_text = font.render("Score: " + str(score), True, GREEN, BLACK)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

def create_asteroids(level): 
    ''' create a list of asteroids for the specified level '''
    asteroids = pygame.sprite.Group()
    for i in range(level+1):
        asteroid = Asteroid((random.randrange(0, WINDOW_WIDTH), random.randrange(0, WINDOW_HEIGHT)), 2)
        asteroids.add(asteroid)
    return asteroids

asteroids_group = create_asteroids(level)

ship = Ship(INITIAL_POS, level)
ship_group = pygame.sprite.GroupSingle(ship)
aliens_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
alien_bullets_group = pygame.sprite.Group()

def has_collided(asteroids, ship_group):
    ''' check if the ship has collided with an asteroid '''
    collisions = pygame.sprite.groupcollide(asteroids, ship_group, False, False, image_utils.intersects)
    collided = False
    for ast, shp in collisions.items():
        collided = collided or shp 
    return collided

def bullet_collision(targets, bullets):
    ''' check if any asteroid has been hit by a bullet, if it has remove the bullet and return the asteroid that has hit '''
    collisions = pygame.sprite.groupcollide(targets, bullets, False, True, image_utils.intersects)
    for target, blt in collisions.items():
        if blt:
            return target
    return None

def any_alien_visible():
    result = False
    for alien in aliens_group.sprites():
        result = result or alien.visible
    return result

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_to(pos, sprites):
    result = None
    for sprite in sprites:
        distance = calculate_distance(pos, sprite.pos)
        if result == None or distance < result:
            result = distance
    return result

def has_space(pos):
    closest_asteroid = closest_to(pos, asteroids_group.sprites())
    closest_alien = closest_to(pos, aliens_group.sprites())
    closest_bullet = closest_to(pos, alien_bullets_group.sprites())
    return (closest_asteroid == None or closest_asteroid > MINIMUM_SPACE_DISTANCE) and (closest_alien == None or closest_alien > MINIMUM_SPACE_DISTANCE) and (closest_bullet == None or closest_bullet > MINIMUM_SPACE_DISTANCE)

#Main game loop
running = True
while running:
    for event in pygame.event.get():
        #Does user want to quit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            gameMenu.key_pressed(event.key)
            if event.key == pygame.K_UP:
                ship.start_thrust()
            if event.key == pygame.K_SPACE:
                if lives.game_over():
                    #Reset game
                    lives.reset()
                    level = 0
                    score = 0
                    asteroids_group = create_asteroids(level)
                    bullets_group.empty()
                    aliens_group.empty()
                    alien_bullets_group.empty()
                    ship.set_level(0)
                    waiting_to_spawn = True
                else:    
                    if ship.visible:
                        #Shoot bullets
                        bullets_group.add(ship.shoot())
            if event.key == pygame.K_ESCAPE:
                #Quit game
                running = False
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                #Stop thrusting
                ship.stop_thrust()
                    
        keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        #Rotate ship left
        ship.turn_left()
    if keys[pygame.K_RIGHT]:
        #Rotate ship right
        ship.turn_right()

    #Spaceship and asteroid collide
    collided = has_collided(asteroids_group, ship_group) or has_collided(aliens_group, ship_group)
    if collided:
        ship.reset()
        if ship.visible:
            lives.life_lost()
            waiting_to_spawn = True

    #Player bullet and alien collide
    alien_shot = bullet_collision(aliens_group, bullets_group)
    if alien_shot:
        alien_shot.dead()
        score += ALIEN_BONUS

    if not any_alien_visible():
        pygame.mixer.music.stop()
    
    #Player bullet and asteroid collide
    ast_hit = bullet_collision(asteroids_group, bullets_group)
    if ast_hit:
        crash_sound.play()
        score += 1
        asteroids_group.add(ast_hit.break_up())  # add any fragments that the astreoid creates when it's destroyed
        if score % ALIEN_FREQUENCY == 0:
            alien = Alien()
            alien.new_alien()
            aliens_group.add(alien)
            pygame.mixer.music.play(-1,0,0)

    #Alien bullet and ship collide
    alien_bullet_ship = bullet_collision(ship_group, alien_bullets_group)
    if alien_bullet_ship:
        ship.reset()
        if ship.visible:
            lives.life_lost()
            waiting_to_spawn = True

    #Hide ship if game over
    if lives.game_over() or collided:
        ship.hide()
        alien_bullets_group.empty()
    
    
    if waiting_to_spawn and has_space(INITIAL_POS):
        waiting_to_spawn = False
        ship.show()    

    #Level complete?
    if not asteroids_group:
        level += 1
        score += LEVEL_BONUS
        lives.bonus_life()
        ship.upgrade()
        lives.level = level
        asteroids_group = create_asteroids(level)
        bullets_group = pygame.sprite.Group()

    if aliens_group and frame % ALIEN_BULLET_INTERVAL == 0:
        for alien in aliens_group:
            alien_bullet = alien.shoot(ship)
            if alien_bullet:
                alien_bullets_group.add(alien_bullet)

    display_surface.fill((0,0,0))

    #Blit text
    score_text = font.render("Score: " + str(score), True, GREEN, BLACK)
    display_surface.blit(score_text, score_rect)
    lives.draw()


    #Update asteroids, bullets and ship groups
    asteroids_group.update()
    asteroids_group.draw(display_surface)
    if gameMenu.playing():
        bullets_group.update()
        bullets_group.draw(display_surface)
        ship_group.update()
        ship_group.draw(display_surface)
        aliens_group.update()
        aliens_group.draw(display_surface)
        alien_bullets_group.update()
        alien_bullets_group.draw(display_surface)

    #Blit game over text if game is over
    if lives.game_over():
        gameMenu.game_over()
    
    gameMenu.draw_menu()

    pygame.display.update()
    clock.tick(FPS)
    frame += 1

pygame.quit()