import pygame
import essentials.classes as classes

#I hate this python file
#this is the least likable python file I've ever seen
#I hate it. I just hate it so much
#and I don't know why. It does its job but, man, I hate it
#It's just... it's kind of here. and it's one of the most important files in this project
#but it doesn't feel like it belongs here.
#why does this file exist?
#I hate it.
#I really really hate this stupid file, and its stupid single function definition

DEBUG_MODE = False
UNSCALED_CANVAS_SIZE = (320, 320)
CAMERA_MODE = "Follow" #Fixed | Follow
CAMERA_OFFSET = (UNSCALED_CANVAS_SIZE[0]/2-16, UNSCALED_CANVAS_SIZE[1]/2-16) #Shift to make player center of screen. Could also be used to pan.

#draws everything and scales it up to screen size for pixelated effect.
def make_graphics(game_main, MODULES):

    player_character = MODULES.get_module("Essential::Player").player_character
    
    canvas_unscaled = pygame.Surface(UNSCALED_CANVAS_SIZE)
    
    if CAMERA_MODE == "Fixed": #this one for dungeons and other interior spaces
        canvas_unscaled.blit(game_main.current_map.alphamap, (0,0))
        canvas_unscaled.blit(player_character.get_sprite(), (player_character.x_position, player_character.y_position))
        
    elif CAMERA_MODE == "Follow": #this one for overworld
        canvas_unscaled.blit(game_main.current_map.alphamap, (-player_character.x_position+CAMERA_OFFSET[0], -player_character.y_position+CAMERA_OFFSET[1]))
        canvas_unscaled.blit(player_character.get_sprite(), CAMERA_OFFSET)
    
    game_main.current_map.rendered_items.modify_pos((-player_character.x_position+CAMERA_OFFSET[0], -player_character.y_position+CAMERA_OFFSET[1]), 1, ["groundtile","zetatile"])
    
    return canvas_unscaled
    
#There is one glaring efficiency problem here, and that is that every frame 
#the game has to make a new canvas, blit a whole bunch of things on it, rescale and blit again.
#Maybe this could be fixed by prescaling all sprites and blitting it directly onto the screen.
#But that would also require camera reworking
#
#For now it runs fine.