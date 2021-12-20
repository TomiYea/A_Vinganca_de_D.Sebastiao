import pygame
from pygame import *
import random
import os

from pygame.key import name
import sound
import cards
import the_AI
import wave_generatore
import Effect
import menu
import deckBuilder
import textures
import ClientLeaderBoards
import triggerKeyboard
from pygame.time import Clock
import math


from pygame.constants import K_SPACE

WIN = pygame.display.set_mode((900,600))

pygame.display.set_caption("A Vingança de D. Sebastião")
pygame.display.set_icon(pygame.image.load("monkeyfuckyou.png"))

pygame.mixer.init()
pygame.mixer.set_num_channels(100)
pygame.mixer.music.set_volume(1)

pygame.font.init()
font = pygame.font.SysFont(None, 24)

TILEOBJECTS = (0,"vertical", "horizontal", "Down_To_Right_Turn", "Up_To_Right_Turn", "Right_To_Up_Turn", "Right_To_Down_Turn", "start", "T")


SQR_SIDE = 50

CurrentFrame = 0
CurrentWave = 1
WaveTimer = 600
EnemiesToSpawn = []
EnemySpawnerDelay = 0
ParabensMaedoLory = random.randint(30*60,3600*60)

OverExdend = True
OverExdend_hurtTimer = 60
PmousePress=False

menu.MENUINIT()

def load_random_map():
    mapp = [ [0]*18, [0]*18, [0]*18, [0]*18, [0]*18, [0]*18, [0]*18, [0]*18, [0]*18 ]

    def up(line, direction):
        line -= 1
        if direction=="right":
                mapp[line+1][column] = "Right_To_Up_Turn"
        direction = "up"
        return line, direction

    def down(line, direction):
        line += 1
        if direction=="right":
                mapp[line-1][column] = "Right_To_Down_Turn"
        direction = "down"
        return line, direction

    starting_pos_of_1 = random.randint(0,8)
    ending = [random.randint(0,8),17]

    column = 0
    line = starting_pos_of_1
    enabledown = True
    enableup = True

    column += 1
    direction = "right"
    mapp[line][column] = "horizontal"

    path_array = [(0, starting_pos_of_1*50), (50, starting_pos_of_1*50)]

    while True:
        try:
            if column != 17:
                if enableup == False:
                    num = random.randint(4,10)
                elif enabledown == False:
                    num = random.randint(1,7)
                else: num = random.randint(1,10)

                if num > 3 and num < 8:
                    if column != 17:
                        column += 1
                        if direction=="up":
                            mapp[line][column-1] = "Up_To_Right_Turn"
                        elif direction=="down":
                            mapp[line][column-1] = "Down_To_Right_Turn"
                        direction = "right"

                elif line != 0 and num <= 3 and direction!="down":
                    line, direction = up(line, direction)

                elif line != 8 and num <= 8 and direction!="up":
                    line, direction = down(line, direction)
                
            elif column == 17:
                if line < ending[0]:
                    line, direction = down(line, direction)
                elif line>ending[0]:
                    line, direction = up(line, direction)

            if direction != "right":
                mapp[line][column] = "vertical"
                if path_array[-1] != (column*50, line*50):
                    path_array.append((column*50, line*50))

            else:
                mapp[line][column] = "horizontal"
                if path_array[-1] != (column*50, line*50):
                    path_array.append((column*50, line*50))


        except: 
            pass

        if line == ending[0] and column == ending[1]:
            break

    mapp[starting_pos_of_1][0]="start"

    if not menu.Overexdednd_enabled:
        if direction=="up":
            path_tile_finish = textures.ENDD
        elif direction=="down":
            path_tile_finish = textures.ENDU
        elif direction=="right":
            path_tile_finish = textures.ENDR
        mapp[ending[0]][ending[1]]="finish"
    else:
        if direction=="up":
            path_tile_finish = textures.O_ENDD
        elif direction=="down":
            path_tile_finish = textures.O_ENDU
        elif direction=="right":
            path_tile_finish = textures.O_ENDR
        mapp[ending[0]][ending[1]]="finish"


    times=12
    while times>0:
        for i in range(len(mapp)):
            for b in range(len(mapp[i])):
                if b!=0:
                    if mapp[i][b] == 0 and mapp[i][b] != "T" and times>0:
                        try:
                            if mapp[i+1][b] != 0 or mapp[i-1][b]!=0 or mapp[i][b+1]!=0 or mapp[i][b-1]!=0:
                                if random.randint(1,50)==1:
                                    mapp[i][b] = "T"
                                    times-=1
                            elif random.randint(1,750)==1:
                                mapp[i][b] = "T"
                                times-=1
                        except:
                            pass

    the_AI.EnemyPath=path_array

    return mapp, path_tile_finish, path_array









#this function is too big
#maybe make it a tab

def maths(mapp):
    global PmousePress

    mousePos = pygame.mouse.get_pos()
    mouseAct = pygame.mouse.get_pressed()

    global OverExdend_hurtTimer

    global OverExdend

    global CurrentFrame

    OverExdend=menu.Overexdednd_enabled

    if(cards.CardSacrife==False):
        if(OverExdend):
            if(len(cards.cards)>3):
                if(OverExdend_hurtTimer==0):
                    the_AI.hurtBase(5)
                    OverExdend_hurtTimer=60
                OverExdend_hurtTimer-=1
        else:
            OverExdend_hurtTimer=60

    global WaveTimer
    global EnemiesToSpawn
    global font
    global CurrentWave
    global EnemySpawnerDelay
    global tutorial_pause
 
    if(cards.CardSacrife==False):
        the_AI.CurrentWave=CurrentWave

        the_AI.AI_math()
        Effect.drawParticles_math()
    cards.cards_math(mapp)

    if (cards.CardSacrife==False) and (cards.tutorial_pause==False):
        WaveTimer -= 1

        if(WaveTimer==0):
            CurrentWave += 1
            EnemiesToSpawn = wave_generatore.makeWave(CurrentWave)
            cards.new_card(1)

        if(len(EnemiesToSpawn)>0):
            if(EnemySpawnerDelay<=0):
                WaveTimer=600
                the_AI.MakeEnemy(EnemiesToSpawn.pop())
                EnemySpawnerDelay=16/(CurrentWave/10)
            EnemySpawnerDelay -= 1

        if(the_AI.Base_Healt<=0):
            if not menu.Overexdednd_enabled:
                try: ClientLeaderBoards.Try_Add_To_Leaderboard(CurrentWave, menu.name)
                except: pass
            menu.DIE()

    CurrentFrame = CurrentFrame + 1

    if CurrentFrame == ParabensMaedoLory:
        menu.ParabensMaedoLory()

    PmousePress = mouseAct[2]


def visuals(mapp,background):
    global PmousePress
    #the usage of the win might be bad for performace see later TODO

    #there might be a better way
    if not menu.Overexdednd_enabled:
        for i in range(len(mapp)):
            for b in range(len(mapp[i])):
                for x in range(len(textures.PATHLIST1)):
                    if mapp[i][b] == TILEOBJECTS[x]:
                        background.blit(textures.PATHLIST1[x], (b*50, i*50))
                if mapp[i][b]=="finish":
                    background.blit(path_tile_finish, (b*50, i*50))
    else:
        for i in range(len(mapp)):
            for b in range(len(mapp[i])):
                for x in range(len(textures.O_PATHLIST)):
                    if mapp[i][b] == TILEOBJECTS[x]:
                        background.blit(textures.O_PATHLIST[x], (b*50, i*50))
                if mapp[i][b]=="finish":
                    background.blit(path_tile_finish, (b*50, i*50))

    background.blit(textures.FOG, (0,0))

    mousePos = pygame.mouse.get_pos()
    mouseAct = pygame.mouse.get_pressed()

    global OverExdend_hurtTimer

    global OverExdend

    OverExdend=menu.Overexdednd_enabled

    if(OverExdend):
        if(len(cards.cards)>3):
            pygame.draw.rect(background,Color(255,0,0),((0,450),(900,150)),int(15+math.cos(float(OverExdend_hurtTimer)/5.0)*5))

    global WaveTimer
    global EnemiesToSpawn
    global font
    global CurrentWave
    global EnemySpawnerDelay
 
    #pygame.draw.rect(background,Color(120,120,0),((0,450),(900,200)))#replace whit texture (board?)
    if not menu.Overexdednd_enabled:
        background.blit(textures.PlaceHolder_Deck_tex,(0,450))
    else:
        background.blit(textures.PlaceHolder_Deck_Overexdend_tex,(0,450))

    background = the_AI.AI_draw(background,WIN)
    background = Effect.drawParticles_draw(background,WIN)
    background = cards.cards_draw(background,WIN)

    img = font.render(str(the_AI.Base_Healt), True, pygame.Color(255,0,0))
    pygame.draw.rect(background,Color(255,0,0),((0,30),(24,24)))#replace whit texture (heart?)
    background.blit(img, (24, 36))

    pygame.draw.rect(background,Color(255,255,255),((0,0),(int(WaveTimer/4),24)))
    pygame.draw.rect(background,Color(0,0,0),((0,0),(150,24)),3)
    img = font.render(str(CurrentWave-1), True, pygame.Color(255,255,255))
    background.blit(img, (150, 0))

    #img = font.render(str(mousePos[0])+"|"+str(mousePos[1]), True, pygame.Color(255,255,255))
    #background.blit(img, (0, 24))

    sound.soundCheckUp()
    return background

loop = True

mapp, path_tile_finish, path_array = load_random_map()

with open(os.path.join("Cards","deck.txt"),"r") as f:
    thing=f.read()
cards.possibleCards=thing.split("\n")
cards.possibleCards.remove("")

with open(os.path.join("Miscs","firstTime.txt"),"r") as f:
    thing=f.read()
firstTime = thing.split("\n")

try: menu.name=firstTime[1]
except: pass

while loop:
    WIN.fill((255,255,255))

    loop=menu.loop

    background = pygame.Surface(WIN.get_size())#bropbaply a very bad idea
    background = background.convert()#this too
    background.fill((250, 250, 250,255))
    
    if firstTime[0] == "True":
        triggerKeyboard.input_enable = True

    if(menu.gaming):
        background=visuals(mapp,background)
        if(not menu.menuPause):
            maths(mapp)
    
    if(not menu.gaming or menu.menuPause):
        menu.MENUDRAW(background)        
        if(menu.Restart_map):
            menu.Restart_map=False
            CurrentFrame=0
            ParabensMaedoLory = random.randint(30*60,3600*60)
            CurrentWave=1
            WaveTimer=600
            mapp, path_tile_finish, path_array = load_random_map()
        if menu.DeckBuildTime:
            background=deckBuilder.deckPoggerrs(background)
        if menu.Leaderboarding:
            ClientLeaderBoards.Leader_Boards_Draw(background)

    WIN.blit(background, (0, 0))

    pygame.display.update()


    input_key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            #print(cards.possibleCards)
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_SPACE:
            #    mapp, path_tile_finish, path_array = load_random_map()

            #if event.key == pygame.K_KP_ENTER:
            #    print(mapp, path_array)
            
            if event.key == pygame.K_ESCAPE:
                if(menu.gaming == True):
                    menu.menuPause = not menu.menuPause
                    menu.Menu_Pause()
            
            elif triggerKeyboard.input_enable:
                if event.key == pygame.K_BACKSPACE:
                    try: triggerKeyboard.text.pop()
                    except: pass
                elif (event.key == pygame.K_KP_ENTER or event.key == 13) and triggerKeyboard.ult!="":
                    triggerKeyboard.input_enable=False
                    menu.name = triggerKeyboard.ult
                    firstTime[0] = "False"
                    with open(os.path.join("Miscs","firstTime.txt"),"w") as f:
                        f.write(firstTime[0])
                        f.write("\n")
                        f.write(menu.name)

                elif event.key != 92 and event.key != 126 and event.key != 180 and event.key != pygame.K_KP_ENTER and event.key != 13 and len(triggerKeyboard.text)<=25: 
                    triggerKeyboard.text.append(event.unicode)

                triggerKeyboard.ult = ""
                for i in triggerKeyboard.text:
                    triggerKeyboard.ult += i

pygame.quit()