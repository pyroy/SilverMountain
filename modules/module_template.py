import pygame

#module_head gets all game info
class module_head:
    def __init__(self):
        self.module_name = "Module template"
        
    def handle_keydown(self, event): pass
    def handle_keyup(self, event): pass
    def welcome(self): pass
    def make_graphics(self, game_main, player_character, MODULES): pass
    def run_frame(self, game_main, player_character, MODULES): pass