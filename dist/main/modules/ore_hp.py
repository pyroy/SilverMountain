import pygame
import essentials.classes as classes
import essentials.font as font
from modules.MODULE import module_master

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::OreHP"
        
    def setup(self, game_main, MODULES):
        self.scaler = MODULES.get_module("Essential::Scaler")
    
    def make_graphics(self, game_main, MODULES, visual_core):
        for item in game_main.current_map.rendered_items.get_items():
            if "mined" in item.data and item.data["mined"] < item.data["minetime"]:
                s_pos = item.get_screen_pos()
                fll = self.scaler.scale(16*item.data["mined"]/item.data["minetime"], mode="scale x")
                pygame.draw.rect(game_main.canvas, (0, 255, 0), (self.scaler.scale(s_pos), (fll,2)))
                if fll < self.scaler.scale(16, mode = "scale x"):
                    pygame.draw.rect(game_main.canvas, (255, 0, 0), (self.scaler.scale(s_pos, postoffset=(fll,0)), (16*self.scaler.SCALE_X - fll,4)))