import pygame
import random

pygame.init()

gadget_pair = 1
ch = int(input("Enter your choice for gadget pair: "))
if ch == 1:
    gadget_pair = 1
elif ch == 2:
    gadget_pair = 2

#INITIALS
WIDTH, HEIGHT = 1700, 1000
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
player_1 = player_2 = 0

#Colours
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

#For ball
radius = 15
ball_x, ball_y = WIDTH/2 - radius, HEIGHT/2 - radius
ball_vel_x, ball_vel_y = 1, 1
dummy_x, dummy_y = WIDTH/2 - radius, HEIGHT/2 - radius
dummy_vel_x, dummy_vel_y = 1, 1

#paddle dimensions
paddle_width, paddle_height = 20, 120
left_paddle_y = right_paddle_y = HEIGHT/2 - paddle_height/2
left_paddle_x, right_paddle_x = 100 - paddle_width/2, WIDTH - (100 - paddle_width/2)
right_paddle_vel = left_paddle_vel = 0

#dummy
second_left_paddle_y = second_right_paddle_y = HEIGHT/2 - paddle_height/2
second_left_paddle_x, second_right_paddle_x = 100 - paddle_width/2, WIDTH - (100 - paddle_width/2)
second_right_paddle_vel = second_left_paddle_vel = 0

#gadgets
left_gadget = right_gadget = 0
left_gadget_remaining = right_gadget_remaining = 5

#main game loop
run = True
direction = [0,1]
angle = [0,1,2]
while run:
    wn.fill(BLACK)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        right_paddle_vel = -2
        second_right_paddle_vel = -2
    if keys[pygame.K_DOWN]:
        right_paddle_vel = 2
        second_right_paddle_vel = 2
    if keys[pygame.K_RIGHT] and right_gadget_remaining > 0:
        right_gadget = 1
    if keys [pygame.K_LEFT] and right_gadget_remaining > 0:
        right_gadget = 2
    if keys[pygame.K_w]:
        left_paddle_vel = -2
        second_left_paddle_vel = -2
    if keys[pygame.K_s]:
        left_paddle_vel = 2
        second_left_paddle_vel = 2
    if keys[pygame.K_d] and left_gadget_remaining > 0:
        left_gadget = 1
    if keys[pygame.K_a] and left_gadget_remaining > 0:
        left_gadget = 2
    
    if i.type == pygame.KEYUP:
        if i.key == pygame.K_UP or pygame.K_DOWN:
            right_paddle_vel = 0
            second_right_paddle_vel = 0
        if i.key == pygame.K_a or pygame.K_s:
            left_paddle_vel = 0
            second_left_paddle_vel = 0

        

    #Ball movement controls
    if ball_y <= 0 + radius or ball_y >=HEIGHT - radius:
        ball_vel_y *= -0.75
    if dummy_y <= 0 + radius or dummy_y >=HEIGHT - radius:
        dummy_vel_y *= -0.75
    if ball_x >= WIDTH - radius:
        player_1 += 1
        ball_x, ball_y = WIDTH/2 - radius, HEIGHT/2 - radius
        dummy_x, dummy_y = WIDTH/2 - radius, HEIGHT/2 - radius
        second_left_paddle_y = left_paddle_y
        second_right_paddle_y = right_paddle_y
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                ball_vel_y, ball_vel_x = -1.35, 0.7
                dummy_vel_y, dummy_vel_x = -1.35, 0.7
            if ang == 1:
                ball_vel_y, ball_vel_x = -0.75, 0.75
                dummy_vel_y, dummy_vel_x = -0.75, 0.75
            if ang == 2:
                ball_vel_y, ball_vel_x = -0.75, 1.35
                dummy_vel_y, dummy_vel_x = -0.75, 1.35
            ball_vel_x *= -1
            dummy_vel_x *= -1


        if dir == 1:
            if ang == 0:
                ball_vel_y, ball_vel_x = 1, 1
            if ang == 1:
                ball_vel_y, ball_vel_x = 1, 1
            if ang == 2:
                ball_vel_y, ball_vel_x = 1, 1
        ball_vel_x *= -1


        ball_vel_x *= -1
        ball_vel_y *= -1
    if ball_x <= 0 + radius:
        player_2 += 1
        ball_x, ball_y = WIDTH/2 - radius, HEIGHT/2 - radius
        dummy_x, dummy_y = WIDTH/2 - radius, HEIGHT/2 - radius
        second_right_paddle_y = right_paddle_y
        second_left_paddle_y = left_paddle_y
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                ball_vel_y, ball_vel_x = -1.35, 0.7
                dummy_vel_y, dummy_vel_x = -1.35, 0.7
            if ang == 1:
                ball_vel_y, ball_vel_x = -0.75, 0.75
                dummy_vel_y, dummy_vel_x = -0.75, 0.75
            if ang == 2:
                ball_vel_y, ball_vel_x = -0.75, 1.35
                dummy_vel_y, dummy_vel_x = -0.75, 1.35

        if dir == 1:
            if ang == 0:
                ball_vel_y, ball_vel_x = 1.35, 0.7
                dummy_vel_y, dummy_vel_x = 1.35, 0.7
            if ang == 1:
                ball_vel_y, ball_vel_x = 0.75, 0.75
                dummy_vel_y, dummy_vel_x = 0.75, 0.75
            if ang == 2:
                ball_vel_y, ball_vel_x = 0.75, 1.35
                dummy_vel_y, dummy_vel_x = 0.75, 1.35

    
    #paddle movement controls
    if left_paddle_y >= HEIGHT - paddle_height:
        left_paddle_y = HEIGHT - paddle_height
    if left_paddle_y <0:
        left_paddle_y = 0
    if right_paddle_y >= HEIGHT - paddle_height:
        right_paddle_y = HEIGHT - paddle_height
    if right_paddle_y <0:
        right_paddle_y = 0

    if second_left_paddle_y >= HEIGHT - paddle_height:
        second_left_paddle_y = HEIGHT - paddle_height
    if second_left_paddle_y <0:
        second_left_paddle_y = 0
    if second_right_paddle_y >= HEIGHT - paddle_height:
        right_paddle_y = HEIGHT - paddle_height
    if second_right_paddle_y <0:
        second_right_paddle_y = 0

    #paddle collisions
    #left paddle
    if second_left_paddle_y == left_paddle_y:
        if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
            if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                ball_x = left_paddle_x + paddle_width
                dummy_x = left_paddle_x + paddle_width
                ball_vel_x *= -1
                dummy_vel_x *= -1
    
    if second_left_paddle_y != left_paddle_y:
        if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
            if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                ball_x = left_paddle_x + paddle_width
                dummy_x = left_paddle_x + paddle_width
                ball_vel_x *= -1
                dummy_vel_x *= -1

        if second_left_paddle_x <= ball_x <= second_left_paddle_x + paddle_width:
            if second_left_paddle_y <= ball_y <= second_left_paddle_y + paddle_height:
                ball_x = left_paddle_x + paddle_width
                dummy_x = left_paddle_x + paddle_width
                ball_vel_x *= -1
                dummy_vel_x *= -1
    
    #right paddle
    if second_right_paddle_y == right_paddle_y:
        if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
            if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                ball_x = right_paddle_x
                dummy_x = right_paddle_x
                ball_vel_x *= -1
                dummy_vel_x *= -1

    if second_right_paddle_y != right_paddle_y:
        if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
            if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                ball_x = right_paddle_x
                dummy_x = right_paddle_x
                ball_vel_x *= -1
                dummy_vel_x *= -1

        if second_right_paddle_x <= ball_x <= second_right_paddle_x + paddle_width:
            if second_right_paddle_y <= ball_y <= second_right_paddle_y + paddle_height:
                ball_x = right_paddle_x
                dummy_x = right_paddle_x
                ball_vel_x *= -1
                dummy_vel_x *= -1

    #gadgets in action
    if gadget_pair == 1:
        if left_gadget == 1:
            if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
                if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                    ball_x = left_paddle_x + paddle_width
                    ball_vel_x *= -3.5
                    dummy_vel_x *= -3.5
                    left_gadget = 0
                    left_gadget_remaining -= 1
        elif left_gadget == 2:
            left_paddle_y = ball_y
            left_gadget = 0
            left_gadget_remaining -=1

        if right_gadget == 1:
            if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
                if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                    ball_x = right_paddle_x
                    ball_vel_x *= -3.5
                    dummy_vel_x *= -3.5
                    right_gadget = 0
                    right_gadget_remaining -= 1
        elif right_gadget ==2:
            right_paddle_y = ball_y
            right_gadget = 0
            right_gadget_remaining -= 1
    
    #second pair
    elif gadget_pair == 2:
        if left_gadget == 1:
            if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
                if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                    ball_x = left_paddle_x + paddle_width
                    dummy_x = left_paddle_x + paddle_width
                    ball_vel_x *= -1
                    dummy_vel_x *= -1
                    dummy_vel_y *= -1
                    left_gadget = 0
                    left_gadget_remaining -= 1

        elif left_gadget == 2:
            second_left_paddle_y = left_paddle_y + 200
            left_gadget = 0
            left_gadget_remaining -= 1
    
        if right_gadget == 1:
            if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
                if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                    ball_x = right_paddle_x
                    dummy_x = right_paddle_x
                    ball_vel_x *= -1
                    dummy_vel_x *= -1
                    dummy_vel_y *= -1
                    right_gadget = 0
                    right_gadget_remaining -= 1
        
        elif right_gadget == 2:
            second_right_paddle_y = right_paddle_y + 200
            right_gadget = 0
            right_gadget_remaining -= 1

    #movements
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    dummy_x += dummy_vel_x
    dummy_y += dummy_vel_y
    right_paddle_y += right_paddle_vel
    left_paddle_y += left_paddle_vel
    second_left_paddle_y += second_left_paddle_vel
    second_right_paddle_y += second_right_paddle_vel

    #Scoreboard
    font = pygame.font.SysFont('callibri', 32)
    score_1 = font.render("Player 1: ", str(player_1), True, WHITE)
    wn.blit(score_1, (25, 25))
    score_2 = font.render("Player 2: ", str(player_2), True, WHITE)
    wn.blit(score_2, (WIDTH - 150, 25))
    gad_left_1 = font.render("Gadget left: " + str(left_gadget_remaining), True, WHITE)
    wn.blit(gad_left_1, (25, 65))
    gad_left_2 = font.render("Gadget left: " + str(right_gadget_remaining), True, WHITE)
    wn.blit(gad_left_2, (WIDTH - 150, 65))


    #OBJECTS
    pygame.draw.circle(wn, BLUE, (ball_x, ball_y), radius)
    pygame.draw.rect(wn, RED, pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, RED, pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height))

    #dummy ball section
    pygame.draw.circle(wn, BLUE, (dummy_x, dummy_y), radius)

    #second paddle
    pygame.draw.rect(wn, RED, pygame.Rect(second_left_paddle_x, second_left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, RED, pygame.Rect(second_right_paddle_x, second_right_paddle_y, paddle_width, paddle_height))

    #ENDSCREEN
    winning_font = pygame.font.SysFont('callibri', 100)
    if player_1 >= 3:
        wn.fill(BLACK)
        endscreen = winning_font.render("PLAYER 1 WON!!!", True, WHITE)
        wn.blit(endscreen, (WIDTH//2, HEIGHT//2))

    if player_2 >= 3:
        wn.fill(BLACK)
        endscreen = winning_font.render("PLAYER 2 WON!!!", True, WHITE)
        wn.blit(endscreen, (WIDTH//2 - 100, HEIGHT//2))
    
    if left_gadget == 1:
        pygame.draw.circle(wn, WHITE, (left_paddle_x + 10, left_paddle_y + 10), 4)
    if right_gadget == 1:
        pygame.draw.circle(wn, WHITE, (right_paddle_x + 10, right_paddle_y + 10), 4)
    pygame.display.update()
