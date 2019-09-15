#This file loads all modules of the game.
#every module gets access to game variables and 
#can alter game states and game rendering

import modules.inventory
import modules.timescale_mod
import modules.module_template

#LOAD ORDER MATTERS, KIDS
all_modules = [
    inventory.module_head(),
    timescale_mod.module_head(),
    module_template.module_head()
    ]
    
print("--------------\n ModLoader v1\n--------------\nModules loaded:\n")
[print("- " + m.module_name) for m in all_modules]
print("\n-------------------------\n Silver Mountain Console \n-------------------------")

for m in all_modules:
    try: m.welcome()
    except: pass