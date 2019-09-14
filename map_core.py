import pygame, sprites, classes
import random

#  Map drawing order
#
#     groundmap
#        V          } alphamap
#     zetamap
#        V
#(main.py rendering)
#        V
#     betamap
#
#A map object has three items:
#The alphamap, the boundmap, and the betamap.
#
#In the future, zetamap drawing will require some restructuring due to
#Player perspective (behind vs. in front of a rock.)

def init_test_map():
    groundmap = pygame.Surface((320,320))
    zetamap = pygame.Surface((320,320), pygame.SRCALPHA, 32)
    boundmap = [[0 for i in range(0,10)] for c in range(0,10)]
    
    for i in range(0,10):
        for j in range(0,10):
            groundmap.blit(pygame.transform.rotate(sprites.tile_dirt, 90*random.randint(0,3)), (i*32, j*32)) #groundmap
            if random.randint(0,5) == 0:
                zetamap.blit(sprites.env_stone, (i*32, j*32)) #improvised zetamap
                boundmap[j][i] = 1 #the format for boundchecks is boundmap[y][x]
                
    return classes.Map(boundmap, groundmap, zetamap)