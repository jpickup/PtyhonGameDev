import pygame
import random
import time
from data import Data
import pickle
from networking import Network

MAX_STARTUP_PACKETS = 4

network = Network()

#listen for packets
player_no = 1
received = 0
while network.has_data(0.2) and received < MAX_STARTUP_PACKETS:
    print("Has data on startup")
    data = network.receive()
    print(str(data))
    received += 1
    if data.player_no >= player_no:
        player_no = data.player_no + 1

print("I am player no " + str(player_no))

pygame.init()

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

#Define
right_smash_remaining = 3
left_smash_remaining = 3

NORMAL_BOOST_SPEED = 2

#For ball
radius = 15
ball_x, ball_y = WIDTH/2 - radius, HEIGHT/2 - radius
ball_vel_x, ball_vel_y = 2, 2
left_smash = 0
right_smash = 0

#paddle dimensions
paddle_width, paddle_height = 20, 120
left_paddle_y = right_paddle_y = HEIGHT/2 - paddle_height/2
left_paddle_x, right_paddle_x = 100 - paddle_width/2, WIDTH - (100 - paddle_width/2)
right_paddle_vel = left_paddle_vel = 0

#main game loop
run = True
direction = [0,1]
angle = [0,1,2]
while run:
    data = Data(player_no, left_paddle_y, (ball_x, ball_y))
    network.send(data)

    other_data = None
    while (other_data is None) and network.has_data():
        net_data = network.receive()
        if (net_data.is_valid() and net_data.is_other_player(player_no)):
            other_data = net_data

    wn.fill(BLACK)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        right_paddle_vel = -2
    if keys[pygame.K_RIGHT] and right_smash_remaining > 0:
        right_smash = 1
    if keys[pygame.K_DOWN]:
        right_paddle_vel = 2
    if keys[pygame.K_w]:
        left_paddle_vel = -2
    if keys[pygame.K_s]:
        left_paddle_vel = 2
    if keys[pygame.K_d] and left_smash_remaining > 0:
        left_smash = 1
    
    if i.type == pygame.KEYUP:
        if i.key == pygame.K_UP or pygame.K_DOWN:
            right_paddle_vel = 0
        if i.key == pygame.K_a or pygame.K_s:
            left_paddle_vel = 0

    #Ball movement controls
    if ball_y <= 0 + radius or ball_y >=HEIGHT - radius:
        ball_vel_y *= -1
    if ball_x >= WIDTH - radius:
        player_1 += 1
        ball_x, ball_y = WIDTH/2 - radius, HEIGHT/2 - radius
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                ball_vel_y, ball_vel_x = -1.35, 0.7
            if ang == 1:
                ball_vel_y, ball_vel_x = -0.75, 0.75
            if ang == 2:
                ball_vel_y, ball_vel_x = -0.75, 1.35
            ball_vel_x *= -1


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
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                ball_vel_y, ball_vel_x = -1.35, 0.7
            if ang == 1:
                ball_vel_y, ball_vel_x = -0.75, 0.75
            if ang == 2:
                ball_vel_y, ball_vel_x = -0.75, 1.35

        if dir == 1:
            if ang == 0:
                ball_vel_y, ball_vel_x = 1.35, 0.7
            if ang == 1:
                ball_vel_y, ball_vel_x = 0.75, 0.75
            if ang == 2:
                ball_vel_y, ball_vel_x = 0.75, 1.35

    
    #paddle movement controls
    if left_paddle_y >= HEIGHT - paddle_height:
        left_paddle_y = HEIGHT - paddle_height
    if left_paddle_y <0:
        left_paddle_y = 0
    if right_paddle_y >= HEIGHT - paddle_height:
        right_paddle_y = HEIGHT - paddle_height
    if right_paddle_y <0:
        right_paddle_y = 0

    #paddle collisions
    #left paddle
    if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
        if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
            ball_x = left_paddle_x + paddle_width
            ball_vel_x *= -1
    
    #right paddle
    if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
        if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
            ball_x = right_paddle_x
            ball_vel_x *= -1

    #Left smash gadget
    if left_smash == 1:
        if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
            if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                ball_x = left_paddle_x + paddle_width
                ball_vel_x *= -2
                left_smash = 0
                left_smash_remaining -= 1

    #Right smash gadget
    if right_smash == 1:
        if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
            if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                ball_x = right_paddle_x + paddle_width
                ball_vel_x *= 2
                right_smash = 0
                right_smash_remaining -= 1

    #movements
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    left_paddle_y += left_paddle_vel

    if not(other_data is None):
        right_paddle_y = other_data.bat_position
        if other_data.is_master():
            ball_x = other_data.ball_position[0]
            ball_y = other_data.ball_position[1]

    #Scoreboard
    font = pygame.font.SysFont('callibri', 32)
    score_1 = font.render("Player 1 Score: " + str(player_1), True, WHITE, BLACK)
    wn.blit(score_1, (25, 25))
    score_2 = font.render("Player 2 Score: " + str(player_2), True, WHITE, BLACK)
    wn.blit(score_2, (WIDTH - 250, 25))
    smash_1 = font.render("Smashes remaining: " + str(left_smash_remaining), True, WHITE, BLACK)
    wn.blit(smash_1, (25, 65))
    smash_2 = font.render("Smashes remaining: " + str(right_smash_remaining), True, WHITE, BLACK)
    wn.blit(smash_2, (WIDTH - 250, 65))

    #OBJECTS
    pygame.draw.circle(wn, BLUE, (ball_x, ball_y), radius)
    pygame.draw.rect(wn, RED, pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, RED, pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height))

    if left_smash == 1:
        pygame.draw.circle(wn, WHITE, (left_paddle_x + 10, left_paddle_y + 10), 4)

    if right_smash == 1:
        pygame.draw.circle(wn, WHITE, (right_paddle_x + 10, right_paddle_y + 10), 4)

    #ENDSCREEN
    winning_font = pygame.font.SysFont('callibri', 100)
    if player_1 >= 8:
        wn.fill(BLACK)
        endscreen = winning_font.render("PLAYER 1 WON!!!", True, WHITE)
        wn.blit(endscreen, (WIDTH//2 - 100, HEIGHT//2))

    if player_2 >= 8:
        wn.fill(BLACK)
        endscreen = winning_font.render("PLAYER 2 WON!!!", True, WHITE)
        wn.blit(endscreen, (WIDTH//2 - 100, HEIGHT//2))

    pygame.display.update()
