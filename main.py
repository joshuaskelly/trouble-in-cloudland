#!/usr/bin/python
import pygame
import settings
import game
import utility
import text
import menu
import scene
import splashScreen

import world
import player
import bullet
import baake
import balloon
import gem
import moono
import batto
import rokubi
import haoya
import yurei
import bokko
import hakta
import raayu
import paajo
import boss
import particle
import credits
import vector

from settings import *
from pygame.locals import *

pygame.init()

from utility import *

readSettings()

if settingList[SETTING_FULLSCREEN]:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
pygame.display.set_icon(utility.loadImage("icon"))
pygame.display.set_caption("Trouble In CloudLand v1.1")

screen.fill([0,0,0])
tempText = text.Text(FONT_PATH, 36, [255,255,255])
tempText.setText("Loading...")
tempText.position = vector.vector2d((SCREEN_WIDTH / 2) - (tempText.image.get_width() / 2), (SCREEN_HEIGHT / 2) - (tempText.image.get_height() / 2))
tempText.update()
tempText.draw(screen)
pygame.display.flip()

try:
    pygame.mixer.set_reserved(MUSIC_CHANNEL)
    pygame.mixer.Channel(MUSIC_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(PLAYER_CHANNEL)
    pygame.mixer.Channel(PLAYER_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(OW_CHANNEL)
    pygame.mixer.Channel(OW_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(BAAKE_CHANNEL)
    pygame.mixer.Channel(BAAKE_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(BOSS_CHANNEL)
    pygame.mixer.Channel(BOSS_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(PICKUP_CHANNEL)
    pygame.mixer.Channel(PICKUP_CHANNEL).set_volume(1)
except:
    utility.soundActive = False
    print "WARNING! - Sound not initialized."


from game import Game



pygame.mouse.set_visible(False)
musicList = [utility.loadSound("menuMusic"),utility.loadSound("music0"),utility.loadSound("music1"),utility.loadSound("music2"),utility.loadSound("bossMusic")]

world.loadData()
player.loadData()
bullet.loadData()
pygame.event.pump()
baake.loadData()
balloon.loadData()
gem.loadData()
pygame.event.pump()
moono.loadData()
batto.loadData()
rokubi.loadData()
pygame.event.pump()
haoya.loadData()
yurei.loadData()
bokko.loadData()
pygame.event.pump()
hakta.loadData()
raayu.loadData()
paajo.loadData()
pygame.event.pump()
boss.loadData()
particle.loadData()
menu.loadData()


for event in pygame.event.get():
    pass

splashScreen.SplashScreen(screen,"pygamesplash")
utility.playMusic(musicList[MENU_MUSIC])
splashScreen.SplashScreen(screen,"gameSplash")

if settingList[WORLD_UNLOCKED] == 0:
    newScene = scene.tutorialScene()
elif settingList[WORLD_UNLOCKED] == 1:
    newScene = scene.forestScene()
elif settingList[WORLD_UNLOCKED] == 2:
    newScene = scene.rockyScene()
elif settingList[WORLD_UNLOCKED] == 3:
    newScene = scene.pinkScene() 

try:
    import psyco
    psyco.full()
except:
    print "Warning: Psyco module not installed!"
    print "Continuing happily..."

gameIsRunning = True

mainMenuDictionary = {START_GAME:["Play","Start a New Game"],
                      OPTION_MENU:["Options","Change Sound and Video Options"],
                      CREDIT_MENU:["Credits","Who We Are, What We Did"],
                      EXIT_GAME:["Exit","Exit the Game"]}

worldMenuDictionary = {TUTORIAL:["Tutorial", "Start the Tutorial [Learn]"],
                       WORLD1:["Cloudopolis","Start Playing Cloudopolis [Apprentice]"],
                       WORLD2:["Nightmaria","Start Playing Nightmaria [Journeyman]"],
                       WORLD3:["Opulent Dream","Start Playing Opulent Dream [Master]"],
                       EXIT_OPTIONS:["Back","Go Back to the Main Menu"]}

optionMenuDictionary = {SOUND_MENU:["Sound Options", "Change Sound Options"],
                        DISPLAY_MENU:["Video Options" ,"Change Video Options"],
                        CHANGE_SENSITIVITY:["Mouse Sensitivity: " + getSensitivity(settingList[SENSITIVITY]), "Change Mouse Sensitivity"],
                        EXIT_OPTIONS:["Back","Go Back to the Main Menu"]}

soundMenuDictionary = {TOGGLE_SFX:["Sound Effects: " + on(settingList[SFX]), "Turn " + on(not settingList[SFX]) + " Sound Effects"],
                        TOGGLE_MUSIC:["Music: " + on(settingList[MUSIC]),"Turn " + on(not settingList[MUSIC]) + " Music"],
                        EXIT_OPTIONS:["Back","Go Back to the Option Menu"]}

displayMenuDictionary = {TOGGLE_PARTICLES:["Particles: " + able(settingList[PARTICLES]), "Turn " + on(not settingList[PARTICLES]) + " Particle Effects"],
                        TOGGLE_FULLSCREEN:["Video Mode: " + getScreenMode(settingList[SETTING_FULLSCREEN]), "Switch To " + getScreenMode(not settingList[SETTING_FULLSCREEN]) + " Mode"],
                        EXIT_OPTIONS:["Back","Go Back to the Main Menu"]}

sensitivityMenuDictionary = {0:["Very Low", "Change Sensitivty to Very Low"],
                             1:["Low", "Change Sensitivty to Low"],
                             2:["Normal", "Change Sensitivty to Normal"],
                             3:["High", "Change Sensitivty to High"],
                             4:["Very High", "Change Sensitivty to Very High"],}

menuBounds = [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT]

while gameIsRunning:
    gameIsRunning = menu.Menu(screen,
                                musicList[MENU_MUSIC],
                                newScene,
                                menuBounds,
                                ["Trouble in Cloudland",80,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                mainMenuDictionary).displayMenu()

    if gameIsRunning == START_GAME:
        lastHighlighted = settingList[WORLD_UNLOCKED]
        worldResult = menu.Menu(screen,
                                 musicList[MENU_MUSIC],
                                 newScene,
                                 menuBounds,
                                 ["Choose a World",96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                 worldMenuDictionary,
                                 lastHighlighted).displayMenu()

        if worldResult == TUTORIAL:
            newGame = Game(screen,0,musicList).run()
        elif worldResult == EXIT_OPTIONS:
            worldResult = False
        elif worldResult != False:
            utility.fadeMusic()
            utility.playMusic(musicList[worldResult - 1], True)
            newGame =  Game(screen,worldResult - 1, musicList).run()

    elif gameIsRunning == OPTION_MENU:
        optionResult = True
        lastHighlighted = 0
        while optionResult:

            optionResult = menu.Menu(screen,
                                      musicList[MENU_MUSIC],
                                      newScene,
                                      menuBounds,
                                      ["Options",96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                      optionMenuDictionary,
                                      lastHighlighted).displayMenu()
            
            if optionResult == SOUND_MENU:
                soundResult = True
                lastHighLighted = 0
                while soundResult:
                    
                    soundResult = menu.Menu(screen,
                                            musicList[MENU_MUSIC],
                                            newScene,
                                            menuBounds,
                                            ["Sound Options",96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                            soundMenuDictionary,
                                            lastHighlighted).displayMenu()
                    
                    if soundResult == TOGGLE_SFX:
                        settingList[SFX] = not settingList[SFX]
                        lastHighlighted = 0
                    
                    elif soundResult == TOGGLE_MUSIC:
                        settingList[MUSIC] = not settingList[MUSIC]
                        if not settingList[MUSIC]:
                            pygame.mixer.Channel(MUSIC_CHANNEL).stop()
                        lastHighlighted = 1
                        
                    elif soundResult == EXIT_OPTIONS:
                        soundResult = False
                        
                    soundMenuDictionary = {TOGGLE_SFX:["Sound Effects: " + on(settingList[SFX]), "Turn " + on(not settingList[SFX]) + " Sound Effects"],
                        TOGGLE_MUSIC:["Music: " + on(settingList[MUSIC]),"Turn " + on(not settingList[MUSIC]) + " Music"],
                        EXIT_OPTIONS:["Back","Go Back to the Option Menu"]}
                        
            if optionResult == DISPLAY_MENU:
                displayResult = True
                lastHighlighted = 0
                while displayResult:
                    
                    displayResult = menu.Menu(screen,
                                            musicList[MENU_MUSIC],
                                            newScene,
                                            menuBounds,
                                            ["Video Options",96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                            displayMenuDictionary,
                                            lastHighlighted).displayMenu()           
            
                    if displayResult == TOGGLE_PARTICLES:
                        settingList[PARTICLES] = not settingList[PARTICLES]
                        lastHighlighted = 0
                        
                    elif displayResult == TOGGLE_FULLSCREEN:
                        settingList[SETTING_FULLSCREEN] = not settingList[SETTING_FULLSCREEN]
                        lastHighlighted = 1
                        pygame.mixer.quit()
                        pygame.mixer.init()
                        
                        if settingList[SETTING_FULLSCREEN]:
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                            
                        pygame.mouse.set_visible(False)
                    
                    elif displayResult == EXIT_OPTIONS:
                        displayResult = False
                        
                    displayMenuDictionary = {TOGGLE_PARTICLES:["Particles: " + able(settingList[PARTICLES]), "Turn " + on(not settingList[PARTICLES]) + " Particle Effects"],
                                                TOGGLE_FULLSCREEN:["Video Mode: " + getScreenMode(settingList[SETTING_FULLSCREEN]), "Switch To " + getScreenMode(not settingList[SETTING_FULLSCREEN]) + " Mode"],
                                                EXIT_OPTIONS:["Back","Go Back to the Main Menu"]}
            
            elif optionResult == EXIT_OPTIONS:
                optionResult = False
            
            elif optionResult == CHANGE_SENSITIVITY:
                sensitivityResult = True
                lastHighlighted = 0
                while sensitivityResult:
        
                    sensitivityResult = menu.Menu(screen,
                                              musicList[MENU_MUSIC],
                                              newScene,
                                              menuBounds,
                                              ["Mouse Sensitivity",96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                              sensitivityMenuDictionary,
                                              lastHighlighted).displayMenu()

                    if sensitivityResult == 0:
                        settingList[SENSITIVITY] = .5
                        
                    elif sensitivityResult == 1:
                        settingList[SENSITIVITY] = .75
                        sensitivityResult = False
                        
                    elif sensitivityResult == 2:
                        settingList[SENSITIVITY] = 1
                        sensitivityResult = False
                        
                    elif sensitivityResult == 3:
                        settingList[SENSITIVITY] = 1.25
                        sensitivityResult = False
                        
                    elif sensitivityResult == 4:
                        settingList[SENSITIVITY] = 1.5
                        sensitivityResult = False
    


            optionMenuDictionary = {SOUND_MENU:["Sound Options", "Change Sound Options"],
                                    DISPLAY_MENU:["Video Options" ,"Change Video Options"],
                                    CHANGE_SENSITIVITY:["Mouse Sensitivity: " + getSensitivity(settingList[SENSITIVITY]), "Change Mouse Sensitivity"],
                                    EXIT_OPTIONS:["Back","Go Back to the Main Menu"]}
            
    elif gameIsRunning == CREDIT_MENU:
        credits.Credits(screen, musicList[MENU_MUSIC])
        
    elif gameIsRunning == EXIT_GAME:
        gameIsRunning = False
        writeSettings()
    
    elif gameIsRunning == False:
        writeSettings()
        
splashScreen.SplashScreen(screen,"outroSplash")
quit()
