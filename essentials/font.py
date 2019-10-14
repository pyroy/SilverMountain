import pygame
import pygame.font
pygame.font.init()

font = pygame.font.SysFont("consolas", 10)

def render_to(canvas, position, text, color=(255,255,255), scale=1):

    if position[0] < 0 or position[1] < 0 or position[0] > canvas.get_rect().width or position[1] > canvas.get_rect().width:
        pass;
        
    return canvas.blit(pygame.transform.scale(font.render(text, False, color), get_size(text, scale)), position)
    
def get_size(text, scale=1):
    return (font.size(text)[0]*scale, font.size(text)[1]*scale)