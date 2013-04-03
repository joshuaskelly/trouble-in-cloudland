import pygame
import sys
import settings
import actor
import text
import menu
import utility
import vector

import enemy
import player
import baake
import moono
import batto
import rokubi
import yurei
import bokko
import hakta
import raayu
import paajo
import haoya
import boss

import tutorial
import world
import scene
import bullet

import particle
import icon

import balloon
import gem

import credits

from utility import *
from pygame.locals import *

pauseMenuDictionary = {RESUME_GAME:["Resume","Continue Playing"],
                         OPTION_MENU:["Options","Change Sound and Video Options"],
                         EXIT_GAME:["Exit","Exit to the Main Menu"]}

class Game:

    def __init__(self, screen, worldToStart, musicList):
        self.screen = screen

        pygame.mouse.set_visible(False)

        self.done = False
        self.worldDone = False

        self.highScore = 0

        self.bulletGroup = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()
        self.powerupGroup = pygame.sprite.Group()
        self.bossGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.textGroup = pygame.sprite.Group()
        self.effectsGroup = pygame.sprite.Group()
        
        self.mouseLastMove = MOUSE_DEFAULT_POSITION

        self.groupList = [self.powerupGroup, self.enemyGroup, self.bossGroup,self.textGroup, self.effectsGroup]

        self.scoreBoard = text.Text(FONT_PATH, 36, FONT_COLOR)
        self.tempLifeBoard = text.Text(FONT_PATH, 36, FONT_COLOR)
        self.tempLifeBoard.position = vector.vector2d(48,40)
        self.lifeBoard = self.tempLifeBoard
        
        self.lifeIcon = icon.Icon("life")
        
        self.player = player.Player(self.bulletGroup, self.effectsGroup, self.lifeBoard, self.scoreBoard)
        
        self.playerGroup.add(self.player)
        self.textGroup.add(self.scoreBoard)
        self.textGroup.add(self.tempLifeBoard)
        self.textGroup.add(self.lifeIcon)

        self.musicList = musicList

        self.timer = pygame.time.Clock()

        """Get rid of the first mouse delta"""
        pygame.mouse.get_rel()

        world1_level0 = [[0,ACTOR_MOONO,45,0],
                         [1,ACTOR_MOONO,120,0],
                         [2,ACTOR_MOONO,240,0],
                         [3,ACTOR_BAAKE,-1,1],
                         [4,ACTOR_BOSS_TUT,-1,1],[4,ACTOR_MOONO,35,0]]
        world1_level1 = [[0,ACTOR_MOONO,40,0],
                         [1,ACTOR_MOONO,85,0],
                         [2,ACTOR_MOONO,110,0],
                         [3,ACTOR_BAAKE,-1,2],
                         [4,ACTOR_BOSS_TUT,-1,1],[4,ACTOR_MOONO,30,0]]
        world1_level2 = [[0,ACTOR_MOONO,30,0],
                         [1,ACTOR_BAAKE,-1,1],[0,ACTOR_MOONO,70,0],
                         [2,ACTOR_BAAKE,-1,1],[0,ACTOR_MOONO,130,0],
                         [3,ACTOR_BAAKE,-1,1],[0,ACTOR_MOONO,300,0],
                         [4,ACTOR_BOSS_TUT,-1,1],[4,ACTOR_MOONO,25,0]]
        world1_level3 = [[0,ACTOR_MOONO,25,0],
                         [1,ACTOR_BAAKE,-1,1],[1,ACTOR_MOONO,50,0],
                         [2,ACTOR_BAAKE,-1,2],[2,ACTOR_MOONO,110,0],
                         [3,ACTOR_BAAKE,-1,2],[3,ACTOR_MOONO,210,0],
                         [4,ACTOR_BOSS_TUT,-1,1],[4,ACTOR_MOONO,20,0]]

        world2_level0 = [[0,ACTOR_MOONO,45,0],[0,ACTOR_HAOYA,65,0],
                         [1,ACTOR_BAAKE,-1,1],[1,ACTOR_MOONO,70,0],
                         [2,ACTOR_HAOYA,75,0],
                         [3,ACTOR_MOONO,85,0],
                         [4,ACTOR_BAAKE_BOSS,-1,1],[4,ACTOR_HAOYA,30,0]]
        world2_level1 = [[0,ACTOR_BAAKE,-1,2], [0,ACTOR_BATTO,150,0],[0,ACTOR_MOONO,55,0],
                         [1,ACTOR_HAOYA,60,0],
                         [2,ACTOR_MOONO,100,0],
                         [3,ACTOR_BAAKE,-1,1],[3,ACTOR_BATTO,280,0],
                         [4,ACTOR_BAAKE_BOSS,-1,1],[4,ACTOR_BATTO,70,0]]
        world2_level2 = [[0,ACTOR_ROKUBI,60,0],[0,ACTOR_MOONO,50,0],[0,ACTOR_BAAKE,-1,2],
                         [1,ACTOR_BAAKE,-1,1],[1,ACTOR_BATTO,160,0],
                         [2,ACTOR_HAOYA,60,0],
                         [3,ACTOR_MOONO,80,0],
                         [4,ACTOR_BAAKE_BOSS,-1,1],[4,ACTOR_ROKUBI,30,0]]
        world2_level3 = [[0,ACTOR_HAOYA,60,0],[0,ACTOR_BATTO,170,0],[0,ACTOR_ROKUBI,75,0],[0,ACTOR_BAAKE,-1,1],
                         [1,ACTOR_MOONO,70,0],[1,ACTOR_BAAKE,-1,1],
                         [2,ACTOR_BAAKE,-1,1],[2,ACTOR_ROKUBI,180,1],
                         [3,ACTOR_MOONO,200,0],
                         [4,ACTOR_BAAKE_BOSS,-1,1],[4,ACTOR_HAOYA,100,0],[4,ACTOR_BATTO,240,0],[4,ACTOR_ROKUBI,90,0],[4,ACTOR_BAAKE,-1,1]]

        world3_level0 = [[0,ACTOR_HAKTA,35,0],[0,ACTOR_HAOYA,65,0],
                         [1,ACTOR_BOKKO,-1,1],
                         [2,ACTOR_BOKKO,-1,1],[2,ACTOR_HAKTA,75,0],
                         [3,ACTOR_BOKKO,-1,1],
                         [4,ACTOR_MOONO_BOSS,-1,1],[4,ACTOR_HAKTA,30,0]]
        world3_level1 = [[0,ACTOR_RAAYU,45,0],[0,ACTOR_HAKTA,50,0],
                         [1,ACTOR_BOKKO,-1,1],
                         [2,ACTOR_RAAYU,60,0],
                         [3,ACTOR_BOKKO,-1,1],[3,ACTOR_ROKUBI,80,0],
                         [4,ACTOR_MOONO_BOSS,-1,1],[4,ACTOR_RAAYU,25,0]]
        world3_level2 = [[0,ACTOR_PAAJO,95,0],[0,ACTOR_HAKTA,40,0],
                         [1,ACTOR_BOKKO,-1,2],
                         [2,ACTOR_RAAYU,80,0],
                         [3,ACTOR_BOKKO,-1,1],
                         [4,ACTOR_MOONO_BOSS,-1,1],[4,ACTOR_PAAJO,70,0]]
        world3_level3 = [[0,ACTOR_HAKTA,55,0],[0,ACTOR_RAAYU,75,0],[0,ACTOR_PAAJO,160,0],
                         [1,ACTOR_BOKKO,-1,2],[1,ACTOR_ROKUBI,50,0],
                         [2,ACTOR_HAOYA,120,0],
                         [3,ACTOR_BOKKO,-1,1],
                         [4,ACTOR_MOONO_BOSS,-1,1],[4,ACTOR_HAKTA,60,0],[4,ACTOR_RAAYU,50,0],[4,ACTOR_PAAJO,110,0],[4,ACTOR_BOKKO,-1,1]]
        
        tutorialWorld = ["Tutorial",self.player,self.groupList]
        tempWorld1 = ["Cloudopolis",self.player,self.groupList,[world1_level0,world1_level1,world1_level2,world1_level3]]
        tempWorld2 = ["Nightmaria",self.player,self.groupList,[world2_level0,world2_level1,world2_level2,world2_level3]]
        tempWorld3 = ["Opulent Dream",self.player,self.groupList,[world3_level0,world3_level1,world3_level2,world3_level3]]

        self.worldList = [tutorialWorld,tempWorld1,tempWorld2,tempWorld3]

        self.worldNumber = worldToStart

        if self.worldNumber == 0:
            self.currentWorld = tutorial.Tutorial(self.worldList[self.worldNumber])
        else:
            self.currentWorld = world.World(self.worldList[self.worldNumber],self.musicList[self.worldNumber])
            self.currentWorld.load()


        if self.worldNumber == 0:
            self.newScene = scene.tutorialScene()
            self.player.lives = 99
            self.lifeBoard.setText('x' + str(self.player.lives))
        elif self.worldNumber == 1:
            self.newScene = scene.forestScene()
        elif self.worldNumber == 2:
            self.newScene = scene.rockyScene()
        elif self.worldNumber == 3:
            self.newScene = scene.pinkScene()       


    
    def run(self):
        while not self.done:
            if self.worldDone:
                if self.worldNumber < MAX_WORLD:
                    self.worldBeat()

                    """Resetting player lives so that
                    it isn't in their best interest
                    to play easier worlds just to have
                    extra lives."""
                    self.player.lives = 3
                    self.player.lifeBoard.setText('x' + str(self.player.lives))
                    
                    self.player.score = 0
                    self.player.nextBonus = 50000

                    """Loading the new world"""
                    self.worldNumber += 1
                    
                    if self.worldNumber == 0:
                        self.newScene = scene.tutorialScene()
                    elif self.worldNumber == 1:
                        self.newScene = scene.forestScene()
                    elif self.worldNumber == 2:
                        self.newScene = scene.rockyScene()
                    elif self.worldNumber == 3:
                        self.newScene = scene.pinkScene()                     
                    
                    if self.worldNumber > settingList[WORLD_UNLOCKED]:
                        settingList[WORLD_UNLOCKED] = self.worldNumber
                    utility.playMusic(self.musicList[self.worldNumber],True)
                    self.currentWorld = world.World(self.worldList[self.worldNumber], self.musicList[self.worldNumber])
                    self.currentWorld.load()
                    self.worldDone = False
                        
                else:
                    self.gameBeat()

            self.checkCollision()
            self.update()
            self.draw()
            self.handleEvents()
            
            pygame.mouse.set_pos(MOUSE_DEFAULT_POSITION)
            pygame.mouse.get_rel()
            self.mouseLastMove = pygame.mouse.get_pos()
            
            self.timer.tick(FRAMES_PER_SECOND)
     
            if self.player.dead:
                highScore = readHighScores()

                if self.player.score < highScore[self.worldNumber]:
                    endGameDictionary = {HIGH_SCORE:["High Score For This World: " + str(highScore[self.worldNumber]), "You would need to score " + str(highScore[self.worldNumber] - self.player.score) + " more to beat it!"],
                                         NEXT_WORLD:["Exit","Return To The Menu"]} 
                elif self.player.score == highScore[self.worldNumber]:
                    endGameDictionary = {HIGH_SCORE:["High Score For This World: " + str(highScore[self.worldNumber]), "You Tied the High Score!"],
                                         NEXT_WORLD:["Exit","Return To The Menu"]}         
                else:
                    endGameDictionary = {HIGH_SCORE:["High Score For This World: " + str(highScore[self.worldNumber]), "You Beat the High Score!"],
                                         NEXT_WORLD:["Exit","Return To The Menu"]}

                    highScore[self.worldNumber] = self.player.score
                    writeHighScores(highScore)
                utility.dim(128,FILL_COLOR)
                endGameMenu = menu.Menu(self.screen,
                                        self.musicList[self.worldNumber],
                                        self.screen.convert(),
                                        [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                        ["Game Over",128,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                        endGameDictionary).displayMenu()

                self.done = True
                utility.fadeMusic()
                utility.playMusic(self.musicList[MENU_MUSIC], True)


    def handleEvents(self):
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == MOUSEBUTTONDOWN and event.button == 3) or (event.type == ACTIVEEVENT and event.gain == 0):
                utility.dim(128,FILL_COLOR)
                """takingScreenShot = True
                while takingScreenShot:
                    for shotEvent in pygame.event.get():
                        if (event.type == pygame.MOUSEBUTTONDOWN):
                            takingScreenShot = False"""

                screenGrab = self.screen.copy()
                
                pauseMenuRunning = True
                
                while pauseMenuRunning:
                    pauseMenu = menu.Menu(self.screen,
                                          self.musicList[self.worldNumber],
                                          screenGrab,
                                          [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                          ["Pause",128,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                          pauseMenuDictionary).displayMenu()
    
                    if pauseMenu == OPTION_MENU:
                        optionResult = True
                        lastHighlighted = 0
                        while optionResult:
    
                            optionMenuDictionary = {SOUND_MENU:["Sound Options", "Change Sound Options"],
                                                    DISPLAY_MENU:["Video Options" ,"Change Video Options"],
                                                    CHANGE_SENSITIVITY:["Mouse Sensitivity: " + getSensitivity(settingList[SENSITIVITY]), "Change Mouse Sensitivity"],
                                                    EXIT_OPTIONS:["Back","Go Back to the Main Menu"]}
    
                            sensitivityMenuDictionary = {0:["Very Low", "Change Sensitivty to Very Low"],
                                                         1:["Low", "Change Sensitivty to Low"],
                                                         2:["Normal", "Change Sensitivty to Normal"],
                                                         3:["High", "Change Sensitivty to High"],
                                                         4:["Very High", "Change Sensitivty to Very High"],}
                            
                            soundMenuDictionary = {TOGGLE_SFX:["Sound Effects: " + on(settingList[SFX]), "Turn " + on(not settingList[SFX]) + " Sound Effects"],
                                                    TOGGLE_MUSIC:["Music: " + on(settingList[MUSIC]),"Turn " + on(not settingList[MUSIC]) + " Music"],
                                                    EXIT_OPTIONS:["Back","Go Back to the Option Menu"]}
                            
                            displayMenuDictionary = {TOGGLE_PARTICLES:["Particles: " + able(settingList[PARTICLES]), "Turn " + on(not settingList[PARTICLES]) + " Particle Effects"],
                                                    TOGGLE_FULLSCREEN:["Video Mode: " + getScreenMode(settingList[SETTING_FULLSCREEN]), "Switch To " + getScreenMode(not settingList[SETTING_FULLSCREEN]) + " Mode"],
                                                    EXIT_OPTIONS:["Back","Go Back to the Main Menu"]}
    
                            optionResult = menu.Menu(self.screen,
                                                     self.musicList[self.worldNumber],
                                                     screenGrab,
                                                     [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                                     ["Options",96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                                     optionMenuDictionary,
                                                     lastHighlighted).displayMenu()
                            
                            if optionResult == SOUND_MENU:
                                soundResult = True
                                lastHighLighted = 0
                                while soundResult:
                                    
                                    soundResult = menu.Menu(self.screen,
                                                            self.musicList[self.worldNumber],
                                                            screenGrab,
                                                            [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
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
                                    
                                    displayResult = menu.Menu(self.screen,
                                                            self.musicList[self.worldNumber],
                                                            screenGrab,
                                                            [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
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
                        
                                    sensitivityResult = menu.Menu(self.screen,
                                                                self.musicList[self.worldNumber],
                                                                screenGrab,
                                                                [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
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
                                
                    elif pauseMenu == RESUME_GAME or pauseMenu == False:
                        pauseMenuRunning = False
                        pygame.mouse.get_rel()
    
                    elif pauseMenu == EXIT_GAME:
                       utility.fadeMusic()
                       utility.playMusic(self.musicList[MENU_MUSIC], True)
                       self.done = True
                       pauseMenuRunning = False
                                       
            elif event.type == MOUSEMOTION and self.player.lives:
                mousein = [pygame.mouse.get_pos()[0] - 512.0, pygame.mouse.get_pos()[1] - 384.0]
                if mousein[0] != 0 and mousein[1] != 0:
                    self.player.fire()
                    self.player.velocity = (self.player.velocity + mousein) / 1.5 * settingList[SENSITIVITY]
                    
                


    
    def draw(self):
        self.screen.fill(FILL_COLOR)
        self.newScene.draw(self.screen)
        self.effectsGroup.draw(self.screen)
        self.playerGroup.draw(self.screen)
        self.bulletGroup.draw(self.screen)
        self.powerupGroup.draw(self.screen)
        self.enemyGroup.draw(self.screen)
        self.bossGroup.draw(self.screen)
        self.textGroup.draw(self.screen)
        
        pygame.display.flip()
        
        
        
    def update(self):
        self.worldDone = self.currentWorld.update()
        self.enemyGroup.update()
        self.playerGroup.update()
        self.bulletGroup.update()
        self.powerupGroup.update()
        self.bossGroup.update()
        self.textGroup.update()
        self.effectsGroup.update()


        
    def checkCollision(self):
        if self.player.active:
            self.player.checkCollision(self.powerupGroup)
            self.player.checkCollision(self.enemyGroup)
            self.player.checkCollision(self.bossGroup)

        for boss in self.bossGroup:
            if boss.active:
                boss.checkCollision(self.bulletGroup)

        for enemy in self.enemyGroup:
            if enemy.active:
                enemy.checkCollision(self.powerupGroup)
                enemy.checkCollision(self.bulletGroup)



    def worldBeat(self):
        highScore = readHighScores()
        if self.player.score < highScore[self.worldNumber]:
            worldEndDictionary = {HIGH_SCORE:["High Score For This World: " +str(highScore[self.worldNumber]), "You would need to score " + str(highScore[self.worldNumber] - self.player.score) + " more to beat it!"],
                                  NEXT_WORLD:["Continue", "On to the Next World!"]} 
        elif self.player.score == highScore[self.worldNumber]:
            worldEndDictionary = {HIGH_SCORE:["High Score For This World: " + str(highScore[self.worldNumber]), "You Tied the High Score!"],
                                  NEXT_WORLD:["Continue", "On to the Next World!"]}         
        else:
            worldEndDictionary = {HIGH_SCORE:["High Score For This World: " + str(highScore[self.worldNumber]), "You Beat the High Score!"],
                                  NEXT_WORLD:["Continue", "On to the Next World!"]}         

            highScore[self.worldNumber] = self.player.score
            writeHighScores(highScore)

        utility.dim(128,FILL_COLOR)
        worldEndMenu = menu.Menu(self.screen,
                                 self.musicList[self.worldNumber],
                                 self.screen.convert(),
                                 [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                 ["World Defeated!",64,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                 worldEndDictionary).displayMenu()
         
        utility.fadeMusic()

    
    
    def gameBeat(self):
        highScore = readHighScores()
        if self.player.score < highScore[self.worldNumber]:
            worldEndDictionary = {HIGH_SCORE:["High Score For This World: " +str(highScore[self.worldNumber]), "You would need to score " + str(highScore[self.worldNumber] - self.player.score) + " more to beat it!"],
                                  NEXT_WORLD:["Credits", "On to the Credits!"]} 
        elif self.player.score == highScore[self.worldNumber]:
            worldEndDictionary = {HIGH_SCORE:["High Score For This World: " + str(highScore[self.worldNumber]), "You Tied the High Score!"],
                                  NEXT_WORLD:["Credits", "On to the Credits!"]}         
        else:
            worldEndDictionary = {HIGH_SCORE:["High Score For This World: " + str(highScore[self.worldNumber]), "You Beat the High Score!"],
                                  NEXT_WORLD:["Credits", "On to the Credits!"]}         

            highScore[self.worldNumber] = self.player.score
            writeHighScores(highScore)

        utility.dim(128,FILL_COLOR)
        worldEndMenu = menu.Menu(self.screen,
                                 self.musicList[self.worldNumber],
                                 self.screen.convert(),
                                 [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                 ["Congratulations!",64,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                 worldEndDictionary).displayMenu()

        utility.fadeMusic()
        credits.Credits(self.screen,self.musicList[MENU_MUSIC])
        
        self.done = True