import pygame
import essentials.font as font
import essentials.classes as classes
from modules.MODULE import module_master

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::Dialog"
        
        # Morrowind style dialog system
        
    def setup(self, game_main, MODULES):
        self.scale_mode = "fit"
        self.status = "hide"
        self.current_topic = None
        self.contents = {}
        self.dialog_history = []
        self.pc = MODULES.get_module("Essential::Player").player_character
        self.rendered_items = classes.RenderedItems()
        
    def start_new_frame(self):
        self.mouse_clicked = False
        
    def handle_mouseclick(self, event):
        if event.button == 1:
            self.mouse_clicked = True
        
    def handle_keydown(self, event):
        if event.key == pygame.K_m:
            if self.status == "hide":
                dlog = {"greeting": "Good day, miner.",
                        "background": "Ah, I'm just a miner like everyone else. I work at Plaaniker Mine, great place.",
                        "latest rumors": "Have you heard about the Faskyggr Mine? They're having major trouble trying to get rid of the Firefang Spiders held up inside the mine. I think they cna use someone like you.",
                        "Faskyggr Mine": "Yes. Apparently the place has been infested with Firefang Spiders. They've lost a few miners trying to kill them. I've heard they've put up a 500 Gold reward for those who can exterminate the spiders."}
            
                self.activate(dlog)
            else:
                self.exit()
            
    def exit(self):
        self.status = "hide"
        self.pc.allow_movement = True
        
    def activate(self, contents):
        self.contents = contents
        self.status = "show"
        self.current_topic = "greeting"
        self.dialog_history = []
        
    def run_frame(self, game_main, MODULES):
        if self.mouse_clicked:
            label_clicked = self.rendered_items.get_items_clicked(game_main.mouse_pos)
            if label_clicked != []:
                new_topic = list(self.contents.keys())[ label_clicked[0].data["index"] ]
                self.switch_topic(new_topic)
                
    def switch_topic(self, new_topic):
        self.dialog_history.append( self.contents[self.current_topic] )
        self.current_topic = new_topic
    
    def make_graphics(self, game_main, MODULES, visual_core):
        self.rendered_items.reset()
        
        if self.status == "show":
            self.pc.allow_movement = False
            text_box = pygame.Surface((game_main.screen_size[0]-100, 100), pygame.SRCALPHA)
            topic_box = pygame.Surface((100, game_main.screen_size[1]-300), pygame.SRCALPHA)
            
            text_box.fill((30,30,30,160))
            topic_box.fill((30,30,30,160))
            
            font.render_to(text_box, (10, 10), self.contents[self.current_topic], scale=2)
            for i in range(len(self.contents)):
                text_rect = font.render_to(topic_box, (10, 10+20*i), list(self.contents.keys())[i])
                text_rect.move_ip(game_main.screen_size[0]-150, 100)
                self.rendered_items.add_item(text_rect, (game_main.screen_size[0]-150+10, 100+10+20*i), data={'index':i}, name="topic_label", type="topic_label")
                
            relevant_history = self.dialog_history[-5:][::-1]
            for i in range(len(relevant_history)):
                tmp_s = pygame.Surface(font.font.size(relevant_history[i]))
                tmp_s.fill((255,0,255))
                font.render_to(tmp_s, (0,0), relevant_history[i], color=(255,255,255,128))
                tmp_s.convert_alpha()
                tmp_s.set_colorkey((255,0,255))
                tmp_s.set_alpha(255-50*i)
                game_main.canvas.blit( tmp_s, (60, game_main.screen_size[1]-150-30*i) )
                
            game_main.canvas.blit(text_box, (50, game_main.screen_size[1]-120))
            game_main.canvas.blit(topic_box, (game_main.screen_size[0]-150, 100))