import pygame, math, random

pygame.init()
sign = lambda x: math.copysign(1, x) 

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
GREEN = (0,255,0)
DARK_GREEN = (0,128,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
BORDER_COLOUR = RED
FPS = 120
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
clock = pygame.time.Clock()

score = 0
snake_head_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
snake_length = 50
width = 19
direction = LEFT
velocity = 2
turn_points = [((snake_head_pos[0]+snake_length, snake_head_pos[1]), DARK_GREEN)]

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")

snake_left_image = pygame.image.load("snake/snake-L.png")
snake_right_image = pygame.image.load("snake/snake-R.png")
snake_up_image = pygame.image.load("snake/snake-U.png")
snake_down_image = pygame.image.load("snake/snake-D.png")
snake_rect = snake_left_image.get_rect()
apple_image = pygame.image.load("snake/apple.png")
banana_image = pygame.image.load("snake/banana.png")
cherry_image = pygame.image.load("snake/cherry.png")
coconut_image = pygame.image.load("snake/coconut.png")
strawberry_image = pygame.image.load("snake/strawberry.png")
fruits = [apple_image, banana_image, cherry_image, coconut_image, strawberry_image]
fruit_colours = [GREEN, YELLOW, MAGENTA, CYAN, RED]
fruit_image_rect = apple_image.get_rect()

small_font = pygame.font.SysFont('comicsansms', 32)
font = pygame.font.SysFont('comicsansms', 64)
game_over_text = font.render("Game Over!", True, RED, BLACK)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

game_over2_text = small_font.render("Push space to continue", True, RED, BLACK)
game_over2_rect = game_over_text.get_rect()
game_over2_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80)

border_segments = [((0,0),(0,WINDOW_HEIGHT),BORDER_COLOUR),\
                   ((0,0),(WINDOW_WIDTH,0),BORDER_COLOUR),\
                   ((WINDOW_WIDTH,0),(WINDOW_WIDTH, WINDOW_HEIGHT),BORDER_COLOUR),\
                   ((0,WINDOW_HEIGHT),(WINDOW_WIDTH, WINDOW_HEIGHT),BORDER_COLOUR)]

def apply_velocity(pos, direction, velocity):
    return (pos[0] + (direction[0] * velocity), pos[1] + (direction[1] * velocity))

def distance_between(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def build_segment(p1, p2, colour):
    return (p1, p2, colour)

def skip_adjacent(pos, segments):
    result = segments.copy()
    for segment in segments:
        if intersects_any(pos, [segment]):
            result.remove(segment)
        else:
            break
    return result

def intersects_any(pos, segments):
    result = False
    head_rect = snake_left_image.get_rect()
    head_rect.center = pos
    for segment in segments:
        p1 = segment[0]
        p2 = segment[1]
        min_x = min(p1[0], p2[0]) - width//2
        min_y = min(p1[1], p2[1]) - width//2
        max_x = max(p1[0], p2[0]) + width//2
        max_y = max(p1[1], p2[1]) + width//2
        seg_rect = (min_x, min_y, max_x - min_x, max_y - min_y)
        # pygame.draw.line(display_surface, WHITE, (min_x, min_y), (min_x, max_y)) 
        # pygame.draw.line(display_surface, WHITE, (min_x, min_y), (max_x, min_y)) 
        # pygame.draw.line(display_surface, WHITE, (max_x, max_y), (min_x, max_y)) 
        # pygame.draw.line(display_surface, WHITE, (max_x, max_y), (max_x, min_y)) 
        if (head_rect.colliderect(seg_rect)):
            return True
            # result = True
    return result

def intersects_fruit(snake_head_pos, fruit_pos):
    head_rect = snake_left_image.get_rect()
    head_rect.center = snake_head_pos
    fruit_rect = apple_image.get_rect()
    fruit_rect.center = fruit_pos
    return head_rect.colliderect(fruit_rect)

def construct_segments(pos, length, points):
    used = 0
    segments = []
    idx = 0
    curr_pos = pos
    colour = DARK_GREEN
    while used < length:
        remain = length - used
        prev_used = used
        point_data = points[idx]
        point = point_data[0]
        point_colour = point_data[1]
        point_dist = distance_between(curr_pos, point)
        if (point_dist > remain):
            x_diff = point[0] - curr_pos[0]
            y_diff = point[1] - curr_pos[1]
            closer_point = (curr_pos[0] + min(abs(x_diff), remain) * sign(x_diff), curr_pos[1] + min(abs(y_diff), remain) * sign(y_diff))
            segments.append(build_segment(curr_pos, closer_point, colour))
            used += point_dist
            curr_pos = point
        else:
            segments.append(build_segment(curr_pos, point, colour))
            used += point_dist
            curr_pos = point
        # emergency exit    
        if (prev_used == used):
            break
        prev_used = used
        #colour = point_colour
        idx += 1
    return segments

def draw_segments(segments):
    for segment in segments:
        pygame.draw.line(display_surface, segment[2], segment[0], segment[1], width)
        pygame.draw.circle(display_surface, segment[2], segment[0], width//2, 0)
        pygame.draw.circle(display_surface, segment[2], segment[1], width//2, 0)

def draw_head(pos, direction):
    if direction == LEFT:
        snake_image = snake_left_image
    if direction == RIGHT:
        snake_image = snake_right_image
    if direction == UP:
        snake_image = snake_up_image
    if direction == DOWN:
        snake_image = snake_down_image
    snake_rect.center = pos
    display_surface.blit(snake_image, snake_rect)

def draw_fruit(idx, pos):
    fruit = fruits[idx]
    fruit_image_rect.center = pos
    display_surface.blit(fruit, fruit_image_rect)

def draw_score(score):
    text = small_font.render("Score: " + str(score), True, RED, BLACK)
    text_rect = text.get_rect()
    text_rect.right = WINDOW_WIDTH - 20
    text_rect.top = 20
    display_surface.blit(text, text_rect)


running = True
game_over = False
fruit_idx = 0
fruit_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 // 4)
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                direction = LEFT
                turn_points.insert(0, (snake_head_pos, DARK_GREEN))
            if (event.key == pygame.K_RIGHT):
                direction = RIGHT
                turn_points.insert(0, (snake_head_pos, DARK_GREEN))
            if (event.key == pygame.K_UP):
                direction = UP
                turn_points.insert(0, (snake_head_pos, DARK_GREEN))
            if (event.key == pygame.K_DOWN):
                direction = DOWN
                turn_points.insert(0, (snake_head_pos, DARK_GREEN))
            if (game_over and event.key == pygame.K_SPACE):
                score = 0
                snake_head_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                snake_length = 50
                width = 19
                direction = LEFT
                velocity = 2
                turn_points = [((snake_head_pos[0]+snake_length, snake_head_pos[1]), DARK_GREEN)]

    display_surface.fill(BLACK)

    if not game_over:
        snake_head_pos = apply_velocity(snake_head_pos, direction, velocity)
        snake_segments = construct_segments(snake_head_pos, snake_length, turn_points)

    game_over = intersects_any(snake_head_pos, border_segments) or intersects_any(snake_head_pos, skip_adjacent(snake_head_pos, snake_segments))

    if intersects_fruit(snake_head_pos, fruit_pos):
        score += 1
        snake_length += 50
        velocity += 0.25
        turn_points.insert(0, (snake_head_pos, fruit_colours[fruit_idx]))
        fruit_idx = random.randint(0, len(fruits)-1)
        fruit_pos = (random.randint(16, WINDOW_WIDTH-32), random.randint(16, WINDOW_HEIGHT-32))

    draw_score(score)
    if game_over:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(game_over2_text, game_over2_rect)
    else:
        draw_segments(border_segments)
        draw_segments(snake_segments)
        draw_head(snake_head_pos, direction)
        draw_fruit(fruit_idx, fruit_pos)

    clock.tick(FPS)

pygame.quit()