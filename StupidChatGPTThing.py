import pygame
import sys
import random
import math
import configparser
import os

# Load options from Options.ini
config = configparser.ConfigParser()
config.read('Options.ini')

# Get options or set defaults
player_paddle_speed = config.getint('Options', 'player_paddle_speed', fallback=15)
computer_paddle_speed = config.getint('Options', 'computer_paddle_speed', fallback=15)
ball_speed_x = config.getint('Options', 'ball_speed_x', fallback=-10)
ball_speed_y = config.getint('Options', 'ball_speed_y', fallback=10)
enable_winner_screen = config.getboolean('Options', 'enable_winner_screen', fallback=True)
enable_death_screen = config.getboolean('Options', 'enable_death_screen', fallback=True)
wins_needed = config.getint('Options', 'wins_needed', fallback=3)

# Initialize Pygame
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

font = pygame.font.Font(None, 74)

clock = pygame.time.Clock()

win_sound = pygame.mixer.Sound('win.ogg')
death_sound = pygame.mixer.Sound('death.ogg')

player_score = 0
computer_score = 0

def calculate_angle(x, y):
    return math.degrees(math.atan2(y, x))

def show_winner_screen():
    text = font.render("You Win!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

def show_death_screen():
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

def show_score():
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    computer_text = font.render(f"PC: {computer_score}", True, WHITE)
    screen.blit(player_text, (10, 10))
    screen.blit(computer_text, (WIDTH - computer_text.get_width() - 10, 10))

def show_end_game_prompt():
    text = font.render("Press 'R' to restart or 'Q' to quit", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + text.get_height()))
    pygame.display.flip()

def reset_game():
    global player_score, computer_score
    player_score = 0
    computer_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_q:
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

    if ball.left <= 0:
        if enable_death_screen:
            show_death_screen()
        computer_score += 1
        if computer_score == wins_needed:
            show_end_game_prompt()
            ball_speed_x = 0
            ball_speed_y = 0
    elif ball.right >= WIDTH:
        if enable_winner_screen:
            show_winner_screen()
        player_score += 1
        if player_score == wins_needed:
            show_end_game_prompt()
            ball_speed_x = 0
            ball_speed_y = 0

    if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
        ball_speed_x = -ball_speed_x

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, computer_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    show_score()

    pygame.display.flip()

    clock.tick(FPS)
