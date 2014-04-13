import pygame
import text
import settings
import vector
import utility
import actor
import copy
import animation

from settings import *

def loadData():
    Cursor.MasterAnimationList.buildAnimation("Idle", ["cursor"])

class Menu:
    def __init__(self, screen, musicList, backgroundImage, bounds, title, menuDictionary, startSelection = 0):
        
        self.screen = screen
        self.bounds = bounds
        self.menuDictionary = menuDictionary
        self.title = title
        self.musicList = musicList
        self.backgroundImage = backgroundImage
        
        self.cursor = Cursor()
        
        pygame.mouse.set_visible(False)
        
        self.menuGroup = pygame.sprite.Group()
        self.menuTooltipGroup = pygame.sprite.Group()
        self.cursorGroup = pygame.sprite.Group()
        self.menuSelectionPointer = []
        self.menuTooltipPointer = []
        self.currentSelection = startSelection
        self.timer = pygame.time.Clock()
        
        self.menuBeep = utility.loadSound("menuBeep")
        self.menuForward = utility.loadSound("menuForward")
        self.menuBack = utility.loadSound("menuBack")
        
        index = 0
        
        menuTitle = text.Text(FONT_PATH, title[1], FONT_COLOR, title[0])
        menuTitle.position = vector.vector2d(title[2],title[3])
        menuTitle.setAlign(CENTER_MIDDLE)
        self.menuGroup.add(menuTitle)
        
        for option in menuDictionary:
            menuSelection = text.Text(FONT_PATH, 32, FONT_INACTIVE_COLOR, menuDictionary[option][0],-1,index)
            menuSelection.setAlign(CENTER_MIDDLE)
            menuSelection.position = vector.vector2d((((self.bounds[RIGHT]-self.bounds[LEFT]) / 2)+self.bounds[LEFT],
                                         ((self.bounds[BOTTOM]-self.bounds[TOP]) / (len(self.menuDictionary)+1)*(index + 1))+self.bounds[TOP]))
            
            self.menuGroup.add(menuSelection)
            self.menuSelectionPointer.append(menuSelection)
            
            menuTooltip = text.Text(FONT_PATH, 32, FONT_COLOR, menuDictionary[option][1])
            menuTooltip.setAlign(BOTTOM_MIDDLE)
            menuTooltip.position = vector.vector2d(((SCREEN_WIDTH / 2),SCREEN_HEIGHT))
            self.menuTooltipGroup.add(menuTooltip)
            self.menuTooltipPointer.append(menuTooltip)
            index += 1
            
        self.cursorGroup.add(self.cursor)
            
            
            
            
    def displayMenu(self):
        
        self.menuSelectionPointer[self.currentSelection].setFont(48, FONT_COLOR, FONT_PATH)
        pygame.mouse.get_rel()
        mouseTimeout = 10
        sampleMouse = True
        
        while True:
            """Music Stuff"""
            utility.playMusic(self.musicList)

            """Drawing Stuff"""
            self.screen.fill(FILL_COLOR)
            self.menuGroup.update()
            self.menuTooltipGroup.update()
            self.cursorGroup.update()
            try:
                self.screen.blit(self.backgroundImage, self.backgroundImage.get_rect())
            except:
                self.backgroundImage.draw(self.screen)
            
            self.menuGroup.draw(self.screen)
            self.menuTooltipPointer[self.currentSelection].draw(self.screen)
            self.cursorGroup.draw(self.screen)
            
            pygame.display.flip()
            
            self.cursor.position = vector.vector2d(pygame.mouse.get_pos()) + vector.vector2d(32,32)
            
            """Event Handling Stuff"""
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    utility.playSound(self.menuForward)
                    return self.menuDictionary.keys()[self.currentSelection]
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    utility.playSound(self.menuForward)
                    return self.menuDictionary.keys()[self.currentSelection]
    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    utility.playSound(self.menuBack)
                    return False
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    utility.playSound(self.menuBack)
                    return False
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.menuSelectionPointer[self.currentSelection].setFont(32, FONT_INACTIVE_COLOR, FONT_PATH)
                    self.currentSelection -= 1
                    if self.currentSelection < 0:
                        self.currentSelection = len(self.menuDictionary) - 1
                    self.menuSelectionPointer[self.currentSelection].setFont(48, FONT_COLOR, FONT_PATH)
                    utility.playSound(self.menuBeep)

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.menuSelectionPointer[self.currentSelection].setFont(32, FONT_INACTIVE_COLOR, FONT_PATH)
                    self.currentSelection += 1
                    if self.currentSelection > len(self.menuDictionary) - 1:
                        self.currentSelection = 0
                    self.menuSelectionPointer[self.currentSelection].setFont(48, FONT_COLOR, FONT_PATH)
                    utility.playSound(self.menuBeep)
                    
                elif event.type == pygame.MOUSEMOTION:
                    for element in self.menuGroup:
                        if element.mouseOver():
                            if (element.textIndex != self.currentSelection):
                                self.menuSelectionPointer[self.currentSelection].setFont(32, FONT_INACTIVE_COLOR, FONT_PATH)
                                mouseSelection = element.textIndex
                                self.currentSelection = mouseSelection
                                self.menuSelectionPointer[self.currentSelection].setFont(48, FONT_COLOR, FONT_PATH)
                                utility.playSound(self.menuBeep)
            #
                    
                
                """elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    for element in self.menuTooltipGroup:
                        print "ELEMENT: ", element.textIndex
                        element.mouseOverDump()"""
                    
                """elif event.type == pygame.MOUSEMOTION:
                    mouseInput = list(pygame.mouse.get_rel())
                    if sampleMouse:
                        if mouseInput[1] < -10:
                            self.menuSelectionPointer[self.currentSelection].setFont(32, FONT_INACTIVE_COLOR, FONT_PATH)
                            self.currentSelection -= 1
                            if self.currentSelection < 0:
                                self.currentSelection = len(self.menuDictionary) - 1
                            self.menuSelectionPointer[self.currentSelection].setFont(48, FONT_COLOR, FONT_PATH)
                            sampleMouse = False
                            utility.playSound(self.menuBeep)
                                                
                        elif mouseInput[1] > 10:
                            self.menuSelectionPointer[self.currentSelection].setFont(32, FONT_INACTIVE_COLOR, FONT_PATH)
                            self.currentSelection += 1
                            if self.currentSelection > len(self.menuDictionary) - 1:
                                self.currentSelection = 0
                            self.menuSelectionPointer[self.currentSelection].setFont(48, FONT_COLOR, FONT_PATH)
                            sampleMouse = False       
                            utility.playSound(self.menuBeep)   """                  
                            

                    
            if not sampleMouse:
                mouseTimeout -= 1
                
            if mouseTimeout == 0:
                sampleMouse = True
                mouseTimeout = 3
                
            self.timer.tick(30)
                
                
class Cursor(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):
        actor.Actor.__init__(self)
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.boundStyle == BOUND_STYLE_CLAMP
        self.bounds = [32,32,(SCREEN_WIDTH),(SCREEN_HEIGHT)]
        
        self.position = vector.vector2d.zero
        self.velocity = vector.vector2d.zero
        
    def mouseOver(self):
        pass