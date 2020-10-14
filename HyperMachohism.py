import pygame
from pygame.draw import *
from random import *
import numpy as np

pygame.init()

FPS = 200
screen = pygame.display.set_mode((1200, 600))  # Зададим размеры игрового поля

# Определим используемые в программе цветы
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

global score
score = 0  # Число очков игрока (Равно 0 в начале игры)
N_balls = 6  # Число шаров на экране
M_ellipses = 5  # Число эллипсов на экране
V_balls = 3  # Минимальная линейная скорость шаров по осям X и Y
V_ellipse = 2  # Минимальная линейная скорость эллипсов
Am = 100  # Минимальная амплитуда эллипсов по оси OY

# Определим списки с данными об шарах и эллипсах
Data = []  # Список с данными о движении шаров
CData = []  # Список с данными о движении эллипсов


def new_ball():
    """
        Функция рисует новые шары в произвольной точке экрана, случайным радиусом в диапазоне от 30
        до 50, с рандомными скоростями по осям в диапазоне от V_balls до 2 * V_balls, случайного
        цвета (из опредеённых) и заносит все эти данные шара в список Ball_parameters
    """
    global x, y, r, vx, vy, color, Ball_parametrs
    x = randint(100, 1100)
    y = randint(100, 500)
    r = randint(30, 50)
    vx = randint(V_balls, 2 * V_balls)
    vy = randint(V_balls, 2 * V_balls)
    color = COLORS[randint(0, 5)]
    Ball_parametrs = [x, y, r, vx, vy, color]


def balls(N_balls):
    """
        Рисуем новые шары по данным из списка шаров D
    """
    for i in range(0, N_balls):
        circle(screen, Data[i][5], (Data[i][0], Data[i][1]), Data[i][2])


def new_ellipse():
    """
        Рисуем новый эллипс, вписывая его в прямоугольник. x0, y0 - координаты верхнего левого угла
        описанного прямоугольника, задаются случайным образом. m0 - масштаб, эллипсы возможны 4 разных
        ращмеров. Vx0 - линейная скорость эллипса по оси ОХ, лежит в диапазоне от V_ellipse до 2 * V_ellipse.
        Амплитуда колебаний - A. Все данные каждого эллипса заносятся в список Ellipse_parametrs
    """
    global x0, y0, m0, vx0, A, color, yst, Ellipse_parametrs
    x0 = randint(200, 1000)
    y0 = randint(100, 400)
    yst = y0
    m0 = randint(2, 5)
    vx0 = randint(V_ellipse, 2 * V_ellipse)
    A = randint(Am, 2 * Am)
    color = COLORS[randint(0, 5)]
    Ellipse_parametrs = [x0, y0, A, vx0, yst, m0, color]


def ellipses(M_ellipses):
    """
        Функция рисует M_ellipses штук эллипсов на экране по данным из списка CData
    """
    for i in range(0, M_ellipses):
        ellipse(screen, CData[i][6], (CData[i][0], CData[i][1], CData[i][5] * 40, CData[i][5] * 10))


def Points_Score(n):
    """
        Функция выводит на экран надпись с числом очков у игрока.  n - переменная, отвечающая за число очков
    """
    inscription_font = pygame.font.SysFont('Arial Black', 64)
    inscription = inscription_font.render("Score : " + str(n), 5, (0, 255, 255))  # inscription
    screen.blit(inscription, (450, 0))  # where to


for i in range(0, N_balls):  # Задаём в начале игры количество шаров на игровом поле
    new_ball()
    Data.append(Ball_parametrs)
for i in range(0, M_ellipses):  # Задаём в начале игры количество эллипсов вместе с параметрами
    new_ellipse()
    CData.append(Ellipse_parametrs)


def click(event):
    for i in range(0, N_balls):
        if (event.pos[0] - Data[i][0]) ** 2 + (event.pos[1] - Data[i][1]) ** 2 <= Data[i][2] ** 2:
            global score
            score += 1
            new_ball()
            Data[i] = Ball_parametrs
            pygame.display.update()
            screen.fill(BLACK)
    for i in range(0, M_ellipses):
        # Условие попадания в эллипс: ((x-x0)/a)^2+((y-y0)/b)^2<=1, где x,y - координаты щелчка мышью
        x0 = CData[i][0] + 0.5 * CData[i][5] * 40
        y0 = CData[i][1] + 1 / 2 * CData[i][5] * 10
        a = 0.5 * CData[i][5] * 40
        b = 0.5 * CData[i][5] * 10
        if ((x0 - event.pos[0])/a) ** 2 + ((y0 - event.pos[1])/b) ** 2 <= 1:
            score += 10
            new_ellipse()
            CData[i] = Ellipse_parametrs
            pygame.display.update()
            screen.fill(BLACK)  # После попадания происходит заливка всего экрана. Все элементы отрисовываются заново


pygame.display.update()  # Обновляем дисплей
clock = pygame.time.Clock()
finished = False


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    balls(N_balls)  # Каждый tick рисуем новое положение ВСЕХ элементов на экране
    ellipses(M_ellipses)

    for i in range(0, N_balls):  # Условия отражения от стенов для шаров
        Data[i][0] += Data[i][3]
        Data[i][1] += Data[i][4]
        if Data[i][0] >= 1100 - Data[i][2] or Data[i][0] <= Data[i][2] + 20:
            Data[i][3] = -Data[i][3]
        if Data[i][1] >= 550 - Data[i][2] or Data[i][1] <= Data[i][2] + 20:
            Data[i][4] = -Data[i][4]

    for i in range(0, M_ellipses):  # Уравнение движения эллипсов + телепортация + отскок от стен
        CData[i][0] += CData[i][3]
        CData[i][1] = int(CData[i][4] + A * np.sin(CData[i][0] / 300))
        if CData[i][0] >= 1200 - 100 or CData[i][0] <= 0:
            CData[i][3] = - CData[i][3]
        if CData[i][1] >= 550 or CData[i][1] <= 50:
            CData[i][1] = 600 - CData[i][1]

    Points_Score(score)
    pygame.display.update()
    screen.fill(BLACK)
