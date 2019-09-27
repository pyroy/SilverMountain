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
    
def load_map(map_name):
    map_data = []
    with open("maps/{}.txt".format(map_name)) as map_file:
        l = map_file.readlines()
        map_width = len(l[0]) - 1
        map_height = len(l)

    groundmap = pygame.Surface((32*map_width, 32*map_height))
    zetamap = pygame.Surface((32*map_width, 32*map_height), pygame.SRCALPHA, 32)
    boundmap = [[0 for i in range(0, map_width)] for c in range(0, map_height)]
    
    for i in range(0, map_width):
        for j in range(0, map_height):
            groundmap.blit(pygame.transform.rotate(sprites.tile_dirt, 90*random.randint(0,3)), (i*32, j*32))
            if l[j][i] == '1':
                zetamap.blit(sprites.env_stone, (i*32, j*32))
                boundmap[j][i] = 1
            else:
                boundmap[j][i] = 0
                
    return classes.Map(boundmap, groundmap, zetamap)