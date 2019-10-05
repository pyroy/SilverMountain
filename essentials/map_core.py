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
    
TILE_SIZE = 16
    
def new_load_map(map_name):
    rendered_items = classes.RenderedItems()
    
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
            if "sharedjson" in z_json[tile]:
                sharedjson = z_json[tile]["sharedjson"]
                
                with open("blocks/{}.json".format(sharedjson)) as origin_file:
                    origin_data = json.load(origin_file)
                    
                tile_sprites = origin_data["sprites"]
                tile_sprite = tile_sprites[0]
                tile_data = {'id':tile,'x':x*TILE_SIZE,'y':y*TILE_SIZE}
                tile_data.update( origin_data )
                tile_data.update( z_json[tile]["extradata"] )
                tile_has_collision = int( origin_data["collision"] )
            else:
                tile_sprites = z_json[tile]["sprites"]
                tile_sprite = tile_sprites[0]
                tile_data = {'id':tile,'x':x*TILE_SIZE,'y':y*TILE_SIZE}
                tile_data.update( z_json[tile]["data"] )
                tile_has_collision = int( z_json[tile]["collision"] )
            
            zetamap.blit(sprites.IDS[tile_sprite], (x*TILE_SIZE, y*TILE_SIZE))
            rendered_items.add_item(pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), (x*TILE_SIZE, y*TILE_SIZE), data=tile_data, name=tile, type="zetatile")
            boundmap[y][x] = tile_has_collision
    
    return classes.Map(boundmap, groundmap, rendered_items, zetamap)