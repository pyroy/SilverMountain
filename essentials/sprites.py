import pygame

#this entire thing might just be moved to item_db.py, but we'll see when more sprites are added.

#gamesprites
player_sprite = pygame.image.load("sprites/player16x16.png")
pick_sprite = pygame.image.load("sprites/pick16x16.png")

#tilesprites
tile_dirt = pygame.image.load("sprites/tile_dirt16x16.png")

#environment sprites
env_stone = pygame.image.load("sprites/stone16x16.png")
env_ore = pygame.image.load("sprites/ore16x16.png")

IDS = {
    "tile_dirt": pygame.image.load("sprites/tile_dirt16x16.png"),
    "test_pick": pygame.image.load("sprites/pick16x16.png"),
    "env_stone": pygame.image.load("sprites/stone16x16.png"),
    "env_ore": pygame.image.load("sprites/ore16x16.png"),
    "ruby_ore": pygame.image.load("sprites/ruby_ore16.png"),
    "player_left": pygame.image.load("sprites/player_left16.png"),
    "player_right": pygame.image.load("sprites/player_right16.png"),
    "tile_warp": pygame.image.load("sprites/warp.png"),
    "item_rubyshards": pygame.image.load("sprites/item_rubyshards.png"),
    "item_ironore": pygame.image.load("sprites/item_ironore.png"),
    "sell_arrows": pygame.image.load("sprites/sell_arrows.png")
    }
    
#TODO: put every sprite in this ID list