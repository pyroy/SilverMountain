import pygame, random
pygame.init()

#load the test map
import map_core
test_map = map_core.init_test_map()

#Prepare classes from classes.py
import classes
player_character = classes.Player()
player_character.set_map(test_map) #Possibly needs reworking

#this will draw everything on screen
import visual_core

SCREEN_SIZE = (720,720)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Silver Mountain pre-alpha v0.1")
frame_limiter = pygame.time.Clock()
game_loop_active = True
game_paused = False
dt = 0

#--=[Modules]=--
import modules
MODULES = modules.all_modules
#---------------

#game loop (duh)
while game_loop_active:
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            game_loop_active = False
            
        if event.type == pygame.KEYDOWN:
            for module_head in MODULES:
                module_head.handle_keydown(event)
            
    #For movement
    if not game_paused:
        player_character.feed_info(dt, pygame.key.get_pressed() )
            
    #Draw everything. See visual_core.py.
    visual_core.make_graphics(SCREEN_SIZE, screen, player_character, test_map)
            
    pygame.display.flip()
    dt = frame_limiter.tick(120) #game cannot function under 10fps