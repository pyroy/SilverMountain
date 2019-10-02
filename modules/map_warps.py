import pygame, math
import essentials.classes as classes
import essentials.font as font
from modules.MODULE import module_master

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::MapWarps"
        
    def setup(self, game_main, MODULES):
        self.pc = MODULES.get_module("Essential::Player").player_character
        self.sc = MODULES.get_module("Essential::Scaler")
    
    def make_graphics(self, game_main, MODULES, visual_core):
        for item in game_main.current_map.rendered_items.get_items(type="warp"):
            s_pos = item.get_screen_pos()
            destination = item.data["destination"]
            pygame.draw.rect(game_main.canvas, (120, 0, 255), (self.sc.scale(s_pos, preoffset=(8,8)), self.sc.scale( (16,16) )))
            if self.pc.within_distance(item.get_pos(), 40, posoffset = (16,16)):
                font.render_to(game_main.canvas, self.sc.scale(s_pos, preoffset = (8,8)), destination )