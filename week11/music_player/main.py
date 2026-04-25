import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

player = MusicPlayer(screen)
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.handle_key(event.key)

    player.update()
    player.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()