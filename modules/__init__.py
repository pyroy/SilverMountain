#This file loads all modules of the game.
#every module gets access to game variables and 
#can alter game states and game rendering


module_list = [
    "inventory",
    "item_equipper"
    #"timescale_mod",
    #"module_template",
    #"debug_info"
    ]
    
exec("".join(["import modules.{}\n".format(m) for m in module_list]))

all_modules = []
[exec("all_modules.append({}.module_head())".format(m)) for m in module_list]
    
print("--------------\n ModLoader v1\n--------------\nModules loaded:\n")
[print("- " + m.module_name) for m in all_modules]
print("\n-------------------------\n Silver Mountain Console \n-------------------------")

for m in all_modules:
    try: m.welcome()
    except: pass