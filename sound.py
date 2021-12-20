import pygame
import os
import menu
import random

ch = 2
deathSound = ["deathSound1.wav","deathSound2.wav"]
music = ["Music1.mp3","Music2.mp3"]
overexdend = ["Overexdend.mp3"]
CLICK = "click.mp3"
PEW = "pew.mp3"

soundPlay = True
song = None

def soundCheckUp():
    global ch

    pygame.mixer.Channel(ch).set_volume(menu.Sound_Effects)
    pygame.mixer.Channel(1).set_volume(menu.Sound_Effects)

    if menu.menuPause: pygame.mixer.pause()
    else: pygame.mixer.unpause()

    if(soundPlay):
        if not pygame.mixer.Channel(1).get_busy() and menu.gaming:
            if menu.Overexdednd_enabled:
                song = pygame.mixer.Sound(os.path.join("sound_effect", overexdend[0]))
                pygame.mixer.Channel(1).play(song)
            else:
                rand = random.randint(0,1)
                song = pygame.mixer.Sound(os.path.join("sound_effect", music[rand]))
                pygame.mixer.Channel(1).play(song)
    else:
        pygame.mixer.Channel(1).pause()

def get(name):
    global ch

    if(not soundPlay): 
        return

    sound = pygame.mixer.Sound(os.path.join("sound_effect", name))

    if name == CLICK:
        sound.set_volume(5)

    pygame.mixer.Channel(ch).play(sound)

    ch += 1
    if ch >= 99:
        ch = 2
