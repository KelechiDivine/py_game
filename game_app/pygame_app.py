import pygame, sys
from pygame.locals import *

pygame.init()

Display_Game_By_Kelechi = pygame.display.set_mode((490, 390))
pygame.display.set_caption("Kelechi Divine")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()

