import pygame,sys
from pygame import  Color
import the_AI
import random
import Effect
import math
import textures
import sound
import menu
    
pygame.font.init()
font = pygame.font.SysFont(None, 16)

#90 120

class Base_Card:
    cost=1
    description = ["Average range, ave-","rage damage, average ","attack speed, it's the ","most basic and boring", "single target turret."]
    cardFloatX = 800.0
    cardFloatY = 500.0
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"Base_Turret")
    def draw(self,ID,x,y,background):
        background.blit(textures.Basic_Card_tex, (x,y))
        #pygame.draw.rect(background,Color(0,255,0),((x,y),(80,120)))

class Destroy(Base_Card):
    cost=0
    type = "on_turret"
    def use(self,x,y):
        for Curr in range(len(the_AI.Turret_Array)):
            if(the_AI.Turret_Array[Curr].x == x and the_AI.Turret_Array[Curr].y == y):
                the_AI.Turret_Array.pop(Curr)
                new_card(1)
                break
    def draw(self,ID,x,y,background):
        background.blit(textures.Mae_do_Digoo_tex, (x,y))

class Reply(Base_Card):
    cost=1
    type = "anywhere"
    def use(self,x,y):
        new_card(2)
    def draw(self,ID,x,y,background):
        background.blit(textures.Lucky_Draw, (x,y))
        #pygame.draw.rect(background,Color(0,0,255),((x+10,y+10),(70,100)))

class Predict(Base_Card):
    cost=2
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"IceTurret")
    def draw(self,ID,x,y,background):
        if(cardPickup==True and ID==cardSel):
            pygame.draw.rect(background,Color(200,200,200,100),(((x-x%50),(y-y%50)-100),(150,150)),2)
        background.blit(textures.Predict_tex, (x,y))

class Altar(Base_Card):
    cost=0
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"Altar")
    def draw(self,ID,x,y,background):
        background.blit(textures.Joel_tex, (x,y))

class Explode(Base_Card):
    cost=0
    type = "anywhere"
    def use(self,x,y):
        the_AI.MakeProj(the_AI.CocaColaEspuma(x,y,0,0))
    def draw(self,ID,x,y,background):
        background.blit(textures.Explode_tex, (x,y))
        #pygame.draw.rect(background,Color(100,100,100),((x,y),(80,120)))

class Dart(Base_Card):
    cost=1
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"Darter")
    def draw(self,ID,x,y,background):
        background.blit(textures.missing_tex, (x,y))
        pygame.draw.rect(background,Color(200,200,200),((x+10,y+10),(70,100)))

class MIND(Base_Card):
    cost=4
    type = "anywhere"
    timer=0
    def use(self,x,y):
        the_AI.MakeTurret(x-25,y-25,"Calamity")
    def draw(self,ID,x,y,background):
        self.timer+=1
        background.blit(textures.missing_tex, (x,y))
        pygame.draw.rect(background,Color(int(math.cos(self.timer/60)*100+150),0,0),((x+10,y+10),(70,100)))

class SOUL(Base_Card):
    cost=4
    type = "anywhere"
    timer=0
    def use(self,x,y):
        the_AI.MakeTurret(x-25,y-25,"Yharon")
    def draw(self,ID,x,y,background):
        self.timer+=1
        background.blit(textures.missing_tex, (x,y))
        pygame.draw.rect(background,Color(0,int(math.cos(self.timer/60)*100+150),0),((x+10,y+10),(70,100)))

class POWER(Base_Card):
    cost=4
    type = "anywhere"
    timer=0
    def use(self,x,y):
        the_AI.MakeTurret(x-25,y-25,"Destroyer")
    def draw(self,ID,x,y,background):
        self.timer+=1
        background.blit(textures.missing_tex, (x,y))
        pygame.draw.rect(background,Color(0,0,int(math.cos(self.timer/60)*100+150)),((x+10,y+10),(70,100)))

class DEATH(Base_Card):
    cost=8
    type = "anywhere"
    timer=0
    def use(self,x,y):
        the_AI.MakeTurret(x-25,y-25,"SCalamity")
    def draw(self,ID,x,y,background):
        self.timer+=1
        background.blit(textures.missing_tex, (x,y))
        pygame.draw.rect(background,Color(int(math.cos(self.timer/60)*100+150),int(math.cos(self.timer/60)*100+150),int(math.cos(self.timer/60)*100+150)),((x+10,y+10),(70,100)))

class HyperDrive(Base_Card):
    cost=2
    type = "anywhere"
    def use(self,x,y):
        the_AI.MakeProj(the_AI.HyperDriveCore(x,y))
    def draw(self,ID,x,y,background):
        if(cardPickup==True and ID==cardSel):
            pygame.draw.circle(background,Color(255,255,255),(x+40,y-40),150,2)
        background.blit(textures.missing_tex, (x,y))
        pygame.draw.rect(background,Color(0,0,100),((x+10,y+10),(70,100)))

class Sniper_TF2(Base_Card):
    cost=2
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"Sniper_TF2")
    def draw(self,ID,x,y,background):
        background.blit(textures.SniperTF2_tex, (x,y))
        #pygame.draw.rect(background,Color(50,150,100),((x,y),(80,120)))

class Enchance(Base_Card):
    cost=1
    type = "on_turret"
    def use(self,x,y):
        for Curr in range(len(the_AI.Turret_Array)):
            if(the_AI.Turret_Array[Curr].x == x and the_AI.Turret_Array[Curr].y == y):
                the_AI.MODTURRET(Curr,the_AI.Omega())
                break
    def draw(self,ID,x,y,background):
        background.blit(textures.missing_tex, (x,y))
        pygame.draw.rect(background,Color(0,0,0),((x,y),(80,120)))

class CARTIME(Base_Card):
    cost=0
    cardFloatX = 800.0
    cardFloatY = 500.0
    type = "anywhere"
    def use(self,x,y):
        the_AI.MakeProj(the_AI.CARTIME(x-x%50,0,0,15))
    def draw(self,ID,x,y,background):
        background.blit(textures.Stora_de_Mat, (x,y))
        #pygame.draw.rect(background,Color(0,255,0),((x,y),(80,120)))

class Wrath(Base_Card):
    cost=2
    cardFloatX = 800.0
    cardFloatY = 500.0
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"Slower")
    def draw(self,ID,x,y,background):
        background.blit(textures.Jojo_tex,(x,y))
        #pygame.draw.rect(background,Color(0,255,0),((x,y),(80,120)))

class Stonks(Base_Card):
    cost=2
    cardFloatX = 800.0
    cardFloatY = 500.0
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"Stonker")
    def draw(self,ID,x,y,background):
        background.blit(textures.missing_tex,(x,y))
        #pygame.draw.rect(background,Color(0,255,0),((x,y),(80,120)))

class OHAHOHOH(Base_Card):
    cost=4
    cardFloatX = 800.0
    cardFloatY = 500.0
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"Tachanka")
    def draw(self,ID,x,y,background):
        background.blit(textures.Tachanka_tex,(x,y))
        #pygame.draw.rect(background,Color(0,255,0),((x,y),(80,120)))

class papabenzos(Base_Card):
    cost=0
    cardFloatX = 800.0
    cardFloatY = 500.0
    type = "turret"
    def use(self,x,y):
        the_AI.MakeTurret(x,y,"PapaBento")
    def draw(self,ID,x,y,background):
        background.blit(textures.missing_tex,(x,y))
        #pygame.draw.rect(background,Color(0,255,0),((x,y),(80,120)))

cards = [] #should be array of cards
cardOffx = 400 #offset later
cardOffy = 500
cardSel = 0 #for outher code to deal whit«
cardPickup = False
#["Enchance","Reply","base_card","destroy_Card","Reply","Predict","Altar","Explode","Dart","MIND","SOUL","POWER","DEATH","HyperDrive","Sniper_TF2","Stora de Mat","Wrath","OHAHOHOH","papabenzos"]
possibleCards = ["Predict"]
debugMode = False
#placing a card returns it to your hand TODO
#cards placed in possibleCards array are put regaldless of deckbuilder

def new_card(num):
    global cards

    if menu.Overexdednd_enabled and possibleCards.__contains__("Altar"):
        for x in possibleCards:
            if x == "Altar":
                possibleCards.pop(possibleCards.index(x))

    if possibleCards==[]:
        possibleCards.append("base_card")

    for i in range(num):
        new = random.choice(possibleCards)
        if(new == "base_card"):
            cards.append(Base_Card())
        if(new == "destroy_Card"):
            cards.append(Destroy())
        if(new == "Reply"):
            cards.append(Reply())
        if(new == "Predict"):
            cards.append(Predict())
        if(new == "Altar" and not menu.Overexdednd_enabled):
            cards.append(Altar())
        if(new == "Explode"):
            cards.append(Explode())
        if(new == "Dart"):
            cards.append(Dart())
        if(new == "MIND"):
            cards.append(MIND())
        if(new == "SOUL"):
            cards.append(SOUL())
        if(new == "POWER"):
            cards.append(POWER())
        if(new == "DEATH"):
            cards.append(DEATH())
        if(new == "HyperDrive"):
            cards.append(HyperDrive())
        if(new == "Sniper_TF2"):
            cards.append(Sniper_TF2())
        if(new == "Enchance"):
            cards.append(Enchance())
        if(new == "Stora de Mat"):
            cards.append(CARTIME())
        if(new == "Wrath"):
            cards.append(Wrath())
        if(new == "Stonks"):
            cards.append(Stonks())
        if(new == "OHAHOHOH"):
            cards.append(OHAHOHOH())
        if(new == "papabenzos"):
            cards.append(papabenzos())



def mouseZone(mouseX,mouseY,X,Y,W,H):
    return mouseX>X and mouseX<X+W and mouseY>Y and mouseY<Y+H

def TryPlace(ID,x,y):
    global CardSacrife
    global CardSumon
    global CardSumonX
    global CardSumonY
    if menu.Overexdednd_enabled:
        cards[ID].use(x,y)
        cards.pop(ID)
    else:
        if(cards[ID].cost==0):
            cards[ID].use(x,y)
            cards.pop(ID)
        else:
            CardSacrife=True
            CardSumon=ID
            CardSumonX=x
            CardSumonY=y
    

PmousePress = False
PmousePress1 = False

CardSacrife = False

CardSumon = 0 # now whit missing m's!
CardSumonX = 0
CardSumonY = 0

CardKill = [] #KILL! *ding*

CardSumonTimer = 0
TurretSel = None

def cards_draw(background,win):
    #might as well put all
    global CardSacrife#fuck pythons variables
    global CardSumonTimer#fuck pythons variables
    global PmousePress
    global PmousePress1
    global TurretSel

    background.blit(textures.back_tex, (800,500))
    #pygame.draw.rect(background,Color(100,100,100),((800,500),(80,120)))
    
    mousePos = pygame.mouse.get_pos()
    mouseAct = pygame.mouse.get_pressed()

    if(CardSacrife):
        tmpsurface= pygame.Surface((900,600), pygame.SRCALPHA)#APLHAAAAAAAAAAAAAAAAAAAAA
        tmpsurface.fill((0,0,0,128))
        background.blit(tmpsurface, (0,0))
        #if(440)
        if(cards[CardSumon].cost==len(CardKill)):
            #pygame.draw.rect(background,Color(0,0,0),((300,150),(50,30)))
            #img = font.render(str("KILL!"), True, pygame.Color(255,255,255))
            #background.blit(img, (300,250))
            background.blit(textures.KILL, (337,210))
        #pygame.draw.rect(background,Color(0,0,0),((500,250),(50,30)))
        #img = font.render(str("no"), True, pygame.Color(255,255,255))
        #background.blit(img, (500,250))
        background.blit(textures.NO, (481,210))

    for x in range(len(cards)):
        X = int(cards[x].cardFloatX)
        Y = int(cards[x].cardFloatY)
        #if(cardPickup and cardSel==x):
        #    pygame.draw.rect(background,Color(0,0,0),((X+90,Y+40),(120,90)))
        #    for desc in cards[x].description:
        #        img = font.render(desc, True, pygame.Color(255,255,255))
        #        background.blit(img, (X+90,Y+40))
        #        Y+=10
        cards[x].draw(x,X,Y,background)

    if(CardSacrife):
        CardSumonTimer+=1
        image , square = textures.rsImage(textures.OponTheAltar,CardSumonTimer,(450,200),pygame.Vector2(0,0),(100,100))
        background.blit(image,square)

    if(mouseAct[0] and not PmousePress):
        for Curr in the_AI.Turret_Array:
            if(Curr.x<mousePos[0] and Curr.y<mousePos[1] and Curr.x+50>mousePos[0] and Curr.y+50>mousePos[1]):
                TurretSel = Curr
                break
            else: TurretSel = None

    if TurretSel != None:
        pygame.draw.circle(background,Color(50,50,100),(TurretSel.x+25,TurretSel.y+25),int(TurretSel.range*TurretSel.rangeMuiltplier),5)
    return background


tutorial_pause = False
def cards_math(mapp):
    global cardSel#fuck pythons variables
    global cardPickup#fuck pythons variables
    global PmousePress
    global PmousePress1
    global CardSacrife
    global tutorial_pause

    if(the_AI.WORKAROUND>0):
        new_card(the_AI.WORKAROUND)
        the_AI.WORKAROUND=0

    if(len(cards)>9):#remove the first card
        cards.pop(0)

    mousePos = pygame.mouse.get_pos()
    mouseAct = pygame.mouse.get_pressed()
    if(CardSacrife==False):
        if(mouseAct[0]==False and cardPickup==True and int(mousePos[1]/50)<9):
            placeX = mousePos[0]-mousePos[0]%50
            placeY = mousePos[1]-mousePos[1]%50
            Altared=False
            for Curr in the_AI.Turret_Array:#check if theirs a altar
                if(Curr.x==placeX and Curr.y==placeY):
                    try:#it gets the job done
                        if(Curr.IsAltar and Curr.level<4):
                            cards.pop(cardSel)
                            Curr.used+=1
                            Altared=True
                    except:
                        pass
            if(Altared==False and cardSel>=0 and cardSel<len(cards)):#if else use card mode
                if(cards[cardSel].type=="turret"):#act as like placing a turret
                    if(mapp[int(mousePos[1]/50)][int(mousePos[0]/50)] == "T"):
                        can = True
                        for Curr in the_AI.Turret_Array:
                            if(Curr.x == placeX and Curr.y == placeY):
                                can=False
                                break
                        if(can==True):
                            tutorial_pause = False
                            TryPlace(cardSel,placeX,placeY)
                elif(cards[cardSel].type=="on_turret"):#act as like actting on turret
                    if(mapp[int(mousePos[1]/50)][int(mousePos[0]/50)] == "T"):
                        can = False
                        for Curr in the_AI.Turret_Array:
                            if(Curr.x == placeX and Curr.y == placeY):
                                can=True
                                break
                        if(can==True):
                            TryPlace(cardSel,placeX,placeY)
                elif(cards[cardSel].type=="anywhere"):#act as like act on anything
                    TryPlace(cardSel,mousePos[0],mousePos[1])

        if(PmousePress1==False and mouseAct[2]==True):
            for Curr in the_AI.Turret_Array:#for free roaming turrets
                if(Curr.x<mousePos[0] and Curr.y<mousePos[1] and Curr.x+50>mousePos[0] and Curr.y+50>mousePos[1]):
                    sound.get(sound.CLICK)
                    #erm hum umh mh erm
                    #maybe an int was better
                    if(Curr.mode=="first"):
                        Curr.mode="last"
                        Effect.makePartic(Effect.Text(mousePos[0],mousePos[1],"last"))
                    elif(Curr.mode=="last"):
                        Curr.mode="health"
                        Effect.makePartic(Effect.Text(mousePos[0],mousePos[1],"health"))
                    elif(Curr.mode=="health"):
                        Curr.mode="close"
                        Effect.makePartic(Effect.Text(mousePos[0],mousePos[1],"close"))
                    elif(Curr.mode=="close"):
                        Curr.mode="first"
                        Effect.makePartic(Effect.Text(mousePos[0],mousePos[1],"first"))
                        
    else:
        if(mouseAct[0]==True and PmousePress==False and mouseZone(mousePos[0],mousePos[1],341,212,45,46) and cards[CardSumon].cost==len(CardKill)):
            cards[CardSumon].use(CardSumonX,CardSumonY)
            CardKill.append(CardSumon)
            CardKill.sort()
            CardKill.reverse()
            for x in CardKill:
                cards.pop(x)
            CardKill.clear()
            CardSacrife=False
        if(mouseAct[0]==True and PmousePress==False and mouseZone(mousePos[0],mousePos[1],514,212,45,46)):
            CardSacrife=False
            CardKill.clear()
        if(mouseAct[0]==False and cardPickup==True and mousePos[0]>400 and mousePos[0]<500 and mousePos[1]>150 and mousePos[1]<250):
            CardKill.append(cardSel)
            if(len(CardKill)>cards[CardSumon].cost):
                CardKill.pop(0)

    if(mouseAct[0]==False):
        cardPickup=False
    for x in range(len(cards)):
        if(CardSumon==x and CardSacrife==True):
            cards[x].cardFloatX=cards[x].cardFloatX*0.80+0.20*(450-45)
            cards[x].cardFloatY=cards[x].cardFloatY*0.80+0.20*(15)
        else:
            beingKilled=-1
            for y in range(len(CardKill)):
                if(CardKill[y]==x):
                    beingKilled=y
                    break
            if(beingKilled>=0):
                cards[x].cardFloatX=cards[x].cardFloatX*0.80+0.20*(450+90*(beingKilled-len(CardKill)/2))
                cards[x].cardFloatY=cards[x].cardFloatY*0.80+0.20*(320)
            else:
                if(cardPickup and cardSel==x):
                    cards[x].cardFloatX=cards[x].cardFloatX*0.80+0.20*(mousePos[0]-45)
                    cards[x].cardFloatY=cards[x].cardFloatY*0.80+0.20*(mousePos[1]+40)
                else:
                    if(mousePos[0]>(cardOffx+(x-len(cards)/2)*90+0) and mousePos[0]<(cardOffx+(x-len(cards)/2)*90+90) and mousePos[1]>450 and cardPickup==False):#is ! not a valide operacion?
                        if(mouseAct[0]):
                            cardPickup=True
                        else:
                            cardSel=x
                            cards[x].cardFloatX=cards[x].cardFloatX*0.75+0.25*(cardOffx+(x-len(cards)/2)*90)
                            cards[x].cardFloatY=cards[x].cardFloatY*0.75+0.25*(cardOffy-40)
                    else:
                        cards[x].cardFloatX=cards[x].cardFloatX*0.95+0.05*(cardOffx+(x-len(cards)/2)*90)
                        cards[x].cardFloatY=cards[x].cardFloatY*0.95+0.05*cardOffy
            #wait
            #something wrong

    PmousePress = mouseAct[0]
    PmousePress1 = mouseAct[2]