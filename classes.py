import sprites, pygame

class Player:
    def __init__(self):
        self.x_position = 32
        self.y_position = 32
    def get_sprite(self):
        return sprites.player_sprite
        
class Map:
    def __init__(self, boundmap, groundmap, zetamap=None, betamap=None):
        self.boundmap = boundmap
        self.groundmap = groundmap
        self.zetamap = zetamap
        self.betamap = betamap
        self.alphamap = pygame.Surface((320,320))
        self.alphamap.blit(self.groundmap, (0,0))
        self.alphamap.blit(self.zetamap, (0,0))