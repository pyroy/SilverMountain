import sprites, pygame

#adds tuples or lists such that (a, b) + (c, d) = (a + b, c + d)
def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]

class Player:
    def __init__(self):
        self.x_position = 32
        self.y_position = 32
        self.bounding_box = [
            (6,6),
            (6,26),
            (26,6),
            (26,26)
            ]
        
    #In the future when inventory gets added, players look 
    #different based on what they're wearing.
    #This function will eventually handle that.
    def get_sprite(self):
        return sprites.player_sprite
        
    #returns the screen position of the four boundcheck corners
    def get_bounds(self):
        return [tuple_add(self.bounding_box[i], (self.x_position, self.y_position)) for i in range(4)]
        
class Map:
    def __init__(self, boundmap, groundmap, zetamap=None, betamap=None):
        self.boundmap = boundmap
        self.groundmap = groundmap
        self.zetamap = zetamap
        self.betamap = betamap
        self.alphamap = pygame.Surface((320,320))
        self.alphamap.blit(self.groundmap, (0,0))
        self.alphamap.blit(self.zetamap, (0,0))
        
    #Determines for any amount of boundcheck corners if they collide with the boundmap.
    def check_bounds(self, corners):
        corners_onmap = [self.convert_tup_mappos(i) for i in corners]
        return any( [self.boundmap[ c[1] ][ c[0] ] for c in corners_onmap] )
        
    #converts screen position to map position
    def convert_tup_mappos(self, tuple):
        return (tuple[0]//32, tuple[1]//32)