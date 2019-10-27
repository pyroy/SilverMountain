import pygame, time

class VisualCore:
    def __init__(self, dsize, zsize):
        self.items_to_render = []
        self.direct_layers = {}
        self.zoomed_layers = {}
        self.dsize = dsize
        self.zsize = zsize
        self.rendered_layers = {}
        
    def dump_layer(self, layer, mode="direct"):
        if mode == "zoomed" and layer in self.zoomed_layers:
            self.zoomed_layers[layer] = []
        elif layer in self.direct_layers: self.direct_layers[layer] = []
        
    def add_items_to_layer(self, item, layer, mode="direct"):
        if mode == "zoomed":
        
            if layer in self.zoomed_layers:
            
                self.zoomed_layers[layer] += item
                
            else: 
            
                self.zoomed_layers[layer] = item
        else:
        
            if layer in self.direct_layers:
            
                self.direct_layers[layer] += item
                
            else: 
            
                self.direct_layers[layer] = item
        
    def render_layer(self, layer, mode="direct"):
        surf = pygame.Surface(self.zsize, pygame.SRCALPHA, 32)
        
        for item in self.zoomed_layers[layer]:
            surf.blit(item[0], item[1])
            
        if mode == "zoomed":
            self.rendered_layers[layer] = pygame.transform.scale(surf, self.dsize)
        else:
            self.rendered_layers[layer] = surf
        
    def render_all(self):
    
        surf = pygame.Surface(self.dsize)
        
        for layer in sorted(list(self.rendered_layers.keys())):
            surf.blit( self.rendered_layers[layer], (0,0) )
            
        return surf