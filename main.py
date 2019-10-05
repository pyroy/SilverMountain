import pygame, random, math
pygame.init()

import essentials.classes as classes
import essentials.visual_core as visual_core
import essentials.map_core as map_core

#--=[Modules]=--
import modules
MODULES = modules.MODULES
ALL_MODULES = MODULES.get_all_modules()
#---------------

#game_main is our main game controller. all the game variables will be set in this class.
game_main = classes.Game()
game_main.set_title("Silver Mountain pre-alpha v0.14285714286")
game_main.set_target_fps(120)
game_main.unscaled_canvas_size = (240, 135)
game_main.screen_size = (1280, 720)

#maps load from map_core
game_main.set_map( map_core.new_load_map("test_map") )

#setup all modules
for module_head in ALL_MODULES: module_head.setup(game_main, MODULES)

visual_core.setup(game_main)

#if a command is initiated by pressing c, this runs the command
def execute_command(cmd):
    if cmd[0] == "help" and len(cmd) == 1:
        print("[Console]>> - loadmap [map]")
        print("            - setplayerpos (x) (y)")
        print("            - getinfo [module]")
        print("            - removetile [ground | zeta | beta] (x) (y)")
        print("            - settile [ground | zeta | beta] (x) (y) [tilename]")
        print("            - settimescale (scale)")
        print("            - settargetfps (fps)")
        
    if cmd[0] == "loadmap" and len(cmd) == 2:
        game_main.set_map( map_core.load_map(cmd[1]) )
        player_character = MODULES.get_module("Essential::Player").player_character
        player_character.set_map(game_main.current_map)
                        
    if cmd[0] == "setplayerpos" and len(cmd) == 3:
        player_character = MODULES.get_module("Essential::Player").player_character
        player_character.set_pos( int(cmd[1]), int(cmd[2]) )
        
    if cmd[0] == "getinfo" and len(cmd) == 2:
        print(" ")
        MODULES.get_module(cmd[1]).info()
        
    if cmd[0] == "removetile" and cmd[1] == "zeta" and len(cmd) == 4: 
        game_main.current_map.update_zetamap((int(cmd[2]),int(cmd[3])), "")
        
    if cmd[0] == "settile" and cmd[1] == "zeta" and len(cmd) == 5: 
        game_main.current_map.update_zetamap((int(cmd[2]),int(cmd[3])), cmd[4])
        
    if cmd[0] == "settimescale" and len(cmd) == 2:
        game_main.timescale = float(cmd[1])
        
    if cmd[0] == "settargetfps" and len(cmd) == 2:
        game_main.set_target_fps( float(cmd[1]) )

#variable to store click information for the handle_mouseclick function @ line 84
clicked = False

#game loop
while game_main.is_active:

    #at the very beginning of every frame, this function is run for all modules
    #currently used for resetting mouse click variables
    for module_head in ALL_MODULES: module_head.start_new_frame()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_main.is_active = False
            
        if event.type == pygame.KEYDOWN:
            #just feed the KEYDOWN event to all modules, let them handle it
            for module_head in ALL_MODULES: module_head.handle_keydown(event)
            
            #and if C is pressed, input a command
            if event.key == pygame.K_c:
                cmd = input("\n[Console]<< ").split()
                try: execute_command(cmd)
                except:
                    print("\n[Console]>> Command execution failed, please restart the game as this may cause severe corruption.")
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            #again, feed the event to the modules, let them decide what to do with it
            for module_head in ALL_MODULES: module_head.handle_mousedown(event)
            
            #send a mouseclick event if a mouseup event has happened since the last mouseclick event
            if not clicked:
                for module_head in ALL_MODULES: module_head.handle_mouseclick(event)
                clicked = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            #feed mouseup event to modules
            for module_head in ALL_MODULES: module_head.handle_mouseup(event)
            
            #and reset the mouseclick variable @ line 84
            clicked = False
            
    game_main.keys_pressed = pygame.key.get_pressed()
    game_main.mouse_pos = pygame.mouse.get_pos()
            
    #draw everything on unscaled canvas, see visual_core.py
    canvas_unscaled = visual_core.make_graphics(game_main, MODULES)
    
    #let the modules also draw on the unscaled canvas
    for module_head in ALL_MODULES:
        module_head.make_scaled_graphics(game_main, MODULES, visual_core, canvas_unscaled)
        
    #scale the unscaled canvas to fit the screen
    game_main.canvas.blit(pygame.transform.scale(canvas_unscaled, game_main.screen_size), (0,0))
    
    #then run each frame and draw unscaled graphics over the screen
    #also needs reworking, who calculates frames after scaled graphics, but before unscaled graphics?
    for module_head in ALL_MODULES:
        module_head.run_frame(game_main, MODULES)
        module_head.make_graphics(game_main, MODULES, visual_core)

    #advance my child
    game_main.next_frame() 