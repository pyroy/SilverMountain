import pygame, math
import sprites
import item_db

def tuple_sub(tup1, tup2):
    return [tup1[i] - tup2[i] for i in range(len(tup1))]
    
def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]

class module_head:
    def __init__(self):
        self.module_name = "[Essential] Mining"
        self.pick_rotation = 0
        self.anim_frames = 0
        self.anim_done = True
        
    def setup(self, game_main, player_character, MODULES): pass
    def reset_mousedown(self): pass
    
    def handle_mousedown(self, event):
        self.anim_done = False
        self.anim_frames = 10
        
    def handle_keydown(self, event): pass
    def handle_keyup(self, event): pass
    def welcome(self): pass
    def make_graphics(self, game_main, player_character, MODULES, visual_core): pass
    
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