import pygame, random, math
pygame.init()

import classes, visual_core, map_core

#--=[Modules]=--
import modules
MODULES = modules.all_modules
#---------------

current_map = map_core.load_map("map2")
player_character = classes.Player()
player_character.set_map(current_map) #Possibly needs reworking #Definitely needs reworking this is garbage

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
            
            if event.key == pygame.K_c:
                cmd = input("\n[Console]<< ").split()

                try:
                    if cmd[0] == "loadmap" and len(cmd) == 2:
                        current_map = map_core.load_map(cmd[1])
                        player_character.set_map(current_map)
                        
                    if cmd[0] == "setplayerpos" and len(cmd) == 3:
                        player_character.x_position = int(cmd[1])
                        player_character.y_position = int(cmd[2])
                except:
                    print("\n[Console]>> Command execution failed, please restart the game as this may cause severe corruption.")
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            for module_head in MODULES: module_head.handle_mousedown(event)
            
    #For movement
    if not game_main.is_paused:
        player_character.feed_info(game_main.dt, pygame.key.get_pressed() )
            
    #Draw everything. See visual_core.py.
    canvas_unscaled = visual_core.make_graphics(game_main.screen_size, game_main.canvas, player_character, current_map)
    
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