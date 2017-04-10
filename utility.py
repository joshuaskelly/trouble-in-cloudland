import os
import sys
import pygame

from settings import *

sound_active = True

def makeBool(value):
    if value == "True" or value == "True\n" or value == "1" or value == 1 or value == "T" or value == "t":
        return True
    else:
        return False

def read_high_scores():
    scoreList = []
    try:
        scoreFile = open(getPath() + "/score.bzd",'r')
        scoreList.append(int(scoreFile.readline()))
        scoreList.append(int(scoreFile.readline()))
        scoreList.append(int(scoreFile.readline()))
        scoreList.append(int(scoreFile.readline()))
        scoreFile.close()

        return scoreList
    
    except:
        scoreFile = open(getPath() + "/score.bzd",'w')
        scoreFile.write(str(0) + '\n')
        scoreFile.write(str(0) + '\n')
        scoreFile.write(str(0) + '\n')
        scoreFile.write(str(0) + '\n')
        scoreFile.close()
        
        return [0,0,0,0]

def write_high_scores((tutorial,world1,world2,world3)):
    scoreFile = open(getPath() + "/score.bzd",'w')
    scoreFile.write(str(tutorial) + '\n')
    scoreFile.write(str(world1) + '\n')
    scoreFile.write(str(world2) + '\n')
    scoreFile.write(str(world3) + '\n')
    scoreFile.close()

def read_settings():
    tempList = []
    try:
        settingsFile = open(getPath() + "/settings.bzd",'r')
        tempList.append(makeBool(settingsFile.readline()))
        tempList.append(makeBool(settingsFile.readline()))
        tempList.append(makeBool(settingsFile.readline()))
        tempList.append(int(settingsFile.readline()))
        tempList.append(float(settingsFile.readline()))
        tempList.append(makeBool(settingsFile.readline()))
        settingsFile.close()
        
        for setting in tempList:
            settings_list.append(setting)

    except:
        tempList = []
        print "Missing or Corrupted File:  Restoring Defaults"
        tempList = [True,True,True,0,1,True]

        for setting in tempList:
            settings_list.append(setting)

        writeSettings()

def writeSettings():
    settingsFile = open(getPath() + "/settings.bzd",'w')
    for element in settings_list:
        settingsFile.write(str(element) + '\n')

def able(value):
    if value:
        return "Enabled"
    else:
        return "Disabled"
    
def on(value):
    if value:
        return "On"
    else:
        return "Off"    
    
def get_sensitivity(value):
    if value == .5:
        return "Very Low"
    elif value == .75:
        return "Low"
    elif value == 1:
        return "Normal"
    elif value == 1.25:
        return "High"
    elif value == 1.5:
        return "Very High"
    
def get_screen_mode(value):
    if value and not sys.platform.startswith('darwin'):
        return "Fullscreen"
    else:
        return "Windowed"

def getPath():
    """This figures out the 'home' path. Useful for 
    storing config/save stuff."""
    
    pathname = ""
    try:
        pathname = os.environ["HOME"] + "/.battlezero"
    except:
        try:
            pathname = os.environ["APPDATA"] + "/battlezero"
        except:
            print "Could not get environment variable for home directory"
            pathname = "."
    if not os.path.exists(pathname):
        os.mkdir(pathname)
    return pathname

def loadImage(name):
    filepath = "data/images/" + name + ".bzi"

    if os.path.isfile(filepath):
        return pygame.image.load(filepath).convert_alpha()
    else:
        filepath = "data/images/" + name + ".png"
    
    return pygame.image.load(filepath).convert_alpha()


def loadSound(name):
    filepath = "data/sounds/" + name + ".bza"

    if os.path.isfile(filepath):
        return pygame.mixer.Sound(filepath)
    else:
        filepath = "data/sounds/" + name + ".ogg"

    return pygame.mixer.Sound(filepath)


def play_sound(sound, channelNumber = None):
    if settings_list[SFX] and sound_active:
        if channelNumber:
            pygame.mixer.Channel(channelNumber).play(sound)
        else:
            sound.play()

def play_music(music, forceNext = True):
    if settings_list[MUSIC] and sound_active:
        if forceNext:
            pygame.mixer.Channel(MUSIC_CHANNEL).queue(music)
        elif not pygame.mixer.Channel(MUSIC_CHANNEL).get_queue():
            pygame.mixer.Channel(MUSIC_CHANNEL).queue(music)

def fade_music():
    if sound_active: pygame.mixer.Channel(MUSIC_CHANNEL).fadeout(2000)

def dim(dimValue, colorValue = (0,0,0),):
    dim = pygame.Surface(pygame.display.get_surface().get_size())
    dim.fill(colorValue)
    dim.set_alpha(dimValue)
    pygame.display.get_surface().blit(dim,pygame.display.get_surface().get_rect())

def dimSurface(dimValue, colorValue = (0,0,0),):
    dim = pygame.Surface(pygame.display.get_surface().get_size())
    dim.fill(colorValue)
    dim.set_alpha(dimValue)
    return dim

def set_fullscreen(full=True):
    """Creates a display surface either full screen or windowed."""
    if full and not sys.platform.startswith('darwin'):
        return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
