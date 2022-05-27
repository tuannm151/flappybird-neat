import pygame
import os
from constants import WIN_WIDTH, WIN_HEIGHT

# ------ character animation sprites----------

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('sprites', 'redbird-midflap.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('sprites', 'redbird-downflap.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('sprites', 'redbird-upflap.png'))),
]
# ------------------------------------ #

#---------- Obstacles sprites----------------#
BG_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join('sprites', 'bg-game.png')), (WIN_WIDTH, WIN_HEIGHT))

OB_TOP = []
for picIndex in range(4):
    image = pygame.image.load(os.path.join(
        'obstacles', 'tow'+str(picIndex+1)+'.png'))
    OB_TOP.append(image)

OB_BOTTOM = []
for picIndex in range(5):
    image = pygame.image.load(os.path.join(
        'obstacles', 'vol'+str(picIndex+1)+'.png'))
    OB_BOTTOM.append(image)
OB_TERRAIN = []
for picIndex in range(2):
    image = pygame.image.load(os.path.join(
        'obstacles', 'ter'+str(picIndex+1)+'.png'))
    OB_TERRAIN.append(image)
# ----------------------------------------------#



