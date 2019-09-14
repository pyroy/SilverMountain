import pygame, random

#load the test map
import map_core
test_map = map_core.init_test_map()
print(test_map.boundmap)
#---

#Prepare classes from classes.py
import classes
player_character = classes.Player()
player_character.set_map(test_map)
#---

#load all the sprites
import sprites
#---

#this will draw everything on screen
import visual_core
#---

screen = pygame.display.set_mode((720,720))
frame_limiter = pygame.time.Clock()
game_loop_active = True

while game_loop_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop_active = False
            
    #For movement
    player_character.feed_keypresses( pygame.key.get_pressed() )
            
    #Draw everything. See visual_core.py.
    visual_core.make_graphics(screen, player_character, test_map)
            
    pygame.display.flip()
    frame_limiter.tick(60)