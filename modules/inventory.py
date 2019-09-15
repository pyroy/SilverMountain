import pygame
import font

#Inventory module allows usage of items
#
#pretty self explanatory
#
#please do not ask why this is a module

class module_head:
    def __init__(self):
        self.module_name = "[Essential] Inventory"
        self.requests = []
        self.invreach = 0
        self.open = False
        self.finished_animating = True
        
    def handle_keydown(self, event):
        if event.key == pygame.K_i:
            if self.open and self.finished_animating:
               self.open, self.finished_animating = False, False
               self.anim_frames = 0
               
            elif not self.open and self.finished_animating:
               self.open, self.finished_animating = True, False
               self.anim_frames = 0
            
    def run_frame(self, game_main, player_character, MODULES):
        if self.open and not self.finished_animating:
            self.anim_frames += 1
            self.invreach = int(self.anim_frames * 25)
            if self.anim_frames == 10:
                self.finished_animating = True
                
        elif not self.open and not self.finished_animating:
            self.anim_frames += 1
            self.invreach = int(250 - self.anim_frames * 25)
            if self.anim_frames == 10:
                self.finished_animating = True
            
    def make_graphics(self, game_main, player_character, MODULES):
        s = pygame.Surface((self.invreach, game_main.screen_size[1]), pygame.SRCALPHA)
        s.fill((30,30,30,128))
        for item in range(len(player_character.inventory.items)):
            font.render_to(s, (10, 10+20*item), player_character.inventory.items[item].id)
        game_main.canvas.blit(s, (0,0))