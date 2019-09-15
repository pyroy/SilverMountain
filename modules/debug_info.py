import pygame, font

#module_head gets all game info
class module_head:
    def __init__(self):
        self.module_name = "Debug info mod"
        self.show_info = False
        
    def handle_keydown(self, event):
        if event.key == pygame.K_d:
            self.show_info = not self.show_info
            
    def handle_keyup(self, event): pass
    def welcome(self): pass
    
    def make_graphics(self, game_main, player_character, MODULES):
        if self.show_info:
            font.render_to(game_main.canvas, (0, game_main.screen_size[1]-10), "fps: "+str(int(game_main.frame_limiter.get_fps())))
            font.render_to(game_main.canvas, (0, game_main.screen_size[1]-20), "timescale: "+str(game_main.timescale))
            
    def run_frame(self, game_main, player_character, MODULES): pass