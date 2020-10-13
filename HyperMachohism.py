import pygame
from pygame.draw import *
from random import randint
import numpy as np

pygame.init()

FPS = 200
screen = pygame.display.set_mode((1200, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
a1 = (randint(1, 255), randint(1, 255), randint(1, 255))
a2 = (randint(1, 255), randint(1, 255), randint(1, 255))
a3 = (randint(1, 255), randint(1, 255), randint(1, 255))
a4 = (randint(1, 255), randint(1, 255), randint(1, 255))
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, a1, a2, a3, a4]

global score
score = 0
N = 10
M = 10
Data = []
CData = []


def new_ball():
    global x, y, r, vx, vy, color, Array
    x = randint(100, 1100)
    y = randint(100, 500)
    r = randint(30, 50)
    vx = randint(-5, +5)
    vy = randint(-5, +5)
    color = COLORS[randint(0, len(COLORS)-1)]
    Array = [x, y, r, vx, vy, color]


for i in range(0, N):
    new_ball()
    Data.append(Array)


def balls(N):
    for i in range(0, N):
        circle(screen, Data[i][5], (Data[i][0], Data[i][1]), Data[i][2])


def new_cloud():
    """
    Рисуем облако:
    (x0,y0) - координаты центра
    m0 - масштаб
    """
    global x0, y0, m0, vx0, A, color, yst,  CArray
    x0 = randint(200, 1000)
    y0 = randint(100, 400)
    yst = y0
    m0 = randint(1, 4)
    vx0 = randint(20, 30) / 10
    A  = randint(30, 300)
    color = COLORS[randint(0, len(COLORS)-1)]
    CArray = [x0, y0, A, vx0, yst,  m0, color]


for i in range(0, M):
    new_cloud()
    CData.append(CArray)


def clouds(M):
    for i in range(0, M - 1):
        ellipse(screen, CData[i][6], (CData[i][0], CData[i][1], CData[i][5] * 40, CData[i][5] * 10))


def Points_Score(n):
    inscription_font = pygame.font.SysFont('Arial Black', 64)
    inscription = inscription_font.render("Score : " + str(n), 5, (0, 255, 255))  # inscription
    screen.blit(inscription, (450, 0))  # where to


def Catcha():
    inscription_font = pygame.font.SysFont('Arial Black', 64)
    inscription = inscription_font.render("Hitted!", 5, (0, 255, 0))  # inscription
    screen.blit(inscription, (450, 520))  # where to


def click(event):
    for i in range(0, N):
        if (event.pos[0] - Data[i][0]) ** 2 + (event.pos[1] - Data[i][1]) ** 2 <= Data[i][2] ** 2:
            global score
            score += 1
            Catcha()
            new_ball()
            Data[i] = Array
            pygame.display.update()
            screen.fill(BLACK)
    for i in range(0, M):
        if ((event.pos[0] - CData[i][0] - 1/2*CData[i][5]*40)**2)/(1/2*CData[i][5]*40)**2 + ((event.pos[1] - CData[i][1] - 1/2*CData[i][5])**2)/(1/2*CData[i][5] * 10)**2 <= 1:
            score += 10
            Catcha()
            new_cloud()
            CData[i] = CArray
            pygame.display.update()
            screen.fill(BLACK)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

new_ball()
new_cloud()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
            print('Click!')
    balls(N)
    clouds(M)

    for i in range(0, N):
        Data[i][0] += Data[i][3]
        Data[i][1] += Data[i][4]
        if Data[i][0] >= 1100 - Data[i][2] or Data[i][0] <= Data[i][2] + 20:
            Data[i][3] = -Data[i][3]
        if Data[i][1] >= 550 - Data[i][2] or Data[i][1] <= Data[i][2] + 20:
            Data[i][4] = -Data[i][4]

    for i in range(0, M):
        CData[i][0] += CData[i][3]
        CData[i][1] = CData[i][4] + 1.5 * A * np.sin(CData[i][0] / 300)
        if CData[i][0] >= 1200 - 100 or CData[i][0] <= 0:
            CData[i][3] = - CData[i][3]
        if CData[i][1] >= 550 or CData[i][1] <= 50:
            CData[i][1] = 600 - CData[i][1]

    Points_Score(score)
    pygame.display.update()
    screen.fill(BLACK)
