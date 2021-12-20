from typing import Text
import random
import pygame
from pygame import *
import cards
import the_AI
import cards
import wave_generatore
import os
import sound
import textures
import triggerKeyboard
import ClientLeaderBoards

pygame.font.init()
font = pygame.font.SysFont(None, 24)

tutorial = False

class UI:
    x=0
    y=0
    w=0
    h=0
    func= ""
    TAG = ""
    enabled=False
    Text = ""
    def __init__(self,x,y,w,h,func,TAG,Text):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.func=func
        self.TAG=TAG
        self.Text=Text
    def Run(self):
        globals()[self.func]()
    def CRun(self):
        pass
    def Draw(self,background):
        pygame.draw.rect(background,Color(100,100,100),((self.x,self.y),(self.w,self.h)))
        pygame.draw.rect(background,Color(255,212,66),((self.x+2,self.y+2),(self.w-4,self.h-4)))
        img = font.render(str(self.Text), True, pygame.Color(255,255,255));img_sqr = img.get_rect();img_sqr.center = (self.x+self.w/2, self.y+self.h/2)
        background.blit(img, img_sqr)
        return background
        
class UIT(UI):
    def __init__(self,x,y,w,h,func,TAG,Text):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.func=func
        self.TAG=TAG
        self.Text=Text
    def Run(self):
        #no ! ?
        if(globals()[self.func]):#what is this.
            globals()[self.func] = False
        else:
            globals()[self.func] = True
    def CRun(self):
        pass
    def Draw(self,background):
        pygame.draw.rect(background,Color(100,100,100),((self.x,self.y),(self.w,self.h)))
        if(globals()[self.func]):
            pygame.draw.rect(background,Color(0,255,0),((self.x+2,self.y+2),(self.w-4,self.h-4)))
        else:
            pygame.draw.rect(background,Color(255,0,0),((self.x+2,self.y+2),(self.w-4,self.h-4)))
        img = font.render(str(self.Text), True, pygame.Color(255,255,255));img_sqr = img.get_rect();img_sqr.center = (self.x+self.w/2, self.y+self.h/2)
        background.blit(img, img_sqr)
        return background

class UIS(UI):
    def __init__(self,x,y,w,h,func,TAG,Text):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.func=func
        self.TAG=TAG
        self.Text=Text
    def Run(self):
        pass
    def CRun(self):
        mousePos = pygame.mouse.get_pos()
        globals()[self.func]=(mousePos[0]-self.x)/self.w
    def Draw(self,background):
        pygame.draw.rect(background,Color(100,100,100),((self.x,self.y),(self.w,self.h)))
        pygame.draw.rect(background,Color(255,212,66),((self.x+2,self.y+2),(globals()[self.func]*(self.w-4),self.h-4)))
        img = font.render(str(self.Text), True, pygame.Color(255,255,255));img_sqr = img.get_rect();img_sqr.center = (self.x+self.w/2, self.y+self.h/2)
        background.blit(img, img_sqr)
        return background

def MENUINIT(): 
    TurnTagOn("Start_Menu")

WIN = pygame.display.set_mode((900,600))

menu = [
UI(500,400,100,50,"Menu_Go_TO_menu","Start_Menu","Start"),

UI(390,175,110,50,"Menu_Start_Game","Main_Menu","Game"),
UIT(390,225,110,50,"Overexdednd_enabled","Main_Menu","Overexdend"),#it just works!
UI(390,275,110,50,"Menu_Go_options","Main_Menu","Options"),
UI(390,325,110,50,"Menu_Go_Deck_Building","Main_Menu","Deck"),
UI(390,375,110,50,"Lead_Boarding","Main_Menu","Leaderboard"),
UI(390,425,110,50,"Leave","Main_Menu","Exit"),

UI(795,5,100,50,"Menu_Go_Back","Deck","Back"),

UI(10,10,100,50,"Menu_Go_Back","LeadBoarding","Back"),

UI(400,250,100,50,"Menu_Go_Back","Lose_Menu","Back"),
UI(400,300,100,50,"","Lose_Menu","you suck"),

UI(400,225,100,50,"Menu_Go_Back","Options_Menu","Back"),
UIT(400,275,100,50,"Sound_Play","Options_Menu","Sound"),#it just works!
UIS(350,325,200,50,"Sound_Effects","Options_Menu",""),

UI(400,225,100,50,"Menu_UnPause","Main_Pause","Back"),
UI(400,275,100,50,"Menu_Go_options","Main_Pause","Options"),
UI(400,325,100,50,"Menu_Go_TO_menu","Main_Pause","Main Menu"),

UI(325,200,250,50,'AdeusMaedoLory','Parabens Mãe do Lory', 'Parabens Mãe do Lory!')]

Sound_Effects = 0.5
Sound_Play = True

def restart():
    cards.cards=[]
    cards.new_card(3)
    the_AI.Enemy_Array=[]
    the_AI.Turret_Array=[]
    the_AI.PROJ_Array=[]
    the_AI.Base_Healt=300
    wave_generatore.EnabledEnemies.clear()
    wave_generatore.EnabledEnemies_Dificulty.clear()
    wave_generatore.Enemies_in_Wave.clear()
    cards.TurretSel=None
    global Restart_map
    Restart_map=True

def Menu_Start_Game():
    global gaming
    gaming=True
    restart()
    TurnOff()

loop=True
def Leave():
    global loop
    loop = False

def Menu_Go_Back():
    global DeckBuildTime
    DeckBuildTime=False
    global Leaderboarding
    Leaderboarding=False
    TurnOff()
    if(menuPause):
        TurnTagOn("Main_Pause")
    else:
        TurnTagOn("Main_Menu")

def Start_Menu():
    TurnTagOn("Start_Menu")


def Menu_Go_options():
    TurnOff()
    TurnTagOn("Options_Menu")

def Menu_Go_TO_menu():
    global gaming
    global menuPause
    gaming=False
    menuPause=False
    TurnOff()
    TurnTagOn("Main_Menu")

def Menu_Pause():
    TurnOff()
    TurnTagOn("Main_Pause")

def Menu_UnPause():
    global menuPause
    menuPause=False
    TurnOff()

do=False
def Menu_Go_Deck_Building():
    global DeckBuildTime
    global do
    DeckBuildTime=True
    do=True
    TurnOff()
    TurnTagOn("Deck")

Leaderboarding = False
Ldo = False
def Lead_Boarding():
    global Leaderboarding
    global Ldo
    ClientLeaderBoards.tryMore = True
    Leaderboarding=True
    Ldo=True
    TurnOff()
    TurnTagOn("LeadBoarding")

def ParabensMaedoLory():
    global menuPause
    menuPause = True
    TurnOff()
    TurnTagOn('Parabens Mãe do Lory')

def AdeusMaedoLory():
    global menuPause
    menuPause = False
    TurnOff()

def DIE():
    global gaming
    gaming=False
    sound.soundPlay = False
    TurnTagOn("Lose_Menu")

def TurnTagOn(TAG):
    for Curr in menu:
        if(Curr.TAG==TAG):
            Curr.enabled=True

def TurnTagOff(TAG):
    for Curr in menu:
        if(Curr.TAG==TAG):
            Curr.enabled=False

def TurnOff():
    for Curr in menu:
        Curr.enabled=False

PmouseACT = False
UNchank = False

Overexdednd_enabled=False
Restart_map=False
DeckBuildTime=False

fixthis = pygame.image.load(os.path.join("Miscs", "fixthis.png"))
fixthis = pygame.transform.scale(fixthis,(900,600))

name = ""

def MENUDRAW(background):
    global PmouseACT
    global DeckBuildTime

    mousePos = pygame.mouse.get_pos()
    mouseAct = pygame.mouse.get_pressed()
    
    global menuPause
    if(not menuPause):
        for Curr in menu:
            if(Curr.TAG=="Start_Menu" and Curr.enabled):
                background.blit(textures.Start_Menu_background,(0,0))
                break
            elif(Curr.TAG=="Deck" and Curr.enabled):
                background.blit(textures.Deck_Builder_background,(0,0))
                break
            elif (Curr.TAG=="Main_Menu" and Curr.enabled):
                pygame.mixer.stop()
                background.blit(textures.Main_Menu_background,(0,0))
                img = font.render(str(name), True, pygame.Color(255,255,255))
                background.blit(img, (5,5))
                break
            elif (Curr.TAG=="Options_Menu" and Curr.enabled):
                background.blit(textures.Main_Menu_background,(0,0))
                break
            elif (Curr.TAG=="Lose_Menu" and Curr.enabled):
                background.blit(textures.Main_Menu_background,(0,0))
                break
            elif (Curr.TAG=="LeadBoarding" and Curr.enabled):
                pygame.mixer.stop()
                background.blit(textures.Main_Menu_background,(0,0))
                break
                
    else:
        #no fuking idea of making TRASPARENCY ON THIS whiout imgages
        #background.fill((250, 250, 250,100))
        background.blit(fixthis,(0,0))

    global UNchank

    for Curr in menu:
        if(Curr.enabled):
            background=Curr.Draw(background)
            if(mouseAct[0]==True and not UNchank):
                if(mousePos[0]>=Curr.x and mousePos[0]<=Curr.x+Curr.w and mousePos[1]>=Curr.y and mousePos[1]<=Curr.y+Curr.h):
                    if(PmouseACT==False and Curr.func!=""):
                        Curr.Run()
                        UNchank=True
                    Curr.CRun()

    UNchank=False

    WIN.blit(background, (0, 0))
    PmouseACT=mouseAct[0]

    sound.soundMultiplier=Sound_Effects
    sound.soundPlay=Sound_Play


    if triggerKeyboard.input_enable:
        background.fill([0,0,0])
        triggerKeyboard.sqr(0,200,900,50,"Name:",background,(0,0,0))
        triggerKeyboard.sqr(0,250,900,100,triggerKeyboard.ult,background,(255,212,66))
        triggerKeyboard.sqr(0,350,900,50,"Press Enter to continue",background,(0,0,0))

    return background

#globals()["myfunction"]()
#YES!

gaming = False
menuPause = False