import pygame, math, random
import essentials.sprites as sprites
from essentials.item_db import idb
from modules.MODULE import module_master

def tuple_sub(tup1, tup2):
    return [tup1[i] - tup2[i] for i in range(len(tup1))]
    
def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]

def get_cells_around(cell, map_limit_x=100000, map_limit_y=100000):
    ret = []
    
    if cell[0] - 1 >= 0:
        ret.append( (cell[0] - 1, cell[1]) )
        
    if cell[0] + 1 <= map_limit_x:
        ret.append( (cell[0] + 1, cell[1]) )
        
    if cell[1] - 1 >= 0:
        ret.append( (cell[0], cell[1] - 1) )
        
    if cell[1] + 1 <= map_limit_y:
        ret.append( (cell[0], cell[1] + 1) )
        
    return ret
    
def distance(a, b, c, d):
    return math.sqrt( (a-b)**2 + (c-d)**2 )

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::Mining"
        self.pick_rotation = 0
        self.anim_frames = 0
        self.anim_done = True
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
        self.focus = None
        
    def info(self):
        print("This module handles mining.\nEquip any pickaxe and click on a minable tile to mine the item from the tile.")
        
    def get_dependencies(self):
        return ["Essential::ItemEquipper", "Essential::Inventory"]
        
    def setup(self, game_main, MODULES):
        self.pc = MODULES.get_module("Essential::Player").player_character
        self.pf = MODULES.get_module("Basegame::Pathfinding")
        self.sc = MODULES.get_module("Essential::Scaler")
        
    def start_new_frame(self):
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
      
    def handle_mouseclick(self, event):
        if event.button == 1:
            self.mouse_pos = event.pos
            self.mouse_clicked = True
    
    def make_scaled_graphics(self, game_main, MODULES, visual_core, canvas_unscaled):
        if "pickaxe" in self.pc.equipped and len(self.pc.equipped["pickaxe"]) > 0 and self.focus != None and self.pc.pathfinder.is_hijacking == False:
            c = self.pc.equipped["pickaxe"][0].sprite.get_rect()
            p = pygame.transform.rotate(self.pc.equipped["pickaxe"][0].sprite, self.pick_rotation)
            c.center = p.get_rect().center
            r_x = -math.sin(-self.pick_rotation/360*2*math.pi+0.75*math.pi)*8
            r_y = math.cos(-self.pick_rotation/360*2*math.pi+0.75*math.pi)*8
            canvas_unscaled.blit(p, tuple_add(tuple_sub(self.focus.get_screen_pos(), c.topleft), (r_x+1-4+14, r_y+4-8))) #adjust positioning for rotation around pivot, and fix it to player location
            #So this does not yet work in FIXED camera mode but that's not fully implemented yet
            
    def mine_block(self, game_main, block): #takes a RenderedItem
        game_main.current_map.update_zetamap( (int(block.get_pos()[0]/16), int(block.get_pos()[1]/16)), "")
        if 'drop' in block.data:
            self.pc.inventory.add_item(idb.lookup[block.data["drop"]].new())
            
    def set_focus(self, block):
        self.focus = block
            
    def run_frame(self, game_main, MODULES):
    
        if self.focus != None and "mined" in self.focus.data:
            d = distance(self.focus.data["x"], self.pc.x_position, self.focus.data["y"], self.pc.y_position)
            if d > 32:
                self.pf.goto_goal( precision=10 )

            elif self.pc.pathfinder.is_hijacking == False:
                self.anim_done = False
                if self.anim_frames == -10:
                    self.anim_frames = 10
            
                self.focus.data["mined"] -= 1
                
                if self.focus.data["mined"] == 0:
                    self.mine_block(game_main, self.focus)
                    self.set_focus(None)
                
        if self.focus != None and not ("pickaxe" in self.pc.equipped and len(self.pc.equipped["pickaxe"]) > 0):
            self.set_focus(None)
            
        if self.pc.is_moving:
            self.set_focus(None)
            self.pf.stop()
    
        if not self.anim_done:
            if self.anim_frames == -10:
                self.anim_done = True
            else:
                if self.anim_frames > 0:
                    self.pick_rotation = 45-9*2.5+50-2.5*self.anim_frames
                else:
                    self.pick_rotation = 45-9*2.5+2.5*self.anim_frames
                self.anim_frames -= 1
                
        if self.mouse_clicked:
            clicked_env = game_main.current_map.rendered_items.get_items_clicked( self.sc.scale(game_main.mouse_pos, mode = "descale tuple"), "zetatile") #you HAVE to descale the mouse, NEVER scale up the canvas!!
            for i in clicked_env:
                if "pickaxe" in self.pc.equipped and len(self.pc.equipped["pickaxe"]) > 0:
                    self.set_focus(i)
                    goals = [g for g in get_cells_around( (int(self.focus.data["x"]//16), int(self.focus.data["y"]//16)) ) if game_main.current_map.boundmap[ g[1] ][ g[0] ] == 0]
                    if goals != []:
                        goal = random.choice(goals)
                        self.pf.set_goal( goal )
                        if distance(self.focus.data["x"], self.pc.x_position, self.focus.data["y"], self.pc.y_position) > 32:
                            self.pf.goto_goal( precision=10 )
                    else: self.set_focus(None)