import pygame
import essentials.font as font
from modules.MODULE import module_master

class module_head(module_master):
    def __init__(self):
        self.module_name = "Extra::DebugInfoMod"
        self.show_info = False
        
    def handle_keydown(self, event):
        if event.key == pygame.K_d:
            self.show_info = not self.show_info
    
    def make_graphics(self, game_main, MODULES, visual_core):
        if self.show_info:
            font.render_to(game_main.canvas, (0, game_main.screen_size[1]-10), "fps: "+str(int(game_main.frame_limiter.get_fps())))
            font.render_to(game_main.canvas, (0, game_main.screen_size[1]-20), "timescale: "+str(game_main.timescale))