import sprites, pygame

#adds tuples or lists such that (a, b) + (c, d) = (a + b, c + d)
def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]

class Item:
    def __init__(self, id):
        self.id = id
        self.sprite = sprites.IDS[self.id]
        self.weight = 0
        self.value = 0

class Itemcontainer:
    def __init__(self, items=[]):
        self.items = items

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
        self.map = None
        
        self.inventory = Itemcontainer([ Item("test_pick"), Item("test_pick"), Item("test_pick")])
        
    #In the future when inventory gets added, players look 
    #different based on what they're wearing.
    #This function will eventually handle that.
    def get_sprite(self):
        return sprites.player_sprite
        
    def set_map(self, map):
        self.map = map
        
    #returns the screen position of the four boundcheck corners
    def get_bounds(self):
        return [tuple_add(self.bounding_box[i], (self.x_position, self.y_position)) for i in range(4)]
        
    def move(self, dt, directions):
        if self.map == None: 
            print("WARNING: player map not set.")
            return
    
        self.speed = 2/17*dt
    
        if directions[0]:
            self.x_position -= self.speed
            if self.map.check_bounds(self.get_bounds()):
                self.x_position += self.speed
                
        if directions[1]:
            self.y_position += self.speed
            if self.map.check_bounds(self.get_bounds()):
                self.y_position -= self.speed
        
        if directions[2]:
            self.y_position -= self.speed
            if self.map.check_bounds(self.get_bounds()):
                self.y_position += self.speed
                
        if directions[3]:
            self.x_position += self.speed
            if self.map.check_bounds(self.get_bounds()):
                self.x_position -= self.speed
        
    def feed_info(self, dt, keys):
        if any( [keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_RIGHT]] ): #DDR order
            self.move(dt, [keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_RIGHT]])
        
class Map:
    def __init__(self, boundmap, groundmap, zetamap=None, betamap=None):
        self.boundmap = boundmap
        self.groundmap = groundmap
        self.zetamap = zetamap
        self.betamap = betamap
        self.alphamap = pygame.Surface((320,320))
        self.alphamap.blit(self.groundmap, (0,0))
        self.alphamap.blit(self.zetamap, (0,0))
        self.map_size = (len(boundmap), len(boundmap[0]))
        
    #Determines for any amount of boundcheck corners if they collide with the boundmap.
    def check_bounds(self, corners):
        corners_onmap = [self.convert_tup_mappos(i) for i in corners]
        try: #Catches when checking borders of the map
            return any( [self.boundmap[ c[1] ][ c[0] ] for c in corners_onmap] )
        except:
            return True
        
    #converts screen position to map position. Returns None if coordinates lie OOB.
    def convert_tup_mappos(self, tuple):
        x, y = int(tuple[0]//32), int(tuple[1]//32)
        if x < 0 or x > self.map_size[1]:
            x = None
        if y < 0 or y > self.map_size[0]:
            y = None 
        return (x, y)