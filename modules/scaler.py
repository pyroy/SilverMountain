import pygame
from modules.MODULE import module_master

def distance(a, b, c, d):
    return math.sqrt( (a-b)**2 + (c-d)**2 )

class module_head(module_master):
    def __init__(self):
        self.module_name = "Essential::Scaler"
        
    def setup(self, game_main, MODULES):
    
        self.SCALE_X = game_main.screen_size[0] / game_main.unscaled_canvas_size[0]
        self.DESCALE_X = game_main.unscaled_canvas_size[0] / game_main.screen_size[0]
        
        self.SCALE_Y = game_main.screen_size[1] / game_main.unscaled_canvas_size[1]
        self.DESCALE_Y = game_main.unscaled_canvas_size[1] / game_main.screen_size[1]
    
    def scale(self, args, mode="scale tuple", preoffset=(0,0), postoffset=(0,0)):
        if "tuple" not in mode:
            preoffset = 0
            postoffset = 0
    
        if mode == "scale tuple":
            return ( (args[0]+preoffset[0]) * self.SCALE_X + postoffset[0], (args[1] + preoffset[0]) * self.SCALE_Y + postoffset[1])
            
        elif mode == "scale x":
            return (args + preoffset) * self.SCALE_X + postoffset
            
        elif mode == "scale y":
            return (args + preoffset) * self.SCALE_Y + postoffset
            
        elif mode == "descale tuple":
            return ((args[0]+preoffset[0]) * self.DESCALE_X + postoffset[0], (args[1] + preoffset[0]) * self.DESCALE_Y + postoffset[1])
            
        elif mode == "descale x":
            return (args + preoffset) * self.DESCALE_X + postoffset
            
        elif mode == "descale y":
            return (args + preoffset) * self.DESCALE_Y + postoffset
            
    def scale_x(self, val):
        return val*self.SCALE_X
        
    def scale_y(self, val):
        return val*self.SCALE_Y