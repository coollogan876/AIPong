import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 2560, 1440
BALL_RADIUS = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 120
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Singleplayer Pong")

player_paddle = pygame.Rect(WIDTH - PADDLE_WIDTH - 50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
computer_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)

ball_speed_x = -10
ball_speed_y = 10

computer_paddle_speed = 15

def calculate_angle(x, y):
    return math.degrees(math.atan2(y, x))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_y = pygame.mouse.get_pos()[1]
    player_paddle.y = mouse_y - PADDLE_HEIGHT // 2

    if ball_speed_x < 0:
        predicted_y = ball.y + (ball_speed_y / ball_speed_x) * (computer_paddle.left - ball.left)
        
        if computer_paddle.centery < predicted_y and computer_paddle.bottom < HEIGHT:
            computer_paddle.y += computer_paddle_speed
        elif computer_paddle.centery > predicted_y and computer_paddle.top > 0:
            computer_paddle.y -= computer_paddle_speed
    else:
        random_direction = random.choice([-1, 1])
        computer_paddle.y += random_direction * computer_paddle_speed

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x = WIDTH // 2 - BALL_RADIUS // 2
        ball.y = HEIGHT // 2 - BALL_RADIUS // 2
        ball_speed_x = -ball_speed_x

    if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
        ball_speed_x = -ball_speed_x

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, computer_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    pygame.display.flip()

    clock.tick(FPS)
