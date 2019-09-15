import pygame

#gamesprites
player_sprite = pygame.image.load("sprites/idle.png")
pick_sprite = pygame.image.load("sprites/pick.png")

#tilesprites
tile_dirt = pygame.image.load("tiles/tile_dirt.png")

#environment sprites
env_stone = pygame.image.load("sprites/stone.png")

IDS = {
    "test_pick": pygame.image.load("sprites/pick.png")
    }
    
#TODO: put every sprite in this ID list