import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))

image = pygame.image.load('image.png')
rotated_image = pygame.transform.rotate(image, 45)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(rotated_image, (100, 100))
    pygame.display.flip()

pygame.quit()
