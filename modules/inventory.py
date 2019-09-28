import pygame
import font
import sprites
import classes
from modules.MODULE import module_master

#Inventory module allows usage of items
#
#pretty self explanatory
#
#please do not ask why this is a module

class module_head(module_master):
    def __init__(self):
        self.module_name = "Essential::Inventory"

        self.invreach = 0
        self.open = False
        self.finished_animating = True
        
        self.rendered_items = classes.RenderedItems()
        
    def info(self):
        print("This mod handles showing the player's inventory.\nPress I to open the inventory.")
        
    def get_dependencies(self):
        return ["Essential::ItemEquipper"]
        
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
            self.anim_frames = min(10, game_main.dt / 9 + self.anim_frames)
            self.invreach = int(self.anim_frames * 25)
            if self.anim_frames == 10: self.finished_animating = True
                
        elif not self.open and not self.finished_animating:
            self.anim_frames  = min(10, game_main.dt / 9 + self.anim_frames)
            self.invreach = int(250 - self.anim_frames * 25)
            if self.anim_frames == 10: self.finished_animating = True
            
    def make_graphics(self, game_main, player_character, MODULES, visual_core):
    
        self.rendered_items.reset()
        
        s = pygame.Surface((self.invreach, game_main.screen_size[1]), pygame.SRCALPHA)
        s.fill((30,30,30,128))
        
        for i in range(len(player_character.inventory.items)):
            text_rect = font.render_to(s, (10, 10+20*i), player_character.inventory.items[i].get_display_name())
            
            self.rendered_items.add_item(text_rect, (10, 10+20*i), data={'index':i}, name="item_label", type="item_label")
                
            if player_character.inventory.items[i].equipped:
                pygame.draw.rect(s, (255,255,255), (text_rect.right + 15, 10+20*i, 6, 6))
                
        game_main.canvas.blit(s, (0,0))