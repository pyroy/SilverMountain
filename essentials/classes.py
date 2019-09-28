import pygame
import essentials.sprites as sprites

#adds tuples or lists such that (a, b) + (c, d) = (a + b, c + d)
def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]

class Game:
    def __init__(self):
    
        #everything should be pretty self explanatory here.
        self.is_active = True
        self.is_paused = False
        self.screen_size = (720, 720)
        self.canvas = pygame.display.set_mode(self.screen_size)
        self.frame_limiter = pygame.time.Clock()
        self.dt = 0
        self.fps = 60
        self.timescale = 1 #lol
        self.frameno = 0
        self.keys_pressed = []
        
        #sets the map currently active (mainly for graphics)
        self.current_map = None
        
    def next_frame(self):
    
        #calculate dt and increase framecounter
        pygame.display.flip()
        self.dt = abs(self.frame_limiter.tick(self.fps)*self.timescale)
        self.frameno += 1
        
    def set_title(self, title):
        pygame.display.set_caption(title)

class Player:
    def __init__(self):
        self.x_position = 32
        self.y_position = 32
        
        #used for collision checks @ line 58
        self.bounding_box = [
            (6,6),
            (6,26),
            (26,6),
            (26,26)
            ]
            
        self.map = None
        
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
            print("[Console/W]>> Player map not set!")
            return
    
        #just check bounds everywhere you try to move
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
        #keys are in DDR order. do not move if relevant keys are not being pressed
        if any( [keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_RIGHT]] ):
            self.move(dt, [keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_RIGHT]])
        
class Map:
    def __init__(self, boundmap, groundmap, rendered_items, zetamap=None, betamap=None):
    
        #more info on what the f*** all these terms mean in map_core.py
        self.map_size = (len(boundmap), len(boundmap[0]))
        self.boundmap = boundmap
        self.groundmap = groundmap
        self.zetamap = zetamap
        self.betamap = betamap
        self.rendered_items = rendered_items
        self.alphamap = None
        self.process_alphamap()
        
    def process_alphamap(self):
    
        #again, see map_core.py
        self.alphamap = pygame.Surface((32*len(self.boundmap[0]),32*len(self.boundmap)))
        self.alphamap.blit(self.groundmap, (0,0))
        self.alphamap.blit(self.zetamap, (0,0))
        
    def check_bounds(self, corners):
    
        #Determines for any amount of boundcheck corners if they collide with the boundmap.
        corners_onmap = [self.convert_tup_mappos(i) for i in corners]
        try:
            return any( [self.boundmap[ c[1] ][ c[0] ] for c in corners_onmap] )
        except:
            #catches when OOB
            return True
        
    def convert_tup_mappos(self, tuple):
    
        #converts screen position to map position. Returns None if coordinates lie OOB.
        x, y = int(tuple[0]//32), int(tuple[1]//32)
        
        if x < 0 or x > self.map_size[1]:
            x = None
            
        if y < 0 or y > self.map_size[0]:
            y = None 
            
        return (x, y)
        
    def update_zetamap(self, pos, env):
        #clear the part to be updated
        self.zetamap.fill( (0,0,0,0), (pos[0]*32, pos[1]*32, 32, 32) )
        
        #and remove the bound
        self.boundmap[pos[1]][pos[0]] = 0
        
        #get the RenderedItem at the specified position
        for i in self.rendered_items.get_items( data=[ ("x", pos[0]*32), ("y", pos[1]*32) ] ):
        
            #im sorry little one
            self.rendered_items.remove_item(i)
        
        if env != "":
        
            #if a replacement tile is specified, rejoice
            self.zetamap.blit( sprites.IDS[env], pos )
            self.boundmap[pos[1]][pos[0]] = 1
            
            #re-add specified tile to the RenderedItems list
            self.rendered_items.add_item(pygame.Rect(0,0,32,32), (pos[0]*32, pos[1]*32), data={'id':env,'x':pos[0]*32,'y':pos[1]*32}, name=env, type="zetatile")
            
        #re-make the alphamap with the updated zetamap
        self.process_alphamap()
        
#see RenderedItems
class RenderedItem:
    def __init__(self, rect, drawn_pos, data, name, type):
        self.rect = rect
        self.drawn_pos = drawn_pos
        self.data = data
        self.name = name
        self.type = type
        
        #offset is used in get_drawnpos literally only for getting the right position for mouse click detection on tiles
        self.offset = (0,0)
    
    def get_drawnpos(self):
        return tuple_add(self.drawn_pos, self.offset)
        
#RenderedItems stores the list of graphical objects rendered, and gives them meaning (data)
#Exempli Gratia: player inventory uses a RenderedItems class to know what label that was drawn corresponds to what item_db class.
#also supports type/data filtering
class RenderedItems:
    def __init__(self):
        self.raw_list = []
        
    def add_item(self, rect, drawn_pos, data={}, name="", type="NoType"):
        self.raw_list.append( RenderedItem(rect, drawn_pos, data, name, type) )
        
    def get_items(self, type="", data=[]):
    
        #return all items passing the type/data filter
        
        if type != "":
            return [i for i in self.raw_list if i.type == type]
            
        elif data != []:
            l = []
            for item in self.raw_list:
                m = True
                for match in data:
                    if not (match[0] in item.data and item.data[match[0]] == match[1]):
                        m = False
                if m: l.append(item)
            return l
            
        else:
            return self.raw_list
            
    def remove_item(self, item):
        self.raw_list.remove(item)
        
    def in_rect(self, rect, mouse, drawn_pos=(0,0)):
    
        #mama mia, look at all this spaghetti!
        #pretty sure these checks aren't even 100% accurate but we'll see
        return mouse[0] >= rect.left+drawn_pos[0] and mouse[0] <= rect.right+drawn_pos[0] and mouse[1] >= drawn_pos[1] and mouse[1] <= rect.bottom+drawn_pos[1]
        
    def get_items_clicked(self, mouse_pos, type="", data=[]):
    
        #returns list of RenderedItem classes where mouse_pos is in the get_drawnpos() rect, meaning the mouse cursor is on the RenderedItem.
        return [i for i in self.get_items(type, data) if self.in_rect(i.rect, mouse_pos, i.get_drawnpos())]
        
    def modify_pos(self, offset, scale, types):
        #applies a linear transformation to RenderedItem offset
        for t in types:
            for i in self.get_items(t):
                i.offset = (offset[0]*scale, offset[1]*scale)
    
    def reset(self):
        self.raw_list = []