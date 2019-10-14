import essentials.sprites as sprites
import copy, os, json

class Database:
    def __init__(self):
        self.lookup = {}
        
idb = Database()
lookup = idb.lookup

class Item:
    def __init__(self, id):
        self.id = id
        self.equipped = False
        self.amount = 1
        self.data = {}
        
    def get_display_name(self):
        if self.amount > 1:
            return self.get_attribute("name") + " (" + str(self.amount) + ")"
        else:
            return self.get_attribute("name")
        
    def load_data(self, data):
        self.data = data
        
    def get_attribute(self, attr):
        return self.data[attr]
        
    def set_attribute(self, attr, val):
        self.data[attr] = val
        
    def new(self, amount=1):
        c = copy.deepcopy(self)
        c.amount = amount
        return c
            
#all this shit needs to be put into a json file tbh
            
for file_name in os.listdir(os.getcwd()+"/items"):
    if ".json" in file_name:
        item_name = file_name[:-5]
        with open("items/{}.json".format(item_name)) as json_file:
            idb.lookup[item_name] = Item(item_name)
            idb.lookup[item_name].load_data(json.load(json_file))