import pygame, random, math
pygame.init()

import classes, visual_core, map_core

#--=[Modules]=--
import modules
MODULES = modules.all_modules
#---------------

test_map = map_core.init_test_map()
player_character = classes.Player()
player_character.set_map(test_map) #Possibly needs reworking

game_main = classes.Game()
game_main.set_title("Silver Mountain pre-alpha v0.1111111111111111")
game_main.fps = 120

while game_main.is_active:
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            game_main.is_active = False
            
        if event.type == pygame.KEYDOWN:
            for module_head in MODULES:
                module_head.handle_keydown(event)
            
    #For movement
    if not game_main.is_paused:
        player_character.feed_info(game_main.dt, pygame.key.get_pressed() )
            
    #Draw everything. See visual_core.py.
    visual_core.make_graphics(game_main.screen_size, game_main.canvas, player_character, test_map)

    game_main.next_frame() 
    
    
#Issues:
# - game cannot do collision checks under 10 fps
# - certain modules are vague and inefficient and should really be (semi-)hardcoded