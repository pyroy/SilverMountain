import essentials.sprites as sprites
import copy

class Database:
    def __init__(self):
        self.lookup = {}
        
idb = Database()

class Item:
    def __init__(self, id):
        self.id = id
        self.sprite = sprites.IDS["test_pick"]
        self.weight = 0
        self.value = 0
        self.stacks = True
        self.equipped = False
        self.equippable = False
        self.type = "Misc."
        self.amount = 1
        self.name = self.id #for now
        
    def get_display_name(self):
        if self.amount > 1:
            return self.name + " (" + str(self.amount) + ")"
        else:
            return self.name
            
    def set_sprite(self, spritename):
        self.sprite = sprites.IDS[spritename]
        
    def new(self, amount=1):
        c = copy.copy(self)
        c.amount = amount
        return c
            
#Rusty Pickaxe
idb.lookup["oldpick"] = Item("item_pick")
idb.lookup["oldpick"].weight = 10
idb.lookup["oldpick"].value = 35
idb.lookup["oldpick"].stacks = False
idb.lookup["oldpick"].equippable = True
idb.lookup["oldpick"].name = "Rusty Old Pickaxe"
idb.lookup["oldpick"].type = "pickaxe"
idb.lookup["oldpick"].set_sprite("test_pick")

#Iron Pickaxe
idb.lookup["ironpick"] = Item("iron_pick")
idb.lookup["ironpick"].weight = 12
idb.lookup["ironpick"].value = 65
idb.lookup["ironpick"].stacks = False
idb.lookup["ironpick"].equippable = True
idb.lookup["ironpick"].name = "Iron Pickaxe"
idb.lookup["ironpick"].type = "pickaxe"
idb.lookup["ironpick"].set_sprite("test_pick")

#Iron Ore
idb.lookup["ironore"] = Item("iron_ore")
idb.lookup["ironore"].weight = 1
idb.lookup["ironore"].value = 3
idb.lookup["ironore"].stacks = True
idb.lookup["ironore"].name = "Iron Ore"
idb.lookup["ironore"].type = "ore"
idb.lookup["ironore"].set_sprite("test_pick")