import pygame
import sprites
import item_db

def in_rect(rect, mouse, offset=(0,0)):
    return mouse[0] >= rect.left+offset[0] and mouse[0] <= rect.right+offset[0] and mouse[1] >= offset[1] and mouse[1] <= rect.bottom+offset[1]

class Itemcontainer:
    def __init__(self, items=[]):
        self.items = items
        self.equiplimits = {}
        
    def add_item(self, item):
        if item.stacks:
            for i in self.items:
                if i.id == item.id:
                    i.amount += 1
                    return
            self.items.append(item)
        else:
            self.items.append(item)
            
    def get_etypecount(self, type):
        c = 0
        for item in self.items:
            if item.type == type and item.equipped:
                c += 1
        return c
        
    def equip(self, item):
        if item.equipped:
            item.equipped = False
        else:
            if item.type in self.equiplimits:
                if self.get_etypecount(item.type) < self.equiplimits[item.type]:
                    item.equipped = True
                else:
                    for i in self.items:
                        if i.type == item.type and self.get_etypecount(item.type) >= self.equiplimits[item.type]:
                            i.equipped = False
                    item.equipped = True
            else:
                item.equipped = True

class module_head:
    def __init__(self):
        self.module_name = "[Essential] Item Equipper"
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
        
    def setup(self, game_main, player_character, MODULES):
        player_character.inventory = Itemcontainer()
        player_character.inventory.add_item(item_db.item_pick.new())
        player_character.inventory.add_item(item_db.item_pick.new())
        player_character.inventory.add_item(item_db.item_pick.new())
        player_character.inventory.add_item(item_db.iron_pick.new())
        player_character.inventory.add_item(item_db.iron_ore.new(34))
        player_character.inventory.equiplimits = {"pickaxe": 1}
        player_character.equipped = []
    
    def reset_mousedown(self):
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
      
    def handle_mousedown(self, event):
        if event.button == 1:
            self.mouse_pos = event.pos
            self.mouse_clicked = True
    
    def handle_keydown(self, event): pass
    def handle_keyup(self, event): pass
    def welcome(self): pass
    def make_graphics(self, game_main, player_character, MODULES): pass
    def run_frame(self, game_main, player_character, MODULES):
        player_character.equipped = [item for item in player_character.inventory.items if item.equipped]
        
        for t in MODULES[0].rendered_items: #TODO: Easier module lookup for a dynamic loading order
            if in_rect(t[1], self.mouse_pos, offset=(10, 10+20*t[0])) and self.mouse_clicked:
                item = player_character.inventory.items[t[0]]
                player_character.inventory.equip(item)