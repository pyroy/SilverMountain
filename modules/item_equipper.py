import pygame
import essentials.font as font
from essentials.item_db import idb
from modules.MODULE import module_master

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
        
        player_character.inventory = Itemcontainer()
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
            if item.equipped:
                if item.type in player_character.equipped:
                    player_character.equipped[item.type].append(item)
                else: player_character.equipped[item.type] = [item]
        
        if self.mouse_clicked:
            for i in MODULES.get_module("Essential::Inventory").rendered_items.get_items_clicked(self.mouse_pos):
                item = player_character.inventory.items[ i.data["index"] ]
                player_character.inventory.equip(item)