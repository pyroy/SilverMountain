import pygame, math
import sprites
import item_db
from modules.MODULE import module_master

def tuple_sub(tup1, tup2):
    return [tup1[i] - tup2[i] for i in range(len(tup1))]
    
def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::Mining"
        self.pick_rotation = 0
        self.anim_frames = 0
        self.anim_done = True
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
        
    def info(self):
        print("This module handles mining.\nEquip any pickaxe and click on a minable tile to mine the item from the tile.")
        
    def get_dependencies(self):
        return ["Essential::ItemEquipper", "Essential::Inventory"]
        
    def start_new_frame(self):
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
      
    def handle_mouseclick(self, event):
        if event.button == 1:
            self.anim_done = False
            self.anim_frames = 10
            
            self.mouse_pos = event.pos
            self.mouse_clicked = True
    
    def make_scaled_graphics(self, game_main, player_character, MODULES, visual_core, canvas_unscaled):
        if "pickaxe" in player_character.equipped and len(player_character.equipped["pickaxe"]) > 0:
            c = player_character.equipped["pickaxe"][0].sprite.get_rect()
            p = pygame.transform.rotate(player_character.equipped["pickaxe"][0].sprite, self.pick_rotation)
            c.center = p.get_rect().center
            r_x = -math.sin(-self.pick_rotation/360*2*math.pi+0.75*math.pi)*16
            r_y = math.cos(-self.pick_rotation/360*2*math.pi+0.75*math.pi)*16
            canvas_unscaled.blit(p, tuple_add(tuple_sub(visual_core.CAMERA_OFFSET, c.topleft), (r_x-6, r_y+8))) #adjust positioning for rotation around pivot, and fix it to player location
            #So this does not yet work in FIXED camera mode but that's not fully implemented yet
            
    def run_frame(self, game_main, player_character, MODULES):
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
            clicked_env = game_main.current_map.rendered_items.get_items_clicked( (self.mouse_pos[0]*320/720, self.mouse_pos[1]*320/720), "zetatile") #you HAVE to descale the mouse, NEVER scale up the canvas!!
            for i in clicked_env:
                if "pickaxe" in player_character.equipped and len(player_character.equipped["pickaxe"]) > 0:
                    game_main.current_map.update_zetamap( (int(i.drawn_pos[0]/32), int(i.drawn_pos[1]/32)), "")
                    player_character.inventory.add_item(item_db.iron_ore.new())