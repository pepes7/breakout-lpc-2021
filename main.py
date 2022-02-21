import pygame
from pygame.locals import *
from sys import exit
import enum

pygame.init()


class Board:
    def __init__(self, color, point):
        self.color = color
        self.collision = False
        self.point = point


class COLOR(enum.Enum):
    GREEN = (0, 165, 0)
    RED = (153, 0, 0)
    YELLOW = (220, 220, 0)
    ORANGE = (210, 110, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 128, 255)


WIDTH = 800
HEIGHT = 800
WIDTH_BOARD = 45
HEIGHT_BOARD = 10
SPACES_BETWEEN_BOARDS = 5

boards = []
colors_boards = [COLOR.RED.value, COLOR.ORANGE.value,  COLOR.GREEN.value, COLOR.YELLOW.value]


for y in colors_boards:
    for x in range(0, int(WIDTH/(WIDTH_BOARD + SPACES_BETWEEN_BOARDS))):
        point_ball = 0
        if y == COLOR.RED.value:
            point_ball = 7
        elif y == COLOR.ORANGE.value:
            point_ball = 5
        elif y == COLOR.GREEN.value:
            point_ball = 3
        else:
            point_ball = 1
        boards.append(Board(y, point_ball))
        boards.append(Board(y, point_ball))


music_collision = pygame.mixer.Sound('collision.wav')
music_coll_paddle = pygame.mixer.Sound('bleep.wav')
font = pygame.font.SysFont('arial', 35, True, True)
paddle_x = int(WIDTH/2 - WIDTH_BOARD/2)
ball_x = int(WIDTH/2)
ball_y = int(HEIGHT/2)
ball_dx = 3
ball_dy = 3
WIDTH_PADDLE_ORIGIN = 45
width_paddle = WIDTH_PADDLE_ORIGIN
height_paddle = 10
points = 0
life = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('breakout')
clock = pygame.time.Clock()


def draw_edge():
    pygame.draw.rect(screen, COLOR.WHITE.value, (0, 0, 4, HEIGHT))
    pygame.draw.rect(screen, COLOR.WHITE.value, (WIDTH - 4, 0, 4, HEIGHT))

    pygame.draw.rect(screen, COLOR.WHITE.value, (0, 0, WIDTH, 25))


def command_keys():
    global paddle_x
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        paddle_x = paddle_x - 5
    if keys[K_RIGHT]:
        paddle_x = paddle_x + 5


def check_ball_collision_wall():
    global ball_dy
    global ball_dx
    global width_paddle
    global life
    global ball_y
    global ball_x

    # collision with upper wall
    if ball_y < 0:
        width_paddle = WIDTH_PADDLE_ORIGIN/2
        ball_dy *= -1

    # collision with right wall
    if ball_x > WIDTH:
        ball_dx *= -1

    # collision with left wall
    if ball_x < 0:
        ball_dx *= -1

    if ball_y > 1000:
        if life > 0:
            life -= 1
        ball_y = int(HEIGHT/2)
        ball_x = int(WIDTH/2)


def draw_board(ball_screen):
    global points
    global ball_dy

    x_board = 0
    y_board = 100
    for board in boards:
        if x_board >= WIDTH:
            y_board += 15
            x_board = 0

        if not board.collision:
            board_collision = pygame.draw.rect(screen, board.color, (x_board, y_board, WIDTH_BOARD, HEIGHT_BOARD))
            if ball_screen.colliderect(board_collision):
                board.collision = True
                points += board.point
                ball_dy *= -1
                music_collision.play()
        x_board += WIDTH_BOARD + SPACES_BETWEEN_BOARDS


while True:
    clock.tick(100)
    message_points = f'{points}'
    message_life = f'{life}'
    text_points = font.render(message_points, True, (255, 255, 255))
    text_life = font.render(message_life, True, (255, 255, 255))

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    command_keys()

    ball = pygame.draw.circle(screen, COLOR.WHITE.value, (ball_x, ball_y), 5)
    paddle = pygame.draw.rect(screen, COLOR.BLUE.value, (paddle_x, HEIGHT - 50, width_paddle, height_paddle))

    draw_board(ball)
    draw_edge()

    if ball.colliderect(paddle):
        ball_dy *= -1
        music_coll_paddle.play()

    check_ball_collision_wall()
    ball_x = ball_x + ball_dx
    ball_y = ball_y + ball_dy

    screen.blit(text_points, (30, 50))
    screen.blit(text_life, (WIDTH/2 + 50, 50))

    if life == 0:
        quit()
    pygame.display.update()
