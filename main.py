import pygame, random

#Prepare classes from classes.py
import classes
player_character = classes.Player()
#---

#load the test map
import map_core
test_map = map_core.init_test_map()
print(test_map.boundmap)
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
            
    #This wall handles movement for now. This will be moved to the Player class.
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_d]:
        player_character.x_position += 2
    if keys_pressed[pygame.K_a]:
        player_character.x_position -= 2
    if keys_pressed[pygame.K_w]:
        player_character.y_position -= 2
    if keys_pressed[pygame.K_s]:
        player_character.y_position += 2
            
    #Draw everything. See visual_core.py.
    visual_core.make_graphics(screen, player_character, test_map)
            
    pygame.display.flip()
    frame_limiter.tick(60)