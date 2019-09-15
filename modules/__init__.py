#This file loads all modules of the game.
#every module gets access to game variables and 
#can alter game states and game rendering

import modules.inventory

all_modules = [
    inventory.module_head()
    ]
    
print("----------\nModLoader v1\n----------\nModules loaded:\n")
[print("- " + m.module_name) for m in all_modules]