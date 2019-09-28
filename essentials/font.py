import pygame
import pygame.freetype
pygame.freetype.init()

font = pygame.freetype.SysFont("consolas", 10)
font.antialiased = False

def render_to(canvas, position, text, color=(255,255,255)):
    return font.render_to(canvas, position, text, color)