import pygame

#this entire thing might just be moved to item_db.py, but we'll see when more sprites are added.

#gamesprites
player_sprite = pygame.image.load("sprites/idle.png")
pick_sprite = pygame.image.load("sprites/pick.png")

#tilesprites
tile_dirt = pygame.image.load("tiles/tile_dirt.png")

#environment sprites
env_stone = pygame.image.load("sprites/stone.png")
env_ore = pygame.image.load("sprites/ore.png")

IDS = {
    "test_pick": pygame.image.load("sprites/pick.png"),
    "env_stone": pygame.image.load("sprites/stone.png"),
    "env_ore": pygame.image.load("sprites/ore.png")
    }
    
#TODO: put every sprite in this ID list