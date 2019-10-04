import pygame

#this entire thing might just be moved to item_db.py, but we'll see when more sprites are added.

#gamesprites
player_sprite = pygame.image.load("sprites/player16x16.png")
pick_sprite = pygame.image.load("sprites/pick16x16.png")

#tilesprites
tile_dirt = pygame.image.load("tiles/tile_dirt16x16.png")

#environment sprites
env_stone = pygame.image.load("sprites/stone16x16.png")
env_ore = pygame.image.load("sprites/ore16x16.png")

IDS = {
    "tile_dirt": pygame.image.load("tiles/tile_dirt16x16.png"),
    "test_pick": pygame.image.load("sprites/pick16x16.png"),
    "env_stone": pygame.image.load("sprites/stone16x16.png"),
    "env_ore": pygame.image.load("sprites/ore16x16.png"),
    "player_left": pygame.image.load("sprites/player_left16.png"),
    "player_right": pygame.image.load("sprites/player_right16.png"),
    "tile_warp": pygame.image.load("sprites/warp.png")
    }
    
#TODO: put every sprite in this ID list