import pygame

text = []
ult = ""

input_enable = False

pygame.font.init()
font = pygame.font.SysFont(None, 64)

def sqr(x,y,w,h,text,background,color):
    pygame.draw.rect(background,(100,100,100),((x,y),(w,h)))
    pygame.draw.rect(background,color,((x+2,y+2),(w-4,h-4)))
    img = font.render(str(text), True, pygame.Color(255,255,255));img_sqr = img.get_rect();img_sqr.center = (x+w/2, y+h/2)
    background.blit(img,img_sqr)