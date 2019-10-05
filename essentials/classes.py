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
        self.screen_size = (1280, 720)
        self.unscaled_canvas_size = (320, 320)
        self.canvas = pygame.display.set_mode(self.screen_size)
        self.frame_limiter = pygame.time.Clock()
        self.dt = 0
        self.fps = 60
        self.timescale = 1 #lol
        self.frameno = 0
        self.keys_pressed = []
        self.mouse_pos = (0, 0)
        
        #sets the map currently active (mainly for graphics)
        self.current_map = None
        
    def next_frame(self):
    
        #calculate dt and increase framecounter
        pygame.display.flip()
        self.dt = abs(self.frame_limiter.tick(self.fps)*self.timescale)
        self.frameno += 1
        
    def set_title(self, title):
        pygame.display.set_caption(title)
        
    def set_target_fps(self, fps):
        self.fps = fps
        
    def set_map(self, map):
        self.current_map = map
        
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
        self.alphamap = pygame.Surface((16*len(self.boundmap[0]),16*len(self.boundmap)))
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
        x, y = int(tuple[0]//16), int(tuple[1]//16)
        
        if x < 0 or x > self.map_size[1]:
            x = None
            
        if y < 0 or y > self.map_size[0]:
            y = None 
            
        return (x, y)
        
    def update_zetamap(self, pos, env):
        #clear the part to be updated
        self.zetamap.fill( (0,0,0,0), (pos[0]*16, pos[1]*16, 16, 16) )
        
        #and remove the bound
        self.boundmap[pos[1]][pos[0]] = 0
        
        #get the RenderedItem at the specified position
        for i in self.rendered_items.get_items( data=[ ("x", pos[0]*16), ("y", pos[1]*16) ] ):
        
            #im sorry little one
            self.rendered_items.remove_item(i)
        
        if env != "":
        
            #if a replacement tile is specified, rejoice
            self.zetamap.blit( sprites.IDS[env], pos )
            self.boundmap[pos[1]][pos[0]] = 1
            
            #re-add specified tile to the RenderedItems list
            self.rendered_items.add_item(pygame.Rect(0,0,16,16), (pos[0]*16, pos[1]*16), data={'id':env,'x':pos[0]*16,'y':pos[1]*16}, name=env, type="zetatile")
            
        #re-make the alphamap with the updated zetamap
        self.process_alphamap()
        
#see RenderedItems
class RenderedItem:
    def __init__(self, rect, pos, data, name, type):
        self.rect = rect
        self.base_rect = rect
        self.pos = pos
        self.data = data
        self.name = name
        self.type = type
        
        #offset is used in get_drawnpos literally only for getting the right position for mouse click detection on tiles
        self.offset = (0,0)
    
    def get_screen_pos(self):
    
        #actual position on the unscaled canvas! vewwy impowtant owo :3
        return tuple_add(self.get_pos(), self.offset)
        
    def get_pos(self):
        return self.pos
        
    def get_center(self):
        return (self.pos[0] + 8, self.pos[1] + 8)
        
    def get_rect(self):
        return self.rect
        
#RenderedItems stores the list of graphical objects rendered, and gives them meaning (data)
#Exempli Gratia: player inventory uses a RenderedItems class to know what label that was drawn corresponds to what item_db class.
#also supports type/data filtering
class RenderedItems:
    def __init__(self):
        self.raw_list = []
        
    def add_item(self, rect, pos, data={}, name="", type="NoType"):
        if rect != None:
            self.raw_list.append( RenderedItem(rect, pos, data, name, type) )
        
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
        print(rect, mouse, drawn_pos, rect.left, rect.right, rect.bottom, rect.top)
    
        #mama mia, look at all this spaghetti!
        #pretty sure these checks aren't even 100% accurate but we'll see
        return mouse[0] >= rect.left+drawn_pos[0] and mouse[0] <= rect.right+drawn_pos[0] and mouse[1] >= rect.top+drawn_pos[1] and mouse[1] <= rect.bottom+drawn_pos[1]
        
    def get_items_clicked(self, mouse_pos, type="", data=[]):
    
        #returns list of RenderedItem classes where mouse_pos is in the get_drawnpos() rect, meaning the mouse cursor is on the RenderedItem.
        return [i for i in self.get_items(type, data) if self.in_rect(i.get_rect(), mouse_pos)]
        
    def modify_pos(self, offset, scale):
        #applies a linear transformation to RenderedItem offset
        for i in self.get_items():
            i.offset = (offset[0]*scale, offset[1]*scale)
            i.rect = pygame.Rect(i.get_screen_pos()[0], i.get_screen_pos()[1], i.base_rect.right, i.base_rect.bottom)
    
    def reset(self):
        self.raw_list = []