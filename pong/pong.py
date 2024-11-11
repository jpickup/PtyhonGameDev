import pygame
import random
import time
import socket
from data import Data
import pickle

#networking
multicast_group = '224.1.1.1' 
multicast_port = 55000
MULTICAST_TTL = 32
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
sender_socket.settimeout(1.0)
addr = (multicast_group, multicast_port)

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
try:
    receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except AttributeError as e:
    print(e)
    pass
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

receiver_socket.bind(('', multicast_port))

host = socket.gethostbyname(socket.gethostname())
receiver_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
receiver_socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton(host))


player_no = input("Player number: ")

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
    message, address = receiver_socket.recvfrom(1024)
    data = pickle.loads(message)
    #print("Message from " + str(address))
    if not(data is None) and data.isValid():
        #print(data.toString())
        if data.player_no != player_no:
            right_paddle_y = data.bat_position

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

    data = Data(player_no, left_paddle_y, (ball_x, ball_y))
    sender_socket.sendto(pickle.dumps(data), addr)

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
    right_paddle_y += right_paddle_vel
    left_paddle_y += left_paddle_vel

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
