import pygame

#module_head gets all game info
class module_head:
    def __init__(self):
        self.module_name = "Inventory"
        self.requests = []
        
    def handle_keydown(self, event):
        if event.key == pygame.K_i:
            print("handled!")