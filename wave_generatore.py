import random
#'Basic_Enemy','Fast_Enemy','Fat_enemy','Disabler_enemy','Shilder_enemy'
#1,2,3,20,8
#enemy internal name
Enemies =           ['Basic_Enemy','Fast_Enemy','Fat_enemy','Disabler_enemy','Shilder_enemy']
#enemy dificulty
Enemies_Dificulty = [1            ,2           ,3          ,20              ,8]
#what wave they can start being used
Enemies_round =     [1            ,1           ,3          ,10              ,10]

EnabledEnemies = []
EnabledEnemies_Dificulty = []

Types = 2 #Change for different number of enemie types per wave

Enemies_in_Wave = []

def makeWave(wave):
    Wave_Power = 0
    #Enemies start appearing when?

    for I in range(len(Enemies_round)):
        if((wave-1)==Enemies_round[I]):
            EnabledEnemies.append(Enemies[I])
            EnabledEnemies_Dificulty.append(Enemies_Dificulty[I])

    Enemies_ID = [*range(len(EnabledEnemies))]

    #Boss waves
    if (wave == 20):
        Enemies_in_Wave.append('Digoo')

    else:
        Wave_Dificulty = wave * 3 + random.randint(2,4) #Change for different dificulties per wave
        Enemy_Types_in_Wave = random.choices (Enemies_ID , k=Types)
        while (Wave_Dificulty > Wave_Power):
            try:
                n = random.choice(Enemy_Types_in_Wave)
                if (Wave_Dificulty >= Wave_Power + EnabledEnemies_Dificulty[n]):
                    Wave_Power = Wave_Power + EnabledEnemies_Dificulty[n]
                    Enemies_in_Wave.append(EnabledEnemies[n])
                else:
                    Enemy_Types_in_Wave.remove(n)
            except:
                break

    if Enemies_in_Wave==[]:
        Enemies_in_Wave.append("Basic_Enemy")
    
    return Enemies_in_Wave