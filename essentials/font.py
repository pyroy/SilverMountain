import pygame
import pygame.font
pygame.font.init()

font = pygame.font.SysFont("consolas", 10)

def render_to(canvas, position, text, color=(255,255,255)):
    if position[0] < 0 or position[1] < 0 or position[0] > canvas.get_rect().width or position[1] > canvas.get_rect().width:
        pass
    return canvas.blit(font.render(text, False, color), position)