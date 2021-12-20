import pygame
import os
import menu
from pygame import mouse
import cards
import textures

win = pygame.display.set_mode((900,600))
WIN = pygame.display.set_mode((900,600))
cardsAv = [
            ["Explode","Altar","destroy_Card","Stora de Mat","Reply","base_card","Predict","Sniper_TF2"],
            ["Wrath","OHAHOHOH"]
          ]

skins = {
"Explode": textures.Explode_tex, 
"Altar": textures.Joel_tex,
"Predict": textures.Predict_tex, 
"Sniper_TF2": textures.SniperTF2_tex, 
"Stora de Mat": textures.Stora_de_Mat, 
"Reply": textures.Lucky_Draw,
"destroy_Card": textures.Mae_do_Digoo_tex,
"base_card": textures.Basic_Card_tex,
"Wrath": textures.Jojo_tex,
"OHAHOHOH": textures.Tachanka_tex
        }

cardSel = None
cardSelNum = None
cardPick = None
deck = []
scroll = 30
LEFTSCROLL = pygame.Rect(0,450,25,150)
RIGHTSCROLL = pygame.Rect(875,450,25,150)
bruh = True
no = False


def deckPoggerrs(background):
    global cardSel
    global cardSelNum
    global deck
    global scroll
    global LEFTSCROLL
    global RIGHTSCROLL 
    global bruh
    global no
    global cardPick

    mousePos = pygame.mouse.get_pos()
    mouseAct = pygame.mouse.get_pressed()

    if menu.do:
        f=open(os.path.join("Cards","deck.txt"),"r")
        thing=f.read()
        f.close
        deck=thing.split("\n")
        deck.remove("")
        menu.do=False

    if not mouseAct[0]:
        no= False


    #pygame.draw.rect(background, (100,100,100), pygame.Rect(0,450,900,150))
    background.blit(textures.PlaceHolder_DeckBuilder_tex,(0,450))

    for i in range(cardsAv.__len__()):
        for j in range(cardsAv[i].__len__()):
            card = pygame.Rect((j*90)+(6+(j*10)-1),(i*80)+(6+(i*50)-1),90,120)

            background.blit(skins[cardsAv[i][j]], (card.x,card.y))

            if card.collidepoint(mousePos) and cardSel==None:
                pygame.draw.rect(background,(255,0,0), card, 3)
                if mouseAct[0] and cardSelNum == None:
                    cardSelNum = [i,j]
                    cardSel = cardsAv[i][j]  
                if mouseAct[2] and bruh:
                    deck.append(cardsAv[i][j])
                    bruh = False


    for a in range(len(deck)):

        cardInDeck = pygame.Rect((a*40)+((a*10))+scroll,460,90,120)

        try:
            background.blit(skins[deck[a]], (cardInDeck.x,cardInDeck.y))
        except:
            pass
            
        if mouseAct[0] and cardSel == None:
            if not no:
                if cardInDeck.collidepoint(mousePos):
                    if mousePos[0] > (a*40)+(6+(a*10)-1)+scroll+40 and len(deck) != 0:
                        if a+1 >= len(deck):
                            deck.pop(a)
                        else: 
                            deck.pop(a+1)
                    else:
                        deck.pop(a)
                    no = True

    if cardSelNum != None:
        if mouseAct[0]:
            cardPick = pygame.Rect(mousePos[0]-40,mousePos[1]-60,90,150)
            background.blit(skins[cardSel], (cardPick.x,cardPick.y))
            

        if not mouseAct[0]:
            if cardPick.colliderect(pygame.Rect(0,450,900,150)):
                #if deck.count(cardsAv[cardSelNum[0]][cardSelNum[1]])<4:
                    #deck.append(cardsAv[cardSelNum[0]][cardSelNum[1]])

                deck.append(cardsAv[cardSelNum[0]][cardSelNum[1]])
            cardSelNum = None
            cardSel = None
                

    if mouseAct[0]:
        if RIGHTSCROLL.collidepoint(mousePos) and scroll>-((len(deck)*40)+(6+(len(deck)*10)-1)+80 - 100) + 805:
            scroll -= 5
            no = True
        if LEFTSCROLL.collidepoint(mousePos) and scroll<30:
            scroll += 5
            no = True
    else:
        if RIGHTSCROLL.collidepoint(mousePos) and scroll>-((len(deck)*40)+(6+(len(deck)*10)-1)+80 - 100) + 805:
            scroll -= 1
            no = True
        if LEFTSCROLL.collidepoint(mousePos) and scroll<30:
            scroll += 1
            no = True
    
    if not mouseAct[2]:
        bruh = True

    pygame.draw.rect(background, (50,50,50), LEFTSCROLL)
    pygame.draw.rect(background, (50,50,50), RIGHTSCROLL)

    #does a quick gay overwrite
    if (cards.debugMode) : pass # do nothing
    elif deck == []: cards.possibleCards = ["base_card"]
    else : cards.possibleCards = deck

    f=open(os.path.join("Cards","deck.txt"),"w")
    a=-1
    for x in deck:
        a+=1
        if deck[a]!="":
            f.write(deck[a])
            f.write("\n")
    f.close

    return background

