import sprites
import copy

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
item_pick = Item("item_pick")
item_pick.weight = 10
item_pick.value = 35
item_pick.stacks = False
item_pick.equippable = True
item_pick.name = "Rusty Old Pickaxe"
item_pick.type = "pickaxe"
item_pick.set_sprite("test_pick")

#Iron Pickaxe
iron_pick = Item("iron_pick")
iron_pick.weight = 12
iron_pick.value = 65
iron_pick.stacks = False
iron_pick.equippable = True
iron_pick.name = "Iron Pickaxe"
iron_pick.type = "pickaxe"
iron_pick.set_sprite("test_pick")

#Iron Ore
iron_ore = Item("iron_ore")
iron_ore.weight = 1
iron_ore.value = 3
iron_ore.stacks = True
iron_ore.name = "Iron Ore"
iron_ore.type = "ore"
iron_ore.set_sprite("test_pick")