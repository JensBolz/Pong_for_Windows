import pygame
import random
import sys

# Pygame initialisieren
pygame.init()

# Fenster und Farben
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - Python")

WHITE = (255, 255, 255)
BLACK = (15, 15, 20)
GRAY = (100, 100, 110)
GREEN = (80, 220, 140)

# Schriftarten
score_font = pygame.font.Font(None, 60)
info_font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 72)

# Spielfeld
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 16
PADDLE_SPEED = 7
WINNING_SCORE = 10

# Schläger
left_paddle = pygame.Rect(
    30, HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH, PADDLE_HEIGHT
)

right_paddle = pygame.Rect(
    WIDTH - 30 - PADDLE_WIDTH,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH, PADDLE_HEIGHT
)

# Ball
ball = pygame.Rect(
    WIDTH // 2 - BALL_SIZE // 2,
    HEIGHT // 2 - BALL_SIZE // 2,
    BALL_SIZE, BALL_SIZE
)

ball_speed_x = random.choice([-5, 5])
ball_speed_y = random.choice([-4, 4])

# Punktestand
left_score = 0
right_score = 0
game_over = False
winner = ""

clock = pygame.time.Clock()


def reset_ball(direction):
    """Setzt den Ball in die Mitte zurück."""
    global ball_speed_x, ball_speed_y

    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = 5 * direction
    ball_speed_y = random.choice([-4, -3, 3, 4])


def draw_text(text, font, color, x, y):
    """Zeichnet Text mittig an einer Position."""
    image = font.render(text, True, color)
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)


def draw_game():
    """Zeichnet das gesamte Spielfeld."""
    screen.fill(BLACK)

    # Mittellinie
    for y in range(0, HEIGHT, 30):
        pygame.draw.rect(
            screen, GRAY,
            (WIDTH // 2 - 2, y, 4, 15)
        )

    # Schläger und Ball
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, GREEN, ball)

    # Punktestand
    draw_text(
        str(left_score), score_font, WHITE,
        WIDTH // 4, 45
    )
    draw_text(
        str(right_score), score_font, WHITE,
        WIDTH * 3 // 4, 45
    )

    # Steuerung
    draw_text(
        "Spieler 1: W / S",
        info_font, WHITE, WIDTH // 4, HEIGHT - 30
    )
    draw_text(
        "Spieler 2: Pfeiltasten",
        info_font, WHITE, WIDTH * 3 // 4, HEIGHT - 30
    )

    # Gewinnanzeige
    if game_over:
        draw_text(
            f"{winner} gewinnt!",
            title_font, GREEN, WIDTH // 2, HEIGHT // 2 - 35
        )
        draw_text(
            "Leertaste: Neustart | ESC: Beenden",
            info_font, WHITE, WIDTH // 2, HEIGHT // 2 + 25
        )


# Hauptschleife
running = True

while running:
    clock.tick(60)

    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_over and event.key == pygame.K_SPACE:
                left_score = 0
                right_score = 0
                game_over = False
                winner = ""

                left_paddle.centery = HEIGHT // 2
                right_paddle.centery = HEIGHT // 2
                reset_ball(random.choice([-1, 1]))

    # Tastatureingaben lesen
    keys = pygame.key.get_pressed()

    if not game_over:
        # Linken Schläger bewegen
        if keys[pygame.K_w]:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left_paddle.y += PADDLE_SPEED

        # Rechten Schläger bewegen
        if keys[pygame.K_UP]:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            right_paddle.y += PADDLE_SPEED

        # Schläger im Spielfeld halten
        left_paddle.clamp_ip(screen.get_rect())
        right_paddle.clamp_ip(screen.get_rect())

        # Ball bewegen
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Kollision mit oberem und unterem Rand
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Kollision mit den Schlägern
        if ball.colliderect(left_paddle) and ball_speed_x < 0:
            ball.left = left_paddle.right
            ball_speed_x *= -1

            # Ballwinkel abhängig vom Treffpunkt
            offset = (
                ball.centery - left_paddle.centery
            ) / (PADDLE_HEIGHT / 2)

            ball_speed_y = offset * 5

        if ball.colliderect(right_paddle) and ball_speed_x > 0:
            ball.right = right_paddle.left
            ball_speed_x *= -1

            offset = (
                ball.centery - right_paddle.centery
            ) / (PADDLE_HEIGHT / 2)

            ball_speed_y = offset * 5

        # Punkt für Spieler 2
        if ball.left <= 0:
            right_score += 1
            reset_ball(1)

        # Punkt für Spieler 1
        if ball.right >= WIDTH:
            left_score += 1
            reset_ball(-1)

        # Gewinner prüfen
        if left_score >= WINNING_SCORE:
            game_over = True
            winner = "Spieler 1"

        elif right_score >= WINNING_SCORE:
            game_over = True
            winner = "Spieler 2"

    # Spielfeld zeichnen
    draw_game()
    pygame.display.flip()

# Programm beenden
pygame.quit()
sys.exit()