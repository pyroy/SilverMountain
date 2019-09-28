import pygame, random, math
pygame.init()

import classes, visual_core, map_core

#--=[Modules]=--
import modules
MODULES = modules.MODULES
ALL_MODULES = MODULES.get_all_modules()
#---------------

game_main = classes.Game()
game_main.set_title("Silver Mountain pre-alpha v0.125")
game_main.fps = 120

game_main.current_map = map_core.load_map("map2")
player_character = classes.Player()
player_character.set_map(game_main.current_map) #Possibly needs reworking #Definitely needs reworking this is garbage (see priority list)

for module_head in ALL_MODULES: module_head.setup(game_main, player_character, MODULES)

def execute_command(cmd):
    if cmd[0] == "loadmap" and len(cmd) == 2:
        game_main.current_map = map_core.load_map(cmd[1])
        player_character.set_map(game_main.current_map)
                        
    if cmd[0] == "setplayerpos" and len(cmd) == 3:
        player_character.x_position = int(cmd[1])
        player_character.y_position = int(cmd[2])
        
    if cmd[0] == "getinfo" and len(cmd) == 2:
        MODULES.get_module(cmd[1]).info()
        
    if cmd[0] == "removetile" and cmd[1] == "zeta" and len(cmd) == 4: 
        game_main.current_map.update_zetamap((int(cmd[2]),int(cmd[3])), "")
        
    if cmd[0] == "settile" and cmd[1] == "zeta" and len(cmd) == 5: 
        game_main.current_map.update_zetamap((int(cmd[2]),int(cmd[3])), cmd[4])
        
    if cmd[0] == "settimescale" and len(cmd) == 2:
        game_main.timescale = float(cmd[1])
        
    if cmd[0] == "settargetfps" and len(cmd) == 2:
        game_main.fps = float(cmd[1])

clicked = False
while game_main.is_active:

    for module_head in ALL_MODULES: module_head.start_new_frame()

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            game_main.is_active = False
            
        if event.type == pygame.KEYDOWN:
            for module_head in ALL_MODULES: module_head.handle_keydown(event)
            
            if event.key == pygame.K_c:
                cmd = input("\n[Console]<< ").split()
                execute_command(cmd)
                #try: execute_command(cmd)
                #except:
                #    print("\n[Console]>> Command execution failed, please restart the game as this may cause severe corruption.")
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            for module_head in ALL_MODULES: module_head.handle_mousedown(event)
            if not clicked:
                for module_head in ALL_MODULES: module_head.handle_mouseclick(event)
                clicked = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            for module_head in ALL_MODULES: module_head.handle_mouseup(event)
            clicked = False
            
    #For movement
    if not game_main.is_paused:
        player_character.feed_info(game_main.dt, pygame.key.get_pressed() )
            
    #Draw everything. See visual_core.py.
    canvas_unscaled = visual_core.make_graphics(game_main.screen_size, game_main.canvas, player_character, game_main.current_map)
    
    for module_head in ALL_MODULES:
        module_head.make_scaled_graphics(game_main, player_character, MODULES, visual_core, canvas_unscaled)
        
    game_main.canvas.blit(pygame.transform.scale(canvas_unscaled, game_main.screen_size), (0,0))
    #game_main.canvas.blit(canvas_unscaled, (0,0))
    
    for module_head in ALL_MODULES:
        module_head.run_frame(game_main, player_character, MODULES)
        module_head.make_graphics(game_main, player_character, MODULES, visual_core)

    game_main.next_frame() 
    
    
#Issues:
# - [high priority] translate visual_core & player_character into modules for cleaner & more consistent main.py code
# - [0 priority] game cannot do collision checks under 10 fps due to bad delta time coding
# - [discarded] certain modules are vague and inefficient and should really be (semi-)hardcoded