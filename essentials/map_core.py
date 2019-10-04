import pygame, random
import json
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
    
def new_load_map(map_name):
    with open("maps/{}/groundmap.txt".format(map_name)) as map_file:
        g_map_txt = map_file.readlines()
    
    with open("maps/{}/zetamap.txt".format(map_name)) as map_file:
        z_map_txt = map_file.readlines()
        
    with open("maps/{}/zetamap.json".format(map_name)) as map_file:
        z_json = json.load(map_file)
        
    #groundmap
    g_b_point = g_map_txt.index("---\n")
    map_height = g_b_point
    map_width = len( g_map_txt[0].replace("\n","").split(";") )
    g_map_dict = {}
    
    for i in range(g_b_point+1, len(g_map_txt)):
        line = g_map_txt[i].replace("\n","").split(":")
        g_map_dict[ line[0] ] = line[1]
    
    groundmap = pygame.Surface((TILE_SIZE*map_width, TILE_SIZE*map_height))
    for y in range(map_height):
        row = g_map_txt[y].replace("\n","").split(";")
        for x in range(map_width):
            tile = g_map_dict[row[x]]
            groundmap.blit(pygame.transform.rotate(sprites.IDS[ tile ], 90*random.randint(0,3)), (x*TILE_SIZE, y*TILE_SIZE))
            rendered_items.add_item(pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), (x*TILE_SIZE, y*TILE_SIZE), data={'id':tile,'x':x*TILE_SIZE,'y':y*TILE_SIZE}, name=tile, type="groundtile")
    
    #zetamap
    z_b_point = z_map_txt.index("---\n")
    
    if z_b_point != map_height or len( z_map_txt[0].replace("\n","").split(";") ) != map_width:
        print("Mismatch in groundmap and zetamap sizes!")
        return "epic"
    
    z_map_dict = {}
    
    for i in range(z_b_point+1, len(z_map_txt)):
        line = z_map_txt[i].replace("\n","").split(":")
        z_map_dict[ line[0] ] = line[1]
        
    zetamap = pygame.Surface((TILE_SIZE*map_width, TILE_SIZE*map_height), pygame.SRCALPHA, 32)
    boundmap = [[0 for i in range(0, map_width)] for c in range(0, map_height)]
    
    for y in range(map_height):
        row = z_map_txt[y].replace("\n","").split(";")
        for x in range(map_width):
            tile = z_map_dict[row[x]]
            if tile == 'void':
                continue
            tile_sprites = z_json[tile]["sprites"]
            tile_sprite = tile_sprites[0]
            tile_data = {'id':tile,'x':x*TILE_SIZE,'y':y*TILE_SIZE}
            tile_data.update( z_json[tile]["data"] )
            tile_has_collision = int( z_json[tile]["collision"] )
            
            
            zetamap.blit(sprites.IDS[tile_sprite], (x*TILE_SIZE, y*TILE_SIZE))
            rendered_items.add_item(pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), (x*TILE_SIZE, y*TILE_SIZE), data=tile_data, name=tile, type="zetatile")
            boundmap[y][x] = tile_has_collision
    
    return classes.Map(boundmap, groundmap, rendered_items, zetamap)
    
def load_map(map_name):
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
            
                zetamap.blit(sprites.IDS["tile_warp"], (i*TILE_SIZE, j*TILE_SIZE))
                rendered_items.add_item(pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), (i*TILE_SIZE, j*TILE_SIZE), data={'id':'map_warp','x':i*TILE_SIZE,'y':j*TILE_SIZE,'destination':'map1','desc':'Map 1','warp_x':16,'warp_y':16}, name="map_warp", type="warp")
                
            else:
            
                boundmap[j][i] = 0
                
    return classes.Map(boundmap, groundmap, rendered_items, zetamap)