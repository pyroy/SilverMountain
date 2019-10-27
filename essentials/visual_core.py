import pygame
import essentials.classes as classes
import classes.VisualCore

#I hate this python file
#this is the least likable python file I've ever seen
#I hate it. I just hate it so much
#It's just... it's kind of here. and it's one of the most important files in this project
#but it doesn't feel like it belongs here.
#why does this file exist?
#I hate it.
#I really really hate this stupid file, and its stupid single function definition

DEBUG_MODE = False
CAMERA_MODE = "Follow" #Fixed | Follow
CAMERA_OFFSET = (0,0)
VC = None
pc = None
sc = None

def setup(game_main, MODULES):
    global CAMERA_OFFSET, VC, pc, sc
    CAMERA_OFFSET = (game_main.unscaled_canvas_size[0]/2-8, game_main.unscaled_canvas_size[1]/2-8) #Shift to make player center of screen. Could also be used to pan.
    pc = MODULES.get_module("Essential::Player").player_character
    sc = MODULES.get_module("Essential::Scaler")
    VC = classes.VisualCore.VisualCore(game_main.screen_size, game_main.unscaled_canvas_size)

#draws everything and scales it up to screen size for pixelated effect.
def make_graphics(game_main):

    if "0gmap" not in VC.zoomed_layers:
        VC.add_items_to_layer( game_main.current_map.groundmap, "0gmap", mode = "zoomed" )
        VC.render_layer("0gmap", mode = "zoomed")
        
    if "0zmap" not in VC.zoomed_layers:
        VC.add_items_to_layer( game_main.current_map.zetamap, "0zmap", mode = "zoomed" )
        VC.render_layer("0zmap", mode = "zoomed")
       
    game_main.canvas.fill( (0,0,0) )
    game_main.canvas.blit( VC.render_all(), sc.scale((-pc.get_x()+CAMERA_OFFSET[0], -pc.get_y()+CAMERA_OFFSET[1])) )
    game_main.current_map.rendered_items.modify_pos((-pc.get_x()+CAMERA_OFFSET[0], -pc.get_y()+CAMERA_OFFSET[1]), 1)
    
#There is one glaring efficiency problem here, and that is that every frame 
#the game has to make a new canvas, blit a whole bunch of things on it, rescale and blit again.
#Maybe this could be fixed by prescaling all sprites and blitting it directly onto the screen.
#But that would also require camera reworking
#
#For now it runs fine.