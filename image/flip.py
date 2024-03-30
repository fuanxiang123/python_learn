import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))

image = pygame.image.load('image.png')
flipped_image = pygame.transform.flip(image, False, True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(flipped_image, (100, 100))
    pygame.display.flip()

pygame.quit()

