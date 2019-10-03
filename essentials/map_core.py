import pygame, random
import essentials.sprites as sprites
import essentials.classes as classes

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
    
rendered_items = classes.RenderedItems()
    
TILE_SIZE = 16
    
def load_map(map_name):
    map_data = []
    with open("maps/{}.txt".format(map_name)) as map_file:
        l = map_file.readlines()
        map_width = len(l[0]) - 1
        map_height = len(l)

    groundmap = pygame.Surface((TILE_SIZE*map_width, TILE_SIZE*map_height))
    zetamap = pygame.Surface((TILE_SIZE*map_width, TILE_SIZE*map_height), pygame.SRCALPHA, 32)
    boundmap = [[0 for i in range(0, map_width)] for c in range(0, map_height)]
    
    for i in range(0, map_width):
        for j in range(0, map_height):
        
            groundmap.blit(pygame.transform.rotate(sprites.tile_dirt, 90*random.randint(0,3)), (i*TILE_SIZE, j*TILE_SIZE))
            rendered_items.add_item(pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), (i*TILE_SIZE, j*TILE_SIZE), data={'id':'tile_dirt','x':i*TILE_SIZE,'y':j*TILE_SIZE}, name="tile_dirt", type="groundtile")
            
            if l[j][i] == '1':
            
                zetamap.blit(sprites.env_stone, (i*TILE_SIZE, j*TILE_SIZE))
                rendered_items.add_item(pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), (i*TILE_SIZE, j*TILE_SIZE), data={'id':'env_stone','x':i*TILE_SIZE,'y':j*TILE_SIZE}, name="env_stone", type="zetatile")
                boundmap[j][i] = 1
                
            elif l[j][i] == '2':
            
                zetamap.blit(sprites.env_ore, (i*TILE_SIZE, j*TILE_SIZE))
                rendered_items.add_item(pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), (i*TILE_SIZE, j*TILE_SIZE), data={'id':'env_ore','x':i*TILE_SIZE,'y':j*TILE_SIZE,'drop':'ironore','minetime':200,'mined':200}, name="env_ore", type="zetatile")
                boundmap[j][i] = 1
                
            elif l[j][i] == '3':
            
                rendered_items.add_item(pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), (i*TILE_SIZE, j*TILE_SIZE), data={'id':'map_warp','x':i*TILE_SIZE,'y':j*TILE_SIZE,'destination':'map1'}, name="map_warp", type="warp")
                
            else:
            
                boundmap[j][i] = 0
                
    return classes.Map(boundmap, groundmap, rendered_items, zetamap)