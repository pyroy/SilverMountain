import pygame

#module_head gets all game info
class module_head:
    def __init__(self):
        self.module_name = "Timescale Mod v1"
        self.timescale = 1
        
    def welcome(self):
        print("Timescale mod: Press T to change timescale!")
        
    def handle_keydown(self, event):
        if event.key == pygame.K_t:
            self.timescale = float(input("set timescale to >>"))
            
    def handle_keyup(self, event): pass
    def make_graphics(self, game_main, player_character, MODULES): pass
    def run_frame(self, game_main, player_character, MODULES):
        game_main.timescale = self.timescale