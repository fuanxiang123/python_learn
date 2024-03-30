import random
import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *

import pymunk
import pymunk.pygame_util
space=pymunk.Space()
spacer.gravity=(0.0, -900.0) # 设置重力
# pygame初始化
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
draw_options=pymunk.pygame_util.Drawoptions(screen)

FPS = 60
balls = []  # 所有的球
ticks_to_next_ball = 10  # 多少帧后出现下一个球
exact = 10  # 一帧计算几次
static_body = space.static_body
static_lines = [
	pymunk.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0),
	pymunk.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
]
for line in static_lines:
    line.elasticity = 0.95  # 弹性系数 0-1
    line.friction = 0.9     # 摩擦系数 0-1
space.add(static_lines)


'''
4.创建物体
pymunk.Body 是物体类
pymunk.Circle是圆类（其父类是Shape 形状类）
下面我们写个函数来创建小球
'''
# 创建一个球
def create_ball():
    mass = 10   # 质量
    radius = 25 # 半径
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(115, 350)
    body.position = x, 400
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.95
    shape.friction = 0.9
    space.add(body, shape)
    balls.append(shape)
'''
5.移除物体
从世界中删除物体
space.remove(Shape, Body)

下面这个函数是创建或删除小球
'''

def update_balls():
	global ticks_to_next_ball
    # 根据需要创建/移除球。每帧只调用一次。
    ticks_to_next_ball -= 1
    if ticks_to_next_ball <= 0:
        create_ball()
        ticks_to_next_ball = 100
    # 移除低于100的球
    balls_to_remove = [ball for ball in balls if ball.body.position.y < 100]
    for ball in balls_to_remove:
        space.remove(ball, ball.body)
        balls.remove(ball)


'''
6.写侦听事件
这里我们介绍一下pygame中的截图方法
pygame.image.save(screen, “bouncing_balls.png”)
'''
def my_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        elif event.type == KEYDOWN and event.key == K_p:
            # 截图
            pygame.image.save(screen, "bouncing_balls.png")



# 清除屏幕
def clear_screen():
    screen.fill(THECOLORS["white"])

# 画对象
def draw_objects():
    space.debug_draw(draw_options)

'''
8.主循环
space.step(time)
空间运行time秒
'''
while True:
    # 计算下一帧位置
    for x in range(exact):
        space.step(1/FPS/exact)

    my_events()
    update_balls()
    clear_screen()
    draw_objects()
    pygame.display.flip()
    clock.tick(FPS)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
