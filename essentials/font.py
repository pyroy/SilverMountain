import pygame
import pygame.freetype
pygame.freetype.init()

font = pygame.freetype.SysFont("consolas", 10)
font.antialiased = False

def render_to(canvas, position, text, color=(255,255,255)):
    if position[0] < 0 or position[1] < 0 or position[0] > canvas.get_rect().width or position[1] > canvas.get_rect().width:
        pass
    return font.render_to(canvas, position, text, color)