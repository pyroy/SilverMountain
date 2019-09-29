import pygame
import essentials.classes as classes
import essentials.font as font
from modules.MODULE import module_master

SCALE = 720/320
def scale_up(pos):
    return (pos[0]*SCALE, pos[1]*SCALE)

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::OreHP"
    
    def make_graphics(self, game_main, MODULES, visual_core):
        for item in game_main.current_map.rendered_items.get_items():
            if "mined" in item.data and item.data["mined"] < item.data["minetime"]:
                dpos = item.get_drawnpos()
                fll = 32*SCALE*item.data["mined"]/item.data["minetime"]
                pygame.draw.rect(game_main.canvas, (0, 255, 0), ((dpos[0]*SCALE, dpos[1]*SCALE), (fll,4)))
                if fll < 72.0:
                    pygame.draw.rect(game_main.canvas, (255, 0, 0), ((dpos[0]*SCALE + fll, dpos[1]*SCALE), (32*SCALE - fll,4)))