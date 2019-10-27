import pygame, math
import essentials.sprites as sprites
from modules.MODULE import module_master

#adds tuples or lists such that (a, b) + (c, d) = (a + b, c + d)
def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]

def distance(a, b, c, d):
    return math.sqrt( (a-b)**2 + (c-d)**2 )

class Player:
    def __init__(self):
        self.x_position = 32
        self.y_position = 32
        self.orientation = "left"
        self.mov_speed = 1.2
        
        #used for collision checks @ line 58
        self.bounding_box = [
            (3,3),
            (3,13),
            (13,3),
            (13,13)
            ]
            
        self.map = None
        self.is_moving = False
        self.scaler = None
        self.allow_movement = True
        
    #In the future when inventory gets added, players look 
    #different based on what they're wearing.
    #This function will eventually handle that.
    def get_sprite(self):
        if self.orientation == "left":
            return sprites.IDS["player_left"]
        elif self.orientation == "right":
            return sprites.IDS["player_right"]
        
    def set_map(self, map):
        self.map = map
        
    def set_scaler(self, scaler):
        self.scaler = scaler
        
    def get_pos(self):
        return (self.get_x(), self.get_y())
        
    def set_pos(self, pos, pos2ndarg=None):
        
        #works with either set_pos( (x, y) )
        #or with set_pos(x, y)
    
        if pos2ndarg == None:
            self.x_position = pos[0]
            self.y_position = pos[1]
        else:
            self.x_position = pos
            self.y_position = pos2ndarg
        
    def get_center(self):
        return (self.get_x() + 8, self.get_y() + 8)
        
    def get_x(self):
        return self.x_position
        
    def get_y(self):
        return self.y_position
        
    #returns the screen position of the four boundcheck corners
    def get_bounds(self):
        return [tuple_add(self.bounding_box[i], (self.x_position, self.y_position)) for i in range(4)]
        
    def within_distance(self, pos, threshold, posoffset=(0,0)):
        center = self.get_center()
        return distance( center[0], pos[0] + posoffset[0], center[1], pos[1] + posoffset[1] ) < threshold
        
    def move(self, dt, directions):
        if self.map == None: 
            print("[Console/W]>> Player map not set!")
            return
            
        if not self.allow_movement:
            return
    
        #just check bounds everywhere you try to move
        self.speed = self.mov_speed/17*dt
    
        if directions[0]:
            self.x_position -= self.speed
            self.orientation = "left"
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
            self.orientation = "right"
            if self.map.check_bounds(self.get_bounds()):
                self.x_position -= self.speed
        
    def feed_info(self, dt, keys):
        if self.allow_movement:
            #keys are in DDR order. do not move if relevant keys are not being pressed
            if any( [keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_RIGHT]] ):
                self.is_moving = True
                self.move(dt, [keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_RIGHT]])
            else: self.is_moving = False

class module_head(module_master):
    def __init__(self):
        self.module_name = "Essential::Player"
        self.player_character = None
        
    def setup(self, game_main, MODULES):
    
        #see classes.py for details. this class basically stores player position & inventory and handles player movement.
        self.player_character = Player()

        #set map for bound checks
        self.player_character.set_map(game_main.current_map)
        
        #set scaler (is this necessary?)
        self.player_character.set_scaler( MODULES.get_module("Essential::Scaler") )
    
    def run_frame(self, game_main, MODULES):
        self.player_character.feed_info(game_main.dt, game_main.keys_pressed)
    
    def make_graphics(self, game_main, MODULES, visual_core):
        visual_core.VC.dump_layer("1player", mode="zoomed")
        visual_core.VC.add_items_to_layer([(self.player_character.get_sprite(), self.player_character.get_pos())], "1player", mode="zoomed")
        visual_core.VC.render_layer("1player", mode = "zoomed")