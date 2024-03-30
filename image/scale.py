import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))

image = pygame.image.load('image.png')
scaled_image = pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(scaled_image, (100, 100))
    pygame.display.flip()

pygame.quit()

