class module_master:
    def __init__(self): pass;  
    def info(self): pass;
    def get_dependencies(self):
        return []
 
    def setup(self, game_main, player_character, MODULES): pass;  
    def start_new_frame(self): pass;
    def handle_mousedown(self, event): pass;
    def handle_mouseup(self, event): pass;
    def handle_keydown(self, event): pass
    def handle_keyup(self, event): pass;
    def handle_mouseclick(self, event): pass;
    def welcome(self): pass;
    def make_scaled_graphics(self, game_main, player_character, MODULES, visual_core, canvas_unscaled): pass;
    def make_graphics(self, game_main, player_character, MODULES, visual_core): pass;
    def run_frame(self, game_main, player_character, MODULES): pass;