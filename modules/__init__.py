#This file loads all modules of the game.
#every module gets access to game variables and 
#can alter game states and game rendering


module_list = [
    "inventory",
    "item_equipper",
    "mining"
    #"timescale_mod",
    #"module_template",
    #"debug_info"
    ]
    
exec("".join(["import modules.{}\n".format(m) for m in module_list]))

class Modules:
    def __init__(self):
        self.all_modules = []
        
    def is_loaded(self, module_name):
        for i in self.all_modules:
            if i.module_name == module_name:
                return True
                
    def get_module(self, module_name):
        for i in self.all_modules:
            if i.module_name == module_name:
                return i
        return None
        
    def get_all_modules(self):
        return self.all_modules
        
MODULES = Modules()

[exec("MODULES.all_modules.append({}.module_head())".format(m)) for m in module_list]
    
print("--------------\n ModLoader v1\n--------------\nModules loaded:\n")
[print("- " + m.module_name) for m in MODULES.all_modules]
print("\n-------------------------\n Silver Mountain Console \n-------------------------\nPress C in-game to execute a command.")
            
markforshutdown = []
for m in MODULES.all_modules:
    for dep in m.get_dependencies():
        if not MODULES.is_loaded(dep):
            markforshutdown.append(m)
            
for m in markforshutdown:
    MODULES.all_modules.remove(m)
    print("\n[Console/W]>> {} has been disabled due to missing dependencies".format(m.module_name))