import pygame,sys
from pygame import K_ESCAPE, Color
import math
import Effect
import random
import textures
import sound

EnemyPath = [(0,0),(900,600)]

Enemy_deleter = []
PROJ_deleter = []
Turret_deleter = []#to be used more rarely

WaveHardener = 0.002#make their health incress SLOWLY each wave
CurrentWave = 1

#textures
#baaaad

class Base_enemy:
    x=0
    y=0
    hp=20
    maxhp=20
    dmg=2
    Tile_Interpelation=0.0
    current_Tile=0
    speed = 0.02
    MODS=[]
    #moddifers that are affected by buff/debuff
    speedMuiltplier=1 # can go negative!
    resistanceMuiltplier=1
    def __init__(self):
        self.x=EnemyPath[0][0]
        self.y=EnemyPath[0][1]
        self.hp = self.hp  * (1+WaveHardener*CurrentWave*CurrentWave)
        self.maxhp = self.hp
        self.MODS = []

    def MathMods(self,ID):
        self.speedMuiltplier=1 # can go negative!
        self.resistanceMuiltplier=1
        for curr in range(len(self.MODS)):
            mod = self.MODS[curr]
            mod.math(ID)
            self.speedMuiltplier*=mod.speedMuiltplier
            self.resistanceMuiltplier*=mod.resistanceMuiltplier
        for curr in reversed(range(len(self.MODS))):
            if(self.MODS[curr].delet):
                self.MODS.pop(curr)
        self.resistanceMuiltplier = max(self.resistanceMuiltplier,0)

    def DrawMods(self,background):
        for curr in range(len(self.MODS)):
            background=self.MODS[curr].draw(background,curr,self.x,self.y)
        return background

    def passive(self,ID):
        pass

    def onDeath(self,ID):
        pass

    def math_Enemy(self,ID):#ID is a method that i use so i can find where this actor is the array for later removal
        #why the self.?
        #interpelate between the points to make movement
        self.MathMods(ID)
        self.x=EnemyPath[self.current_Tile][0]*(1-self.Tile_Interpelation)+EnemyPath[self.current_Tile+1][0]*self.Tile_Interpelation
        self.y=EnemyPath[self.current_Tile][1]*(1-self.Tile_Interpelation)+EnemyPath[self.current_Tile+1][1]*self.Tile_Interpelation
        self.Tile_Interpelation +=self.speed*self.speedMuiltplier
        self.passive(ID)
        if(self.Tile_Interpelation>1.0):
            self.Tile_Interpelation=0
            self.current_Tile+=1
        if(self.Tile_Interpelation<0):
            if(self.current_Tile>0):
                self.Tile_Interpelation=1
                self.current_Tile-=1
            else:
                self.Tile_Interpelation=0
        if(self.current_Tile==len(EnemyPath)-1):
            Enemy_deleter.append(ID)
            hurtBase(self.dmg)
            return
        if(self.hp<=0):
            self.onDeath(ID)
            Enemy_deleter.append(ID)
            rand = random.randint(0,1)
            sound.get(sound.deathSound[rand])
            return

    def draw_Enemy(self,background,win):
        background.blit(textures.Basic_Enemy_tex,(self.x, self.y))
        pygame.draw.rect(background,Color(100,0,0),((self.x,self.y+40),(self.hp*50/self.maxhp,10)))
        self.DrawMods(background)
        return background

    def hurtMePlenty(self,damage):#migth be usefull to make this a function
        self.hp-=damage*self.resistanceMuiltplier

#classes are a amazing thing
class Fast_enemy(Base_enemy):
    hp=20
    speed=0.04
    dmg=4

    def draw_Enemy(self,background,win):
        background.blit(textures.Slightly_Faster_Enemy_tex,(self.x, self.y))
        pygame.draw.rect(background,Color(100,0,0),((self.x,self.y+40),(self.hp*50/self.maxhp,10)))
        self.DrawMods(background)
        return background

class Fat_enemy(Base_enemy):
    hp=60
    speed=0.02
    dmg=8

    def draw_Enemy(self,background,win):
        background.blit(textures.Fat_Enemy_tex,(self.x, self.y))
        pygame.draw.rect(background,Color(100,0,0),((self.x,self.y+40),(self.hp*50/self.maxhp,10)))
        self.DrawMods(background)
        return background

class Digoo(Base_enemy):
    hp=1000
    speed=0.005
    dmg=120

    def draw_Enemy(self,background,win):
        background.blit(textures.Coca_cola_Espuma_0,(self.x, self.y))
        pygame.draw.rect(background,Color(100,0,0),((self.x,self.y+40),(self.hp*50/self.maxhp,10)))
        self.DrawMods(background)
        return background

class Disabler_enemy(Base_enemy):
    hp=20
    speed=0.02
    dmg=2

    def onDeath(self,ID):
        for curr in range(len(Turret_Array)):
            MODTURRET(curr,Silence())
        Effect.makePartic(Effect.BALST(int(self.x),int(self.y)))

    def draw_Enemy(self,background,win):
        background.blit(textures.Disabler_Enemy_tex,(self.x,self.y))
        pygame.draw.rect(background,Color(100,0,0),((self.x,self.y+40),(self.hp*50/self.maxhp,10)))
        self.DrawMods(background)
        return background

class Shilder_enemy(Base_enemy):
    hp=20
    speed=0.02
    dmg=2

    cooldown = 180

    def passive(self, ID):
        self.cooldown-=1
        if(self.cooldown==0):
            target = random.randint(0,len(Enemy_Array)-1)
            MODENEMY(target,PROCTECT())
            self.cooldown=180
            Effect.makePartic(Effect.Sniper_Tracer(self.x+25,self.y+25,Enemy_Array[target].x+25,Enemy_Array[target].y+25))

    def draw_Enemy(self,background,win):
        background.blit(textures.Shielder_Enemy_tex,(self.x,self.y))
        pygame.draw.rect(background,Color(100,0,0),((self.x,self.y+40),(self.hp*50/self.maxhp,10)))
        self.DrawMods(background)
        return background

class Base_Turret:
    x=0
    y=0
    r=0
    cooldown=0
    MaxCooldown=30
    range=200
    mode = "first"
    dmg = 5
    #moddifers that are affected by buff/debuff
    cooldownMuiltplier=1
    rangeMuiltplier=1
    damageMuiltplier=1
    MODS = []
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.MODS=[]

    def MathMods(self,ID):
        self.cooldownMuiltplier=1
        self.rangeMuiltplier=1
        self.damageMuiltplier=1
        for curr in range(len(self.MODS)):
            mod = self.MODS[curr]
            mod.math(ID)
            self.cooldownMuiltplier*=mod.cooldownMuiltplier
            self.rangeMuiltplier*=mod.rangeMuiltplier
            self.damageMuiltplier*=mod.damageMuiltplier
        for curr in reversed(range(len(self.MODS))):
            if(self.MODS[curr].delet):
                self.MODS.pop(curr)
        self.cooldownMuiltplier = max(self.cooldownMuiltplier,0)
        self.rangeMuiltplier = max(self.rangeMuiltplier,0.01)
    def DrawMods(self,background):
        for curr in range(len(self.MODS)):
            background=self.MODS[curr].draw(background,curr,self.x,self.y)
        return background

    def findClosestEnemy(self,ID):
        global Enemy_Array
        Enemy_ID=-1
        if(len(Enemy_Array)>0):#yes this operation must be done every frame so that tower dont shoot things they cant
            if(self.mode == "close"):
                min_dist=9999999#big
                for Curr in range(len(Enemy_Array)):
                    tmpEnemy = Enemy_Array[Curr]
                    dist = math.dist((self.x,self.y),(tmpEnemy.x,tmpEnemy.y))
                    if(dist<min_dist and dist<self.range*self.rangeMuiltplier):
                        min_dist=dist
                        Enemy_ID=Curr
            if(self.mode == "first"):
                min_dist=0#smool
                for Curr in range(len(Enemy_Array)):
                    tmpEnemy = Enemy_Array[Curr]
                    dist = math.sqrt((self.x-tmpEnemy.x)**2+(self.y-tmpEnemy.y)**2)
                    Mapdist = tmpEnemy.current_Tile + tmpEnemy.Tile_Interpelation
                    if(Mapdist>min_dist and dist<self.range*self.rangeMuiltplier):
                        min_dist=Mapdist
                        Enemy_ID=Curr
            if(self.mode == "last"):
                min_dist=9999999#big
                for Curr in range(len(Enemy_Array)):
                    tmpEnemy = Enemy_Array[Curr]
                    dist = math.sqrt((self.x-tmpEnemy.x)**2+(self.y-tmpEnemy.y)**2)
                    Mapdist = tmpEnemy.current_Tile + tmpEnemy.Tile_Interpelation
                    if(Mapdist<min_dist and dist<self.range*self.rangeMuiltplier):
                        min_dist=Mapdist
                        Enemy_ID=Curr
            if(self.mode == "health"):
                min_dist=0#smool
                for Curr in range(len(Enemy_Array)):
                    tmpEnemy = Enemy_Array[Curr]
                    dist = math.sqrt((self.x-tmpEnemy.x)**2+(self.y-tmpEnemy.y)**2)
                    Mapdist = tmpEnemy.hp
                    if(Mapdist>min_dist and dist<self.range*self.rangeMuiltplier):
                        min_dist=Mapdist
                        Enemy_ID=Curr
            #its tan2:tangenting harder baby!
            #90% on roten circutes
            #"my function of the year!" - local sleep deprived programer
        return Enemy_ID

    def math_Turret(self,ID):#ID is a method that i use so i can find where this actor is the array for later removal
        #why the self.?
        self.MathMods(ID)
        Enemy_ID = self.findClosestEnemy(ID)
        if(Enemy_ID>=0):
          self.r=math.atan2(Enemy_Array[Enemy_ID].y-self.y,Enemy_Array[Enemy_ID].x-self.x)
        if(self.cooldown>0):
            self.cooldown-=1*self.cooldownMuiltplier
        if(Enemy_ID>=0 and self.cooldown<=0):
            self.Attack_Enemy(Enemy_ID,self.dmg*self.damageMuiltplier)
            Effect.makePartic(Effect.Tracer(self.x+25,self.y+25,Enemy_Array[Enemy_ID].x+25,Enemy_Array[Enemy_ID].y+25))

    def Attack_Enemy(self,Enemy_ID,damage):
        Enemy_Array[Enemy_ID].hurtMePlenty(damage)
        #sound.get(sound.PEW)
        self.cooldown=self.MaxCooldown

    def draw_Turret(self,background,win):
        Basic_Turret_Upper = pygame.transform.rotate(textures.Basic_Turret_Upper, math.degrees(-self.r))
        Basic_Turret_Upper_Square = Basic_Turret_Upper.get_rect()
        Basic_Turret_Upper_Square.center = (self.x+25, self.y+25)

        background.blit(textures.Basic_Turret_Base, (self.x,self.y))
        background.blit(Basic_Turret_Upper, Basic_Turret_Upper_Square)
        background=self.DrawMods(background)
        
        #alpha channel not working
        #dont know why
        return background

    def draw_Range(self,background,win):
        #pygame.draw.circle(background,Color(0,50,100),(self.x+25,self.y+25),int(self.range*self.rangeMuiltplier),1)
        return background

class IceTurret(Base_Turret):
    MaxCooldown = 30
    dmg = 4
    range = 1
    def math_Turret(self,ID):
        self.MathMods(ID)
        global Enemy_Array
        if(self.cooldown>0):
            self.cooldown-=self.cooldownMuiltplier
        else:
            self.cooldown = self.MaxCooldown
            #Effect.makePartic(Effect.Snow(self.x+25,self.y+25))
            for Curr in range(len(Enemy_Array)):
                if(self.x - 75 <= Enemy_Array[Curr].x and self.x + 75 >= Enemy_Array[Curr].x and self.y - 75 <= Enemy_Array[Curr].y and self.y + 75 >= Enemy_Array[Curr].y):
                    self.Attack_Enemy(Curr,self.dmg*self.damageMuiltplier)

    def Attack_Enemy(self,Enemy_ID,damage):
        Enemy_Array[Enemy_ID].hurtMePlenty(damage)
        #sound.get(sound.BOOM1)
        self.cooldown=self.MaxCooldown
    
    def draw_Turret(self,background,win):
        #pygame.draw.rect(background,Color(0,255,255),((self.x,self.y),(50,50)))
        background.blit(textures.Diogoo_Base,(self.x,self.y))
        rotated_image = pygame.transform.rotate(textures.Diogoo_Fan,self.cooldown/self.MaxCooldown*180)
        new_rect = rotated_image.get_rect(center = textures.Diogoo_Fan.get_rect(topleft = (self.x,self.y)).center)
        background.blit(rotated_image, new_rect)
        background.blit(textures.Diogoo_Upper,(self.x,self.y))
        img,rect=textures.rsImage(textures.Diogoo_Fart,self.cooldown/self.MaxCooldown*90,(self.x+25,self.y+25),pygame.Vector2(0,0),(int(125+math.cos(self.cooldown/self.MaxCooldown*math.pi*2)*25),int(125+math.cos(self.cooldown/self.MaxCooldown*math.pi*2)*25)))
        background.blit(img,rect)
        self.DrawMods(background)
        #alpha channel not working
        #dont know why
        return background

    def draw_Range(self,background,win):
        #pygame.draw.rect(background,Color(200,200,200,100),((self.x-50,self.y-50),(150,150)),2)
        return background

class Altar(Base_Turret):
    IsAltar=True
    used = 0
    required = 2
    level = 0
    MaxCooldown=60
    AuraCooldown=300
    MaxAuraCooldown=300
    dmg = 5
    range=300
    Tick=1

    #too boring
    #make better attacks

    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def math_Turret(self,ID):#ID is a method that i use so i can find where this actor is the array for later removal
        self.MathMods(ID)
        if(self.used == self.required and self.level<4):
            self.level+=1
            self.used=0
            self.required*=2
            #self.required=1
            if(self.level==2):
                self.MaxCooldown=45
            if(self.level==4):
                self.MaxCooldown=30
                self.IsAltar=False
            
        Enemy_ID = self.findClosestEnemy(ID)
        if(Enemy_ID>=0):
          self.r=math.atan2(Enemy_Array[Enemy_ID].y-self.y,Enemy_Array[Enemy_ID].x-self.x)
        if(self.cooldown>0):
            self.cooldown-=self.cooldownMuiltplier
        if(self.cooldown<=0 and Enemy_ID>=0):
            if(self.level==1):
                MakeProj(Bolt(self.x,self.y,math.cos(self.r)*8,math.sin(self.r)*8))
            if(self.level==2):
                self.Tick = self.Tick*-1+1
                if(self.Tick==0):
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r)*8,math.sin(self.r)*8))
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r+math.pi/4)*8,math.sin(self.r+math.pi/4)*8))
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r-math.pi/4)*8,math.sin(self.r-math.pi/4)*8))
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r+math.pi/8)*8,math.sin(self.r+math.pi/8)*8))
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r-math.pi/8)*8,math.sin(self.r-math.pi/8)*8))
                else:
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r+math.pi/8)*8,math.sin(self.r+math.pi/8)*8))
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r-math.pi/8)*8,math.sin(self.r-math.pi/8)*8))
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r+math.pi/16)*8,math.sin(self.r+math.pi/16)*8))
                    MakeProj(Bolt(self.x,self.y,math.cos(self.r-math.pi/16)*8,math.sin(self.r-math.pi/16)*8))
            if(self.level>2):
                MakeProj(SplitShot(self.x,self.y,math.cos(self.r)*4,math.sin(self.r)*4))
            self.cooldown=self.MaxCooldown
        if(self.level==4):
            self.AuraCooldown-=1
            if(self.AuraCooldown<=0):
                ran = random.random()*math.pi*2-math.pi
                MakeProj(Aura(self.x,self.y,math.cos(ran)*4,math.sin(ran)*4))
                self.AuraCooldown=self.MaxAuraCooldown
    
    def draw_Turret(self,background,win):
        #MHHH
        #BAD
        if(self.level==0):
            background.blit(textures.Estatua_Joel_0,(self.x,self.y))
        if(self.level==1):
            background.blit(textures.Estatua_Joel_1,(self.x,self.y))
        if(self.level==2):
            background.blit(textures.Estatua_Joel_2,(self.x,self.y))
        if(self.level==3):
            background.blit(textures.Estatua_Joel_3,(self.x,self.y))
        if(self.level==4):
            background.blit(textures.Estatua_Joel_4,(self.x,self.y))
        #pygame.draw.rect(background,Color(100,100,100),((self.x,self.y),(50,50)))
        pygame.draw.arc(background,Color(200,200,200),((self.x,self.y),(50,50)),0,self.used*math.pi*2/self.required,5)
        self.DrawMods(background)
        #alpha channel not working
        #dont know why
        return background

    def draw_Range(self,background,win):
        #pygame.draw.circle(background,Color(0,50,100),(self.x+25,self.y+25),int(self.range),1)
        return background

class Darter(Base_Turret):
    MaxCooldown = 35
    dmg = 0
    range = 0

    def math_Turret(self,ID):
        self.MathMods(ID)
        if(self.cooldown>0):
            self.cooldown-=self.cooldownMuiltplier
        else:
            self.cooldown=self.MaxCooldown
            for i in range(8):
                MakeProj(Dart(self.x,self.y,math.cos(i*math.pi/4)*8,math.sin(i*math.pi/4)*8))


    def draw_Turret(self,background,win):
        pygame.draw.rect(background,Color(255,0,255),((self.x,self.y),(50,50)))
        self.DrawMods(background)
        return background

    def draw_Range(self,background,win):
        return background

class Calamity(Base_Turret):
    MaxCooldown = 15
    dmg = 0
    range = 900000
    vx=0
    vy=0
    wavespawned=0

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.wavespawned=CurrentWave

    def math_Turret(self,ID):
        self.MathMods(ID)
        ENEMYSPOTED = self.findClosestEnemy(ID)
        global Enemy_Array
        #self.vx+=random.random()*0.2-0.1
        #self.vy+=random.random()*0.2-0.1
        if(ENEMYSPOTED>=0):
            self.r=math.atan2(Enemy_Array[ENEMYSPOTED].y-self.y,Enemy_Array[ENEMYSPOTED].x-self.x)
            distToEnemy = math.dist((self.x,self.y),(Enemy_Array[ENEMYSPOTED].x,Enemy_Array[ENEMYSPOTED].y))
            self.vx+=math.cos(self.r)*(distToEnemy-150)/800
            self.vy+=math.sin(self.r)*(distToEnemy-150)/800
            self.vx=self.vx/20*19
            self.vy=self.vy/20*19
        if(self.cooldown<=0 and ENEMYSPOTED>=0):
            self.cooldown=self.MaxCooldown
            MakeProj(Brimstone(self.x,self.y,math.cos(self.r)*15,math.sin(self.r)*15))
            MakeProj(Brimstone(self.x,self.y,math.cos(self.r+math.pi/16)*15,math.sin(self.r+math.pi/16)*15))
            MakeProj(Brimstone(self.x,self.y,math.cos(self.r-math.pi/16)*15,math.sin(self.r-math.pi/16)*15))
        else:
            self.cooldown-=self.cooldownMuiltplier
        self.vx=self.vx/50*49
        self.vy=self.vy/50*49
        self.x+=self.vx
        self.y+=self.vy
        self.y=max(min(self.y,395),5)
        self.x=max(min(self.x,895),5)
        if(self.wavespawned+1 < CurrentWave):
            for Curr in range(32):
                MakeProj(Brimstone(self.x,self.y,math.cos(Curr*math.pi/16)*1,math.sin(Curr*math.pi/16)*1))
            Turret_deleter.append(ID)

    def draw_Turret(self,background,win):
        #pygame.draw.rect(background,Color(255,0,255),((self.x,self.y),(50,50)))
        #background.blit(Calamity_tex, (self.x, self.y))
        rotated_image = pygame.transform.rotate(textures.Calamity_tex,-self.r/math.pi*180)
        new_rect = rotated_image.get_rect(center = textures.Calamity_tex.get_rect(topleft = (self.x,self.y)).center)
        background.blit(rotated_image, new_rect)
        self.DrawMods(background)
        return background

    def draw_Range(self,background,win):
        return background

class SCalamity(Base_Turret):
    MaxCooldown = 300
    dmg = 0
    range = 900000
    vx=0
    vy=0
    wavespawned=0
    Attack = -1
    AttackCooldown = 300

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.wavespawned=CurrentWave

    def math_Turret(self,ID):
        self.MathMods(ID)
        ENEMYSPOTED = self.findClosestEnemy(ID)
        #self.vx+=random.random()*0.2-0.1
        #self.vy+=random.random()*0.2-0.1
        global Enemy_Array
        if(ENEMYSPOTED>=0):
            self.r=math.atan2(Enemy_Array[ENEMYSPOTED].y-self.y,Enemy_Array[ENEMYSPOTED].x-self.x)
            distToEnemy = math.dist((self.x,self.y),(Enemy_Array[ENEMYSPOTED].x,Enemy_Array[ENEMYSPOTED].y))
            self.vx+=math.cos(self.r)*(distToEnemy-150)/800
            self.vy+=math.sin(self.r)*(distToEnemy-150)/800
            self.vx=self.vx/20*19
            self.vy=self.vy/20*19
            if(self.AttackCooldown<=0):
                if(self.Attack==-1):
                    self.Attack=random.randint(0,2)
                    if(self.Attack==0):
                        self.AttackCooldown=300
                        self.MaxCooldown=300
                    if(self.Attack==1):
                        self.AttackCooldown=300
                        self.MaxCooldown=15
                    if(self.Attack==2):
                        self.AttackCooldown=300
                        self.MaxCooldown=100
                else:
                    self.Attack=-1
                    self.AttackCooldown=300
        if(self.cooldown<=0 and ENEMYSPOTED>=0):
            if(self.Attack==0):
                Effect.makePartic(Effect.BALST(int(self.x+25),int(self.y+25)))
                for Curr in range(len(Enemy_Array)):
                    MODENEMY(Curr,FEAR())
                    self.cooldown=self.MaxCooldown
                    
            if(self.Attack==1):
                self.cooldown=self.MaxCooldown
                MakeProj(SBrimstone(self.x,self.y,math.cos(self.r)*15,math.sin(self.r)*15))
                MakeProj(SBrimstone(self.x,self.y,math.cos(self.r+math.pi/16)*15,math.sin(self.r+math.pi/16)*15))
                MakeProj(SBrimstone(self.x,self.y,math.cos(self.r-math.pi/16)*15,math.sin(self.r-math.pi/16)*15))

            if(self.Attack==2):
                self.cooldown=self.MaxCooldown
                self.vx = math.cos(self.r)*20
                self.vy = math.sin(self.r)*20
        else:
            self.cooldown-=self.cooldownMuiltplier

        if(self.Attack==2):
            self.cool(0)
            if(self.cooldown%20==0):
                Effect.makePartic(Effect.AfterImage(self.x,self.y,self.r))

        self.AttackCooldown-=1

        self.vx=self.vx/50*49
        self.vy=self.vy/50*49
        self.x+=self.vx
        self.y+=self.vy
        self.y=max(min(self.y,395),5)
        self.x=max(min(self.x,895),5)
        if(self.wavespawned+3 < CurrentWave):
            for Curr in range(32):
                MakeProj(SBrimstone(self.x,self.y,math.cos(Curr*math.pi/16)*1,math.sin(Curr*math.pi/16)*1))
                MakeProj(SBrimstone(self.x,self.y,math.cos(Curr*math.pi/16+math.pi/32)*0.9,math.sin(Curr*math.pi/16+math.pi/32)*0.9))
                MakeProj(SBrimstone(self.x,self.y,math.cos(Curr*math.pi/16)*0.8,math.sin(Curr*math.pi/16)*0.8))
            Turret_deleter.append(ID)

    def cool(self,ID):
        for i in range(len(Enemy_Array)):
            Curr = Enemy_Array[i]
            if(self.x-25<=Curr.x+50 and self.x+25>=Curr.x and self.y-25<=Curr.y+50 and self.y+25>=Curr.y):
                Curr.hurtMePlenty(5)
                MODENEMY(i,Melting())

    def draw_Turret(self,background,win):
        #pygame.draw.rect(background,Color(255,0,255),((self.x,self.y),(50,50)))
        #background.blit(Calamity_tex, (self.x, self.y))
        rotated_image = pygame.transform.rotate(textures.SCalamity_tex,-self.r/math.pi*180)
        new_rect = rotated_image.get_rect(center = textures.SCalamity_tex.get_rect(topleft = (self.x-15,self.y-15)).center)
        background.blit(rotated_image, new_rect)
        self.DrawMods(background)
        return background

    def draw_Range(self,background,win):
        return background

class Yharon(Base_Turret):
    MaxCooldown = 60
    dmg = 0
    range = 900000
    vx=0
    vy=0
    wavespawned=0

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.wavespawned=CurrentWave

    def math_Turret(self,ID):
        self.MathMods(ID)
        ENEMYSPOTED = self.findClosestEnemy(ID)
        global Enemy_Array
        #self.vx+=random.random()*0.2-0.1
        #self.vy+=random.random()*0.2-0.1
        if(ENEMYSPOTED>=0):
            self.r=math.atan2(Enemy_Array[ENEMYSPOTED].y-self.y,Enemy_Array[ENEMYSPOTED].x-self.x)
            distToEnemy = math.dist((self.x,self.y),(Enemy_Array[ENEMYSPOTED].x,Enemy_Array[ENEMYSPOTED].y))
            self.vx+=math.cos(self.r)*(distToEnemy-150)/800
            self.vy+=math.sin(self.r)*(distToEnemy-150)/800
            self.vx=self.vx/20*19
            self.vy=self.vy/20*19
        if(self.cooldown<=0 and ENEMYSPOTED>=0):
            self.cooldown=self.MaxCooldown
            MakeProj(FireBall(self.x,self.y,math.cos(self.r)*2,math.sin(self.r)*2))
        else:
            self.cooldown-=self.cooldownMuiltplier
        self.vx=self.vx/50*49
        self.vy=self.vy/50*49
        self.x+=self.vx
        self.y+=self.vy
        self.y=max(min(self.y,395),5)
        self.x=max(min(self.x,895),5)
        if(self.wavespawned+1 < CurrentWave):
            for Curr in range(8):
                MakeProj(FireBall(self.x,self.y,math.cos(Curr*math.pi/4)*8,math.sin(Curr*math.pi/4)*8))
            Turret_deleter.append(ID)

    def draw_Turret(self,background,win):
        #pygame.draw.rect(background,Color(255,0,255),((self.x,self.y),(50,50)))
        #background.blit(Calamity_tex, (self.x, self.y))
        rotated_image = pygame.transform.rotate(textures.Yharon_tex,-self.r/math.pi*180)
        new_rect = rotated_image.get_rect(center = textures.Yharon_tex.get_rect(topleft = (self.x,self.y)).center)
        background.blit(rotated_image, new_rect)
        self.DrawMods(background)
        return background

    def draw_Range(self,background,win):
        return background

class Destroyer(Base_Turret):
    MaxCooldown = 60
    dmg = 0
    range = 900000
    vx=0
    vy=0
    wavespawned=0

    BodySegments = []

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.wavespawned=CurrentWave
        self.BodySegments = []
        for Curr in range(3):
            self.BodySegments.append(pygame.Vector3(x,y,0))

    def math_Turret(self,ID):
        self.MathMods(ID)
        ENEMYSPOTED = self.findClosestEnemy(ID)
        global Enemy_Array
        #self.vx+=random.random()*0.2-0.1
        #self.vy+=random.random()*0.2-0.1
        if(ENEMYSPOTED>=0):
            TOenemy=math.atan2(Enemy_Array[ENEMYSPOTED].y-self.y,Enemy_Array[ENEMYSPOTED].x-self.x)
            #distToEnemy = math.dist((self.x,self.y),(Enemy_Array[ENEMYSPOTED].x,Enemy_Array[ENEMYSPOTED].y))
            self.vx+=math.cos(TOenemy)
            self.vy+=math.sin(TOenemy)
            self.r=math.atan2(self.vy,self.vx)
        else:
            self.cooldown-=self.cooldownMuiltplier
            self.vx=self.vx/50*49
            self.vy=self.vy/50*49
        self.cool(ID)

        TargetA = math.atan2(self.y-self.BodySegments[0].y,self.x-self.BodySegments[0].x)
        TargetD = math.dist((self.x,self.y),(self.BodySegments[0].x,self.BodySegments[0].y))
        self.BodySegments[0].z=TargetA
        self.BodySegments[0].x+=math.cos(TargetA)*(TargetD-40)
        self.BodySegments[0].y+=math.sin(TargetA)*(TargetD-40)

        for Curr in range(1,len(self.BodySegments)):
            TargetA = math.atan2(self.BodySegments[Curr-1].y-self.BodySegments[Curr].y,self.BodySegments[Curr-1].x-self.BodySegments[Curr].x)
            TargetD = math.dist((self.BodySegments[Curr-1].x,self.BodySegments[Curr-1].y),(self.BodySegments[Curr].x,self.BodySegments[Curr].y))
            self.BodySegments[Curr].z=TargetA
            self.BodySegments[Curr].x+=math.cos(TargetA)*(TargetD-40)
            self.BodySegments[Curr].y+=math.sin(TargetA)*(TargetD-40)

        self.x+=self.vx
        self.y+=self.vy
        self.y=max(min(self.y,450),-50)
        self.x=max(min(self.x,950),-50)

        if(self.wavespawned+1 < CurrentWave):
            Turret_deleter.append(ID)

    def cool(self,ID):
        for Curr in Enemy_Array:
            if(self.x-25<=Curr.x+50 and self.x+25>=Curr.x and self.y-25<=Curr.y+50 and self.y+25>=Curr.y):
                Curr.hurtMePlenty(1)
        #OUCH
        for Rruc in self.BodySegments:
            for Curr in Enemy_Array:
                if(Rruc.x-25<=Curr.x+50 and Rruc.x+25>=Curr.x and Rruc.y-25<=Curr.y+50 and Rruc.y+25>=Curr.y):
                    Curr.hurtMePlenty(1)

    def draw_Turret(self,background,win):
        #pygame.draw.rect(background,Color(255,0,255),((self.x,self.y),(50,50)))
        #background.blit(Calamity_tex, (self.x, self.y))
        
        for Curr in range(len(self.BodySegments)-1):
            rotated_image = pygame.transform.rotate(textures.Body_Destroyer_tex,-self.BodySegments[Curr].z/math.pi*180)
            new_rect = rotated_image.get_rect(center = textures.Body_Destroyer_tex.get_rect(topleft = (self.BodySegments[Curr].x,self.BodySegments[Curr].y)).center)
            background.blit(rotated_image, new_rect)

        lastIndex = len(self.BodySegments)-1
        rotated_image = pygame.transform.rotate(textures.Tail_Destroyer_tex,-self.BodySegments[lastIndex].z/math.pi*180)
        new_rect = rotated_image.get_rect(center = textures.Tail_Destroyer_tex.get_rect(topleft = (self.BodySegments[lastIndex].x,self.BodySegments[lastIndex].y)).center)
        background.blit(rotated_image, new_rect)

        rotated_image = pygame.transform.rotate(textures.Head_Destroyer_tex,-self.r/math.pi*180)
        new_rect = rotated_image.get_rect(center = textures.Head_Destroyer_tex.get_rect(topleft = (self.x,self.y)).center)
        background.blit(rotated_image, new_rect)

        self.DrawMods(background)

        return background

    def draw_Range(self,background,win):
        return background

class Sniper_TF2(Base_Turret):
    cooldown=0
    MaxCooldown=150
    range=600
    mode = "first"
    dmg = 30

    def math_Turret(self,ID):#ID is a method that i use so i can find where this actor is the array for later removal
        #why the self.?
        self.MathMods(ID)
        Enemy_ID = self.findClosestEnemy(ID)
        if(Enemy_ID>=0):
          self.r=math.atan2(Enemy_Array[Enemy_ID].y-self.y,Enemy_Array[Enemy_ID].x-self.x)
        if(self.cooldown>0):
            self.cooldown-=self.cooldownMuiltplier
        if(Enemy_ID>=0 and self.cooldown<=0):
            self.Attack_Enemy(Enemy_ID,self.dmg*self.damageMuiltplier)
            Effect.makePartic(Effect.Sniper_Tracer(self.x+25,self.y+25,Enemy_Array[Enemy_ID].x+25,Enemy_Array[Enemy_ID].y+25))

        global WaveHardener
        global CurrentWave
        self.dmg = 30 *(1+WaveHardener*CurrentWave*CurrentWave)
    
    def draw_Turret(self,background,win):
        background.blit(textures.Sniper_base_tex, (self.x,self.y))
        rotated_image = pygame.transform.rotate(textures.Sniper_Turret_tex,-self.r/math.pi*180)
        new_rect = rotated_image.get_rect(center = textures.Sniper_Turret_tex.get_rect(topleft = (self.x,self.y)).center)
        background.blit(rotated_image, new_rect)
        background.blit(textures.Sniper_base2_tex, (self.x,self.y))
        self.DrawMods(background)
        #pygame.draw.rect(background,Color(0,255,0),((self.x,self.y),(50,50)))
        #pygame.draw.line(background,Color(0,200,0),(self.x+25,self.y+25),(self.x+25+math.cos(self.r)*25,self.y+25+math.sin(self.r)*25))
        #alpha channel not working
        #dont know why
        return background

class Slower(Base_Turret):
    MaxCooldown = 1
    dmg = 4
    range = 1
    spin=0

    def math_Turret(self,ID):
        self.MathMods(ID)
        global Enemy_Array
        if(self.cooldown>0):
            self.cooldown-=self.cooldownMuiltplier
        else:
            self.cooldown = self.MaxCooldown
            for Curr in range(len(Enemy_Array)):
                if(self.x - 75 <= Enemy_Array[Curr].x and self.x + 75 >= Enemy_Array[Curr].x and self.y - 75 <= Enemy_Array[Curr].y and self.y + 75 >= Enemy_Array[Curr].y):
                    MODENEMY(Curr,BrainHurt())
    
    def draw_Turret(self,background,win):
        background.blit(textures.Jojo_Turret_tex, (self.x,self.y))
        #pygame.draw.rect(background,Color(0,255,255),((self.x,self.y),(50,50)))
        self.DrawMods(background)
        #alpha channel not working
        #dont know why
        return background


    def draw_Range(self,background,win):
        self.spin+=0.005
        smoke = pygame.transform.rotate(textures.Jojo_Smoke_tex, math.degrees(self.spin))
        smoke_sqr = smoke.get_rect()
        smoke_sqr.center = (self.x+25, self.y+25)

        background.blit(smoke,smoke_sqr)
        return background

class Stonker(Base_Turret):
    MaxCooldown = 1
    dmg = 0
    range = 1

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.wavespawned=CurrentWave

    def math_Turret(self,ID):
        global WORKAROUND
        if(self.wavespawned!=CurrentWave):
            WORKAROUND+=1
            self.wavespawned=CurrentWave
    
    def draw_Turret(self,background,win):
        background.blit(textures.Slower_tex, (self.x,self.y))
        #pygame.draw.rect(background,Color(0,255,255),((self.x,self.y),(50,50)))
        self.DrawMods(background)
        #alpha channel not working
        #dont know why
        return background

    def draw_Range(self,background,win):
        #pygame.draw.rect(background,Color(200,200,200,100),((self.x-50,self.y-50),(150,150)),2)
        return background

class Tachanka(Base_Turret):
    cooldown=0
    MaxCooldown=200
    Reveup=0
    range=300
    mode = "first"
    dmg = 5

    def math_Turret(self,ID):#ID is a method that i use so i can find where this actor is the array for later removal
        #why the self.?
        self.MathMods(ID)
        Enemy_ID = self.findClosestEnemy(ID)
        if(Enemy_ID>=0):
            self.r=math.atan2(Enemy_Array[Enemy_ID].y-self.y,Enemy_Array[Enemy_ID].x-self.x)
            self.Reveup=min(self.Reveup+0.6,400)
        else:
            self.Reveup=max(self.Reveup-0.8,0)
        if(self.cooldown>0):
            self.cooldown-=self.cooldownMuiltplier*(1 + self.Reveup / 25)
        if(Enemy_ID>=0 and self.cooldown<=0):
            self.Attack_Enemy(Enemy_ID,self.dmg*self.damageMuiltplier)
            Effect.makePartic(Effect.Sniper_Tracer(self.x+25,self.y+25,Enemy_Array[Enemy_ID].x+25,Enemy_Array[Enemy_ID].y+25))
    
    def draw_Turret(self,background,win):
        background.blit(textures.Lordy_Tachanka_Base, (self.x,self.y))
        rotated_image = pygame.transform.rotate(textures.Lordy_Tachanka_Upper,-self.r/math.pi*180)
        new_rect = rotated_image.get_rect(center = textures.Lordy_Tachanka_Upper.get_rect(topleft = (self.x,self.y)).center)
        background.blit(rotated_image, new_rect)
        self.DrawMods(background)
        #pygame.draw.rect(background,Color(0,255,0),((self.x,self.y),(50,50)))
        #pygame.draw.line(background,Color(0,200,0),(self.x+25,self.y+25),(self.x+25+math.cos(self.r)*25,self.y+25+math.sin(self.r)*25))
        #alpha channel not working
        #dont know why
        return background

class PapaBento(Base_Turret):
    cooldown=0
    MaxCooldown=200
    Reveup=0
    range=300
    mode = "first"
    level = 0

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.MODS=[]
        self.level=1
        for X in range(len(Turret_Array)):
            dist = math.dist((Turret_Array[X].x,Turret_Array[X].y),(self.x,self.y))
            if(dist<self.range):
                Turret_deleter.append(X)
                self.level+=1
        print(self.level)
    
    def math_Turret(self,ID):#ID is a method that i use so i can find where this actor is the array for later removal
        #why the self.?
        self.MathMods(ID)
        Enemy_ID = self.findClosestEnemy(ID)
        if(Enemy_ID>=0):
            self.r=math.atan2(Enemy_Array[Enemy_ID].y-self.y,Enemy_Array[Enemy_ID].x-self.x)
            self.Reveup=min(self.Reveup+0.4,400)
            print(self.Reveup)
        else:
            self.Reveup=max(self.Reveup-0.4,0)
        if(self.cooldown>0):
            self.cooldown-=self.cooldownMuiltplier*(1 + self.Reveup / 25)
        if(Enemy_ID>=0 and self.cooldown<=0):
            self.Attack_Enemy(Enemy_ID,self.dmg*self.damageMuiltplier)
            Effect.makePartic(Effect.Sniper_Tracer(self.x+25,self.y+25,Enemy_Array[Enemy_ID].x+25,Enemy_Array[Enemy_ID].y+25))
    
    def draw_Turret(self,background,win):
        background.blit(textures.Sniper_base_tex, (self.x,self.y))
        rotated_image = pygame.transform.rotate(textures.tankanc_tex,-self.r/math.pi*180)
        new_rect = rotated_image.get_rect(center = textures.tankanc_tex.get_rect(topleft = (self.x,self.y)).center)
        background.blit(rotated_image, new_rect)
        self.DrawMods(background)
        #pygame.draw.rect(background,Color(0,255,0),((self.x,self.y),(50,50)))
        #pygame.draw.line(background,Color(0,200,0),(self.x+25,self.y+25),(self.x+25+math.cos(self.r)*25,self.y+25+math.sin(self.r)*25))
        #alpha channel not working
        #dont know why
        return background

WORKAROUND = 0

class PROJ:
    x=0
    y=0
    vx=0
    vy=0
    w=0
    h=0
    dmg=0
    pierce=0

    def onColl(self,EnemyID):
        pass

    def draw(self,background,win):
        pygame.draw.rect(background,Color(255,0,0),((self.x+25-self.w/2,self.y+25-self.h/2),(self.w,self.h)))
        return background

    def math(self,ID):
        self.x+=self.vx
        self.y+=self.vy
        self.cool(ID)
        if(self.x<-25 or self.x>900-25 or self.y<-25 or self.y>600-25):
            PROJ_deleter.append(ID)

    def cool(self,ID):
        for i in range(len(Enemy_Array)):
            Curr = Enemy_Array[i]
            if(self.x-self.w/4<=Curr.x+50 and self.x+self.w/4>=Curr.x and self.y-self.h/4<=Curr.y+50 and self.y+self.h/4>=Curr.y):
                Curr.hurtMePlenty(self.dmg)
                self.onColl(i)
                if(self.pierce!=-414):
                    self.pierce-=1
                    if(self.pierce<0):
                        PROJ_deleter.append(ID)
                        return

class Dart(PROJ):
    pierce=-414
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=25
        self.h=25
        self.dmg=0.5

class FireBall(PROJ):
    pierce=-414
    r=0
    life=200
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=50
        self.h=50
        self.dmg=0.1#too much dps

    def math(self,ID):
        self.r+=5
        global Enemy_Array
        Enemy_ID=-1
        if(len(Enemy_Array)>0):
            min_dist=9999999#big
            for Curr in range(len(Enemy_Array)):
                tmpEnemy = Enemy_Array[Curr]
                dist = math.dist((self.x,self.y),(tmpEnemy.x,tmpEnemy.y))
                if(dist<min_dist):
                    min_dist=dist
                    Enemy_ID=Curr
        if(Enemy_ID>=0):
            dirction = math.atan2(Enemy_Array[Enemy_ID].y-self.y,Enemy_Array[Enemy_ID].x-self.x)
            self.vx+=math.cos(dirction)
            self.vy+=math.sin(dirction)
        self.vx=self.vx/50*49
        self.vy=self.vy/50*49
        self.x+=self.vx
        self.y+=self.vy
        self.cool(ID)
        self.life-=1
        if(self.life<=0):
            PROJ_deleter.append(ID)
    
    def draw(self,background,win):
        rotated_image, rect = textures.rsImage(textures.FireBall_tex,self.r,(self.x+25,self.y+25),pygame.Vector2(0,0),(60,60))
        background.blit(rotated_image, rect)
        return background

class Brimstone(PROJ):
    pierce=-414
    r=0
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=8
        self.h=8
        self.dmg=1
        self.r=math.atan2(vy,vx)

    def draw(self,background,win):
        #pygame.draw.rect(background,Color(255,0,0),((self.x,self.y),(50,50)))
        #rotated_image = pygame.transform.rotate(Brimstone_tex,-self.r/math.pi*180)
        #new_rect = rotated_image.get_rect(center = Brimstone_tex.get_rect(topleft  = (self.x+math.cos(self.r),self.y)).center)
        rotated_image, rect = textures.rsImage(textures.Brimstone_tex,self.r/math.pi*180,(self.x+25,self.y+25),pygame.Vector2(-16,0),(32,15))
        background.blit(rotated_image, rect)
        return background

class SBrimstone(PROJ):
    pierce=-414
    r=0
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=16
        self.h=16
        self.dmg=1
        self.r=math.atan2(vy,vx)

    def onColl(self,ID):
        MODENEMY(ID,Melting())

    def draw(self,background,win):
        #pygame.draw.rect(background,Color(255,0,0),((self.x,self.y),(50,50)))
        #rotated_image = pygame.transform.rotate(Brimstone_tex,-self.r/math.pi*180)
        #new_rect = rotated_image.get_rect(center = Brimstone_tex.get_rect(topleft  = (self.x+math.cos(self.r),self.y)).center)
        rotated_image, rect = textures.rsImage(textures.SBrimstone_tex,self.r/math.pi*180,(self.x+25,self.y+25),pygame.Vector2(-16,0),(40,23))
        background.blit(rotated_image, rect)
        return background

class HyperDriveCore(PROJ):

    life=600

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vx=0
        self.vy=0
        self.w=0
        self.h=0
        self.dmg=0
        self.life=200

    def math(self,ID):
        self.life-=1
        global Turret_Array
        for X in range(len(Turret_Array)):
            Curr=Turret_Array[X]
            if(math.dist((self.x,self.y),(Curr.x+25,Curr.y+25))<150):
                #Curr.cooldown=math.floor(Curr.cooldown/2)
                #Curr.cooldown=0
                MODTURRET(X,Hyper())
                Effect.makePartic(Effect.Tracer(self.x,self.y,Curr.x+25,Curr.y+25))
        if(self.life==0):
            PROJ_deleter.append(ID)

    def draw(self,background,win):
        pygame.draw.circle(background,Color(int(255*self.life/200),int(255*self.life/200),int(255*self.life/200)),(self.x,self.y),20)
        rotated_image = pygame.transform.rotate(textures.HyperDriveCore_tex,self.life/200*360)
        new_rect = rotated_image.get_rect(center = textures.HyperDriveCore_tex.get_rect(topleft = (self.x-25+random.random()*4-2,self.y-25+random.random()*4-2)).center)
        background.blit(rotated_image, new_rect)
        return background

class CocaColaEspuma(PROJ):
    pierce=-414
    timer = 60
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=0
        self.h=0
        self.dmg=5

    def draw(self,background,win):
        if(self.timer<20):
            background.blit(textures.Coca_cola_Espuma_2, (self.x-25,self.y-25))
        elif(self.timer<40):
            background.blit(textures.Coca_cola_Espuma_1, (self.x-25,self.y-25))
        else:
            background.blit(textures.Coca_cola_Espuma_0, (self.x-25,self.y-25))
        #pygame.draw.rect(background,Color(255,0,0),((self.x+25-self.w/2,self.y+25-self.h/2),(self.w,self.h)))
        return background

    def math(self,ID):
        self.timer-=1
        if(self.timer==0):
            PROJ_deleter.append(ID)
            Effect.makePartic(Effect.espuma(self.x,self.y))
            for Curr in range(len(Enemy_Array)):
                tmpEnemy = Enemy_Array[Curr]
                dist = math.sqrt((self.x-25-tmpEnemy.x)**2+(self.y-25-tmpEnemy.y)**2)
                if(dist<150):
                    Enemy_Array[Curr].hurtMePlenty(50)

class Bolt(PROJ):
    pierce=15
    r=0
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=8
        self.h=8
        self.dmg=1
        self.r=math.atan2(vy,vx)

    def draw(self,background,win):
        rotated_image, rect = textures.rsImage(textures.Bolt_tex,self.r/math.pi*180,(self.x+25,self.y+25),pygame.Vector2(-16,0),(50,12))
        background.blit(rotated_image, rect)
        return background

class SplitShot(PROJ):
    pierce=-414
    r=0
    timer = 16
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=16
        self.h=16
        self.dmg=6
        self.r=math.atan2(vy,vx)

    def math(self,ID):
        self.x+=self.vx
        self.y+=self.vy
        self.cool(ID)
        self.timer-=1;
        if(self.timer==0):
            PROJ_deleter.append(ID)
            MakeProj(Bolt(self.x,self.y,math.cos(self.r)*8,math.sin(self.r)*10))
            for curr in range(6):
                rot = random.random()*math.pi/8-math.pi/16
                spe = random.random()*5+8
                MakeProj(Bolt(self.x,self.y,math.cos(self.r+rot)*spe,math.sin(self.r+rot)*spe))

    def draw(self,background,win):
        rotated_image, rect = textures.rsImage(textures.SplitShot_tex,self.r/math.pi*180,(self.x+25,self.y+25),pygame.Vector2(-16,0),(50,26))
        background.blit(rotated_image, rect)
        return background

class Aura(PROJ):
    pierce=-414
    r=0
    timer = 400
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=0
        self.h=0
        self.dmg=0
        self.r=math.atan2(vy,vx)

    def math(self,ID):
        self.r+=5
        global Enemy_Array
        Enemy_ID=-1
        if(len(Enemy_Array)>0):
            min_dist=9999999#big
            for Curr in range(len(Enemy_Array)):
                tmpEnemy = Enemy_Array[Curr]
                dist = math.dist((self.x,self.y),(tmpEnemy.x,tmpEnemy.y))
                if(dist<min_dist):
                    min_dist=dist
                    Enemy_ID=Curr
        if(Enemy_ID>=0):
            dirction = math.atan2(Enemy_Array[Enemy_ID].y-self.y,Enemy_Array[Enemy_ID].x-self.x)
            self.vx+=math.cos(dirction)*0.2
            self.vy+=math.sin(dirction)*0.2
        self.vx=self.vx/30*29
        self.vy=self.vy/30*29
        self.x+=self.vx
        self.y+=self.vy
        self.timer-=1
        for Curr in range(len(Enemy_Array)):
            tmpEnemy = Enemy_Array[Curr]
            dist = math.dist((self.x,self.y),(tmpEnemy.x,tmpEnemy.y))
            if(dist<150):
                Effect.makePartic(Effect.Tracer(self.x+25,self.y+25,tmpEnemy.x+25,tmpEnemy.y+25))
                tmpEnemy.hurtMePlenty(0.6)
        if(self.timer<=0):
            PROJ_deleter.append(ID)

    def draw(self,background,win):
        background.blit(textures.Aura_tex, (self.x,self.y))
        return background

class CARTIME(PROJ):
    pierce=-414
    timer = 400
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.w=50
        self.h=50
        self.dmg=6
        self.r=math.atan2(vy,vx)

    def onColl(self, EnemyID):
        MODENEMY(EnemyID,RunOver())

    def draw(self,background,win):
        #background.blit(CAR_tex, (self.x,self.y))
        rotated_image = pygame.transform.rotate(textures.CAR_tex,self.y/2)
        new_rect = rotated_image.get_rect(center = textures.CAR_tex.get_rect(topleft = (self.x,self.y)).center)
        background.blit(rotated_image, new_rect)
        return background

#never make this
class TowerMOD:
    IsBuff=False
    cooldownMuiltplier=1
    rangeMuiltplier=1
    damageMuiltplier=1
    timer=1
    #different aproch to deleting stuff in an array
    delet=False
    def math(self,ID):
        self.ExtraEffect(ID)
        self.timer-=1
        if(self.timer==0):
            self.delet=True
    
    def ExtraEffect(self,TOWER):
        pass

    def draw(self,background,ID,x,y):
        return background
    
class Omega(TowerMOD):
    IsBuff=True
    cooldownMuiltplier=200
    rangeMuiltplier=2
    damageMuiltplier=0.1
    timer=360
    
    def draw(self,background,ID,x,y):
        background.blit(textures.testbuff_tex, (x+ID*25,y))
        return background

class Silence(TowerMOD):
    IsBuff=False
    cooldownMuiltplier=0
    rangeMuiltplier=0
    damageMuiltplier=1
    timer=180
    
    def draw(self,background,ID,x,y):
        background.blit(textures.silence_tex, (x+ID*25,y))
        return background

class Hyper(TowerMOD):
    IsBuff=True
    cooldownMuiltplier=6
    rangeMuiltplier=1
    damageMuiltplier=1.2
    timer=5
    
    def draw(self,background,ID,x,y):
        background.blit(textures.Hyper_tex, (x+ID*25,y))
        return background

class EnemyMOD:
    IsBuff=False
    speedMuiltplier=1 # can go negative!
    resistanceMuiltplier=1
    timer=1
    #different aproch to deleting stuff in an array
    delet=False
    def math(self,ID):
        self.ExtraEffect(ID)
        self.timer-=1
        if(self.timer==0):
            self.delet=True
    
    def ExtraEffect(self,ENEMY):
        pass

    def draw(self,background,ID,x,y):
        return background
    
class FEAR(EnemyMOD):
    IsBuff=False
    speedMuiltplier=-1.2 # can go negative!
    resistanceMuiltplier=1.2
    timer=300
    
    def draw(self,background,ID,x,y):
        background.blit(textures.FEAR_tex, (x+ID*25,y))
        return background

class Melting(EnemyMOD):
    IsBuff=False
    speedMuiltplier=0.8 # can go negative!
    resistanceMuiltplier=1
    timer=120
    
    def ExtraEffect(self, ENEMY):
        return Enemy_Array[ENEMY].hurtMePlenty(1)

    def draw(self,background,ID,x,y):
        background.blit(textures.Melting_tex, (x+ID*25,y))
        return background

class RunOver(EnemyMOD):
    IsBuff=False
    speedMuiltplier=0.2 # can go negative!
    resistanceMuiltplier=1.2
    timer=600

    def draw(self,background,ID,x,y):
        background.blit(textures.RunOver_tex, (x+ID*25,y))
        return background

class BrainHurt(EnemyMOD):
    IsBuff=False
    speedMuiltplier=0.4 # can go negative!
    resistanceMuiltplier=1.4
    timer=5

    def draw(self,background,ID,x,y):
        background.blit(textures.BrainHurt_tex, (x+ID*25,y))
        return background

class PROCTECT(EnemyMOD):
    IsBuff=True
    speedMuiltplier=0.9 # can go negative!
    resistanceMuiltplier=0
    timer=120

    def draw(self,background,ID,x,y):
        background.blit(textures.PROTECT_tex, (x+ID*25,y))
        return background

def MODTURRET(ID,MOD):
    miniDict = type(MOD)
    for curr in Turret_Array[ID].MODS:
        if(type(curr)==miniDict):
            curr.timer=MOD.timer
            return
    Turret_Array[ID].MODS.append(MOD)

def MODENEMY(ID,MOD):
    miniDict = type(MOD)
    for curr in Enemy_Array[ID].MODS:
        if(type(curr)==miniDict):
            curr.timer=MOD.timer
            return
    Enemy_Array[ID].MODS.append(MOD)

Turret_Array = []
Enemy_Array = []
PROJ_Array = []

Base_Healt = 500

def AI_math():
    #not the best but a method that works for me preaty well
    #math and drawing are seperated so that pausing should be easy to implement

    for Curr in range(len(Turret_Array)):
        Turret_Array[Curr].math_Turret(Curr)
        
    Turret_deleter.reverse()

    for Curr in Turret_deleter:
        Turret_Array.pop(Curr)

    Turret_deleter.clear()

    #not the best but a method that works for me preaty well
    for Curr in range(len(Enemy_Array)):
        Enemy_Array[Curr].math_Enemy(Curr)

    Enemy_deleter.reverse()

    for Curr in Enemy_deleter:
        Enemy_Array.pop(Curr)

    Enemy_deleter.clear()

    #stuff
    
    for Curr in range(len(PROJ_Array)):
        PROJ_Array[Curr].math(Curr)


    #stuff

    PROJ_deleter.reverse()

    for Curr in PROJ_deleter:
        try: PROJ_Array.pop(Curr)
        except: pass

    PROJ_deleter.clear()

def AI_draw(background,win):
    for Curr in Enemy_Array:
        background = Curr.draw_Enemy(background,win)

    for Curr in Turret_Array:
        background = Curr.draw_Range(background,win)

    for Curr in Turret_Array:
        background = Curr.draw_Turret(background,win)

    for Curr in PROJ_Array:
        background = Curr.draw(background,win)

    return background

def MakeEnemy(name):
    if(name == "Basic_Enemy"):
        Enemy_Array.append(Base_enemy())
    if(name == "Fast_Enemy"):
        Enemy_Array.append(Fast_enemy())
    if(name == "Fat_enemy"):
        Enemy_Array.append(Fat_enemy())
    if(name == "Disabler_enemy"):
        Enemy_Array.append(Disabler_enemy())
    if(name == "Shilder_enemy"):
        Enemy_Array.append(Shilder_enemy())
    if(name == "Digoo"):
        Enemy_Array.append(Digoo())

def MakeProj(proj):
    #this desciption might be usefull
    PROJ_Array.append(proj)

def MakeTurret(x,y,name):
    Turret_Array.append(GetTurret(x,y,name))

def GetTurret(x,y,name):
    if(name=="Base_Turret"):
        return Base_Turret(x,y)
    if(name=="IceTurret"):
        return IceTurret(x,y)
    if(name=="Altar"):
        return Altar(x,y)
    if(name=="Darter"):
        return Darter(x,y)
    if(name=="Calamity"):
        return Calamity(x,y)
    if(name=="Yharon"):
        return Yharon(x,y)
    if(name=="Destroyer"):
        return Destroyer(x,y)
    if(name=="SCalamity"):
        return SCalamity(x,y)
    if(name=="Sniper_TF2"):
        return Sniper_TF2(x,y)
    if(name=="Slower"):
        return Slower(x,y)
    if(name=="Stonker"):
        return Stonker(x,y)
    if(name=="Tachanka"):
        return Tachanka(x,y)
    if(name=="PapaBento"):
        return PapaBento(x,y)

def hurtBase(dmg):
    global Base_Healt
    Base_Healt -= dmg