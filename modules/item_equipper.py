import pygame
import essentials.font as font
import essentials.classes as classes
from essentials.item_db import idb
from modules.MODULE import module_master

class module_head(module_master):
    def __init__(self):
        self.module_name = "Essential::ItemEquipper"
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
        
    def info(self):
        print("This mod handles all inventory actions.")
        
    def get_dependencies(self):
        return ["Essential::Inventory"]
        
    def start_new_frame(self):
        self.mouse_pos = (0,0)
        self.mouse_clicked = False
        
    def setup(self, game_main, MODULES):
    
        player_character = MODULES.get_module("Essential::Player").player_character
        
        player_character.inventory = classes.Itemcontainer().cpy()
        player_character.inventory.add_item(idb.lookup["oldpick"].new())
        player_character.inventory.add_item(idb.lookup["oldpick"].new())
        player_character.inventory.add_item(idb.lookup["oldpick"].new())
        player_character.inventory.add_item(idb.lookup["ironpick"].new())
        player_character.inventory.add_item(idb.lookup["ironore"].new(33))
        player_character.inventory.add_item(idb.lookup["ironore"].new())
        player_character.inventory.equiplimits = {"pickaxe": 1}
        player_character.equipped = {}
      
    def handle_mouseclick(self, event):
        if event.button == 1:
            self.mouse_pos = event.pos
            self.mouse_clicked = True
    
    def run_frame(self, game_main, MODULES):
    
        player_character = MODULES.get_module("Essential::Player").player_character
        player_character.equipped = {}
        
        for item in player_character.inventory.items:
            i_type = item.get_attribute("type")
            if item.equipped:
                if i_type in player_character.equipped:
                    player_character.equipped[i_type].append(item)
                else: player_character.equipped[i_type] = [item]
        
        if self.mouse_clicked and MODULES.get_module("Essential::Inventory").open:
            for i in MODULES.get_module("Essential::Inventory").rendered_items.get_items_clicked(self.mouse_pos):
                item = player_character.inventory.items[ i.data["index"] ]
                player_character.inventory.equip(item)