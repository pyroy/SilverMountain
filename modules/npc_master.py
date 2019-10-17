import pygame, json
import essentials.classes as classes
import essentials.sprites as sprites
from modules.MODULE import module_master

def tuple_add(tup1, tup2):
    return [tup1[i] + tup2[i] for i in range(len(tup1))]

def load_all_npcs():
    return {"npc1": {"name":"henk", "pos": (32,32)}}

class module_head(module_master):
    def __init__(self):
        self.module_name = "Essential::NPC-master"
        
    def setup(self, game_main, MODULES):
        self.pc = MODULES.get_module("Essential::Player").player_character
        self.npcs = load_all_npcs()
    
    def make_scaled_graphics(self, game_main, MODULES, visual_core, canvas_unscaled):
        for npc in self.npcs.values():
            dpos = (npc["pos"][0] - self.pc.get_x() + visual_core.CAMERA_OFFSET[0], npc["pos"][1] - self.pc.get_y() + visual_core.CAMERA_OFFSET[1])
            canvas_unscaled.blit( sprites.IDS["player_right"], dpos)