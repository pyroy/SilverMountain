import pygame
import essentials.font as font
import essentials.classes as classes
import essentials.sprites as sprites
from essentials.item_db import idb
from modules.MODULE import module_master

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::SellMenu"
        
        # Morrowind style bartering system
        
    def setup(self, game_main, MODULES):
        self.scale_mode = "fit"
        self.status = "hide"
        self.merchant_inv = None
        self.final_price_delta = 0
        self.pc = MODULES.get_module("Essential::Player").player_character
        self.dummy_inv = classes.Itemcontainer().cpy()
        self.dummy_inv.add_item(idb.lookup["ironore"].new(200))
        self.dummy_inv.add_item(idb.lookup["rubyshards"].new(200))
        
        self.l_i_spr = []
        self.r_i_spr = []
        self.main_gui = None
        
        self.rendered_items = classes.RenderedItems()
        
    def start_new_frame(self):
        self.mouse_clicked = False
        
    def handle_mouseclick(self, event):
        if event.button == 1:
            self.mouse_clicked = True
        
    def handle_keydown(self, event):
        if event.key == pygame.K_n:
            if self.status == "hide":
                self.activate(self.pc.inventory)
            else:
                self.status = "hide"
                self.pc.allow_movement = True
            
    def exit(self):
        self.status = "hide"
        
    def activate(self, merchant_inv):
        self.p_inv = self.pc.inventory.cpy()
        self.merchant_inv = self.dummy_inv.cpy()
        self.status = "show"
        self.final_price_delta = 0
        
        self.l_i_spr = [pygame.transform.scale(sprites.IDS[self.p_inv.items[i].get_attribute("sprite")], (64,64)) for i in range(len(self.p_inv.items))]
        self.r_i_spr = [pygame.transform.scale(sprites.IDS[self.merchant_inv.items[i].get_attribute("sprite")], (64,64)) for i in range(len(self.merchant_inv.items))]
        self.redraw_invs()
        
    def run_frame(self, game_main, MODULES):
        if self.mouse_clicked:
            pass;
    
    def redraw_invs(self):
        self.main_gui = pygame.Surface((800, 320), pygame.SRCALPHA)
    
        inventory_showcase = pygame.Surface((320, 320), pygame.SRCALPHA)
        inventory_showcase.fill((30,30,30,160))
        
        merchant_inv_showcase = pygame.Surface((320, 320), pygame.SRCALPHA)
        merchant_inv_showcase.fill((30,30,30,160))
        
        all_items = self.p_inv.items
        for i in range(len(all_items)):
            inventory_showcase.blit(self.l_i_spr[i], (64*(i%5), 64*(i//5)))
            a = str(all_items[i].amount)
            if a != "0" and a != "1":
                font.render_to(inventory_showcase, (64*(i%5)+64-font.get_size(a, scale=2)[0], 64*(i//5)+64-20), a, scale=2)
            self.rendered_items.add_item(pygame.Rect(64*(i%5), 64*(i//5), 64, 64), (64*(i%5), 64*(i//5)), data={'index':i}, name="item_icon", type="item_icon")
            
        all_items = self.merchant_inv.items
        for i in range(len(all_items)):
            merchant_inv_showcase.blit(self.r_i_spr[i], (64*(i%5), 64*(i//5)))
            a = str(all_items[i].amount)
            if a != "0" and a != "1":
                font.render_to(merchant_inv_showcase, (64*(i%5)+64-font.get_size(a, scale=2)[0], 64*(i//5)+64-20), a, scale=2)
            self.rendered_items.add_item(pygame.Rect(64*(i%5), 64*(i//5), 64, 64), (64*(i%5), 64*(i//5)), data={'index':i}, name="item_icon", type="item_icon")
            
        l_inv = inventory_showcase
        r_inv = merchant_inv_showcase
        
        s_arr = pygame.transform.scale(sprites.IDS["sell_arrows"], (92, 108))
            
        self.main_gui.blit(l_inv, (0, 0))
        self.main_gui.blit(s_arr, (320+34, 106))
        self.main_gui.blit(r_inv, (800-320, 0))
    
    def make_graphics(self, game_main, MODULES, visual_core):
        self.rendered_items.reset()
        
        if self.status == "show":
            self.pc.allow_movement = False
            game_main.canvas.blit(self.main_gui, (int((game_main.screen_size[0]-800)/2), int((game_main.screen_size[1]-320)/2)))