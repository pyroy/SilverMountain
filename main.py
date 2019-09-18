import pygame, random, math
pygame.init()

import classes, visual_core, map_core

#--=[Modules]=--
import modules
MODULES = modules.all_modules
#---------------

test_map = map_core.init_test_map()
player_character = classes.Player()
player_character.set_map(test_map) #Possibly needs reworking #Definitely needs reworking this is garbage

game_main = classes.Game()
game_main.set_title("Silver Mountain pre-alpha v0.125")
game_main.fps = 120 #if timescale mod is active, this variable will be hijacked

for module_head in MODULES: module_head.setup(game_main, player_character, MODULES)

while game_main.is_active:

    for module_head in MODULES:
        module_head.reset_mousedown()

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            game_main.is_active = False
            
        if event.type == pygame.KEYDOWN:
            for module_head in MODULES: module_head.handle_keydown(event)
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            for module_head in MODULES: module_head.handle_mousedown(event)
            
    #For movement
    if not game_main.is_paused:
        player_character.feed_info(game_main.dt, pygame.key.get_pressed() )
            
    #Draw everything. See visual_core.py.
    canvas_unscaled = visual_core.make_graphics(game_main.screen_size, game_main.canvas, player_character, test_map)
    
    for module_head in MODULES:
        module_head.make_scaled_graphics(game_main, player_character, MODULES, visual_core, canvas_unscaled)
        
    game_main.canvas.blit(pygame.transform.scale(canvas_unscaled, game_main.screen_size), (0,0))
    
    for module_head in MODULES:
        module_head.run_frame(game_main, player_character, MODULES)
        module_head.make_graphics(game_main, player_character, MODULES, visual_core)

    game_main.next_frame() 
    
    
#Issues:
# - [low priority] game cannot do collision checks under 10 fps due to bad delta time coding
# - [medium priority] certain modules are vague and inefficient and should really be (semi-)hardcoded