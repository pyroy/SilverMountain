import pygame, math
import essentials.classes as classes
import essentials.font as font
import essentials.map_core as map_core
from modules.MODULE import module_master

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::MapWarps"
        
    def setup(self, game_main, MODULES):
        self.pc = MODULES.get_module("Essential::Player").player_character
        self.sc = MODULES.get_module("Essential::Scaler")
    
    def make_graphics(self, game_main, MODULES, visual_core):
        for item in game_main.current_map.rendered_items.get_items(data=[("id", "warp")]):
            s_pos = item.get_screen_pos()
            destination = item.data["destination"]
            
            if self.pc.within_distance(item.get_center(), 30):
                font.render_to(game_main.canvas, self.sc.scale(s_pos, postoffset=(10,-10)), item.data["desc"] )
                
            if self.pc.within_distance(item.get_center(), 5):
                game_main.set_map( map_core.new_load_map(destination) )
                self.pc.set_map(game_main.current_map)
                self.pc.set_pos(item.data["warp_x"], item.data["warp_y"])