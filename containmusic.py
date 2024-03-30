import pygame.sprite.Sprite
import pygame

# 初始化Pygame
pygame.init()

# 设置窗口大小
size = (700, 500)
screen = pygame.display.set_mode(size)

# 设置窗口标题
pygame.display.set_caption("My Game")



class MySprite(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([50, 50])
        	self.image.fill((255, 0, 0))
        	self.rect = self.image.get_rect()
        	self.rect.x = 50
        	self.rect.y = 50
        	
my_group = pygame.sprite.Group()
my_sprite = MySprite()
my_group.add(my_sprite)

# 检测碰撞
collision_list = pygame.sprite.spritecollide(my_sprite, other_group, False)
if collision_list:
print("碰撞了！")


# 加载音乐
pygame.mixer.music.load("music/music.mp3")

# 播放音乐
pygame.mixer.music.play(-1)

# 创建时钟对象
clock = pygame.time.Clock()

# 游戏循环
done = False
while not done:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                my_sprite.rect.x -= 10
            elif event.key == pygame.K_RIGHT:
                my_sprite.rect.x += 10
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("鼠标点击")

    # 绘制背景
    screen.fill((255, 255, 255))

    # 绘制精灵
    my_group.draw(screen)

    # 更新窗口
    pygame.display.update()

    # 控制游戏帧率
    clock.tick(60)

# 退出Pygame
pygame.quit()
