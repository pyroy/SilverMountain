import pygame

DEBUG_MODE = True

#adds tuples or lists such that (a, b) + (c, d) = (a + b, c + d)
def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]
    
#multiplies tuples or lists such that (a, b) * (c, d) = (a * b, c * d)
def tuple_mult(tup1, tup2):
    return [tup1[i] * tup2[i] for i in range(len(tup1))]

#draws everything and scales it up to screen size for pixelated effect.
def make_graphics(game_canvas, player_character, test_map):
    canvas_unscaled = pygame.Surface((320,320))
    
    canvas_unscaled.blit(test_map.alphamap, (0,0))
    canvas_unscaled.blit(player_character.get_sprite(), (player_character.x_position, player_character.y_position))
    
    print(test_map.check_bounds(player_character.get_bounds()))
    
    if DEBUG_MODE:
        for i in player_character.get_bounds():
            pygame.draw.circle(canvas_unscaled, (0,255,0), i, 2)
    
    game_canvas.blit(pygame.transform.scale(canvas_unscaled, (720,720)), (0,0))