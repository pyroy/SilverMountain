import pygame

def make_graphics(game_canvas, player_character, test_map):
    canvas_unscaled = pygame.Surface((320,320))
    
    canvas_unscaled.blit(test_map.alphamap, (0,0))
    canvas_unscaled.blit(player_character.get_sprite(), (player_character.x_position, player_character.y_position))
    
    game_canvas.blit(pygame.transform.scale(canvas_unscaled, (720,720)), (0,0))