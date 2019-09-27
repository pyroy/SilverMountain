import pygame
import sprites
import item_db

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
        self.module_name = "[E] Item Equipper"
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
        
    def info(self):
        print("This mod handles all inventory actions.")
        
    def get_dependencies(self):
        return ["[E] Inventory"]
        
    def setup(self, game_main, player_character, MODULES):
        player_character.inventory = Itemcontainer()
        player_character.inventory.add_item(item_db.item_pick.new())
        player_character.inventory.add_item(item_db.item_pick.new())
        player_character.inventory.add_item(item_db.item_pick.new())
        player_character.inventory.add_item(item_db.iron_pick.new())
        player_character.inventory.add_item(item_db.iron_ore.new(33))
        player_character.inventory.add_item(item_db.iron_ore.new())
        player_character.inventory.equiplimits = {"pickaxe": 1}
        player_character.equipped = {}
    
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
    def make_scaled_graphics(self, game_main, player_character, MODULES, visual_core, canvas_unscaled): pass
    def make_graphics(self, game_main, player_character, MODULES, visual_core): pass
    def run_frame(self, game_main, player_character, MODULES):
        player_character.equipped = {}
        for item in player_character.inventory.items:
            if item.equipped:
                if item.type in player_character.equipped:
                    player_character.equipped[item.type].append(item)
                else: player_character.equipped[item.type] = [item]
        
        for i in MODULES.get_module("[E] Inventory").rendered_items.get_items_clicked(self.mouse_pos):
            item = player_character.inventory.items[ i.data["index"] ]
            player_character.inventory.equip(item)