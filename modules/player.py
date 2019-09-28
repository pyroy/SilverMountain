import pygame
import essentials.classes as classes
from modules.MODULE import module_master

class module_head(module_master):
    def __init__(self):
        self.module_name = "Essential::Player"
        self.player_character = None
        
    def setup(self, game_main, MODULES):
    
        #see classes.py for details. this class basically stores player position & inventory and handles player movement.
        self.player_character = classes.Player()

        #set map for bound checks
        self.player_character.set_map(game_main.current_map)
    
    def run_frame(self, game_main, MODULES):
        self.player_character.feed_info(game_main.dt, game_main.keys_pressed)