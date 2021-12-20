import os
import pygame,sys
from pygame import *
from pygame import K_ESCAPE, Color
import random
import math

Coca_cola_Espuma_3 = pygame.image.load(os.path.join("Turrets.Projs", "Coca-cola_Espuma_3.png"))

pygame.font.init()
font = pygame.font.SysFont(None, 24)

particleRemover = []
particles = [] #woah

class Base_effect:#THIS IS A BASE CLASS WHIT NO CONSTRUCTOR DONT EVER SPAWN
    x=0
    y=0
    vx=0
    vy=0
    timer=60
    def math(self,ID):
        if(self.timer==0):
            particleRemover.append(ID)
        self.timer -= 1
    
    def draw(self,background,win):
        pygame.draw.rect(background,Color(255,255,255),((self.x,self.y),(1,1)))
        return background

class Text(Base_effect):
    text = ""
    def __init__(self,x,y,text):
        self.x=x
        self.y=y
        self.text=text

    def math(self,ID):
        if(self.timer==0):
            particleRemover.append(ID)
        self.timer -= 1
        self.y-=1

    def draw(self,background,win):
        img = font.render(self.text, True, pygame.Color(255,255,255))
        background.blit(img, (self.x, self.y))
        return background

class Snow(Base_effect):
    timer=30
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def math(self,ID):
        if(self.timer==0):
            particleRemover.append(ID)
        self.timer -= 1
    def draw(self,background,win):
        pygame.draw.circle(background,Color(255,255,255),(self.x,self.y),int((30-self.timer)*3),int((31-self.timer)/4))
        #pygame.draw.rect(background,Color(int(51*self.timer),int(51*self.timer),int(51*self.timer)),((self.x,self.y),(1,1)))
        return background

class Tracer(Base_effect):
    timer=5
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
    def math(self,ID):
        if(self.timer==0):
            particleRemover.append(ID)
        self.timer -= 1
    def draw(self,background,win):
        pygame.draw.line(background,Color(97,89,12),(self.x,self.y),(self.vx,self.vy))
        #pygame.draw.rect(background,Color(int(51*self.timer),int(51*self.timer),int(51*self.timer)),((self.x,self.y),(1,1)))
        return background

class Sniper_Tracer(Base_effect):
    timer=30
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
    def math(self,ID):
        if(self.timer==0):
            particleRemover.append(ID)
        self.timer -= 1
    def draw(self,background,win):
        pygame.draw.line(background,Color(97,89,12),(self.x,self.y),(self.vx,self.vy))
        #pygame.draw.rect(background,Color(int(51*self.timer),int(51*self.timer),int(51*self.timer)),((self.x,self.y),(1,1)))
        return background

class espuma(Base_effect):
    timer=0
    vx=0
    vy=0
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def math(self,ID):
        self.timer += 1
        if(self.timer==60):
            particleRemover.append(ID)

    def draw(self,background,win):
        if(self.timer==0):
            return background
        #avoid div by 0
        #this is a 2d quadratic bezier curve
        pointS = 0
        pointSA = 2
        pointEA = 0.2
        pointE = 0
        timerS = self.timer/60
        interP1 = (pointS*(1-timerS)+pointSA*timerS)
        interP2 = (pointSA*(1-timerS)+pointEA*timerS)
        interP3 = (pointEA*(1-timerS)+pointE*timerS)
        interP4 = (interP1*(1-timerS)+interP2*timerS)
        interP5 = (interP2*(1-timerS)+interP3*timerS)
        scale =  (interP4*(1-timerS)+interP5*timerS)
        #there might be too much math

        scaledImage = pygame.transform.rotozoom(Coca_cola_Espuma_3,0,scale)
        background.blit(scaledImage, (self.x-75*scale,self.y-75*scale))
        return background

class BALST(Base_effect):
    timer=120
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def math(self,ID):
        if(self.timer==0):
            particleRemover.append(ID)
        self.timer -= 1
    def draw(self,background,win):
        pygame.draw.circle(background,Color(255,255,255),(self.x,self.y),int((120-self.timer)*12),int((121-self.timer)/16))
        #pygame.draw.rect(background,Color(int(51*self.timer),int(51*self.timer),int(51*self.timer)),((self.x,self.y),(1,1)))
        return background

def drawParticles_math():
    for Curr in range(len(particles)):
        particles[Curr].math(Curr)

    global particleRemover
    particleRemover.reverse()

    for Curr in particleRemover:
        particles.pop(Curr)

    particleRemover.clear()


def drawParticles_draw(background,win):
    for Curr in range(len(particles)):
        background = particles[Curr].draw(background,win)

    return background

def makePartic(particle):
    particles.append(particle)