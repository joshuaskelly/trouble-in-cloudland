import pygame
import scenery
import settings
import utility
import aitools

from settings import *

class rockyScene:
    
    def __init__(self):
        self.actorGroup1 = pygame.sprite.Group()
        self.actorGroup2 = pygame.sprite.Group()
        self.actorGroup3 = pygame.sprite.Group()
        
        self.cloudTimer = 0
        scenery.loadData()
        
        self.DoOnce = True

       
            
    def render(self):
        self.actorGroup3.draw(self.screen)
        self.actorGroup2.draw(self.screen)
        self.actorGroup1.draw(self.screen)


    
    def update(self):
        if self.DoOnce:
            CloudsToCreate = 11
            while CloudsToCreate:
                tempCloud = scenery.CloudSmall()
                aitools.spawnOnScreen(tempCloud)
                self.actorGroup2.add(tempCloud)
                CloudsToCreate -= 1
                
            IslandsToCreate = 3
            while IslandsToCreate:
                tempIsland = scenery.IslandBig()
                aitools.spawnOnScreen(tempIsland)
                self.actorGroup2.add(tempIsland)
                IslandsToCreate -= 1
                
            CloudsToCreate = 7
            while CloudsToCreate:
                tempCloud = scenery.Cloud()
                aitools.spawnOnScreen(tempCloud)
                self.actorGroup1.add(tempCloud)
                CloudsToCreate -= 1
            self.DoOnce = False
            
            IslandsToCreate = 9
            while IslandsToCreate:
                tempIsland = scenery.IslandSmall()
                aitools.spawnOnScreen(tempIsland)
                self.actorGroup3.add(tempIsland)
                IslandsToCreate -= 1
        
        self.actorGroup3.update()
        self.actorGroup2.update()
        self.actorGroup1.update()
       
        
    
    def draw(self, screen):
        self.screen = screen
        
        self.screen.fill(FILL_COLOR)
        self.update()
        self.render()
        
        

class forestScene:
    
    def __init__(self):
        self.actorGroup1 = pygame.sprite.Group()
        self.actorGroup2 = pygame.sprite.Group()
        self.actorGroup3 = pygame.sprite.Group()
        
        self.cloudTimer = 0
        scenery.loadData()
        
        self.DoOnce = True

       
            
    def render(self):
        self.actorGroup3.draw(self.screen)
        self.actorGroup2.draw(self.screen)
        self.actorGroup1.draw(self.screen)


    
    def update(self):
        if self.DoOnce:

            CloudsToCreate = 3
            while CloudsToCreate:
                tempIsland = scenery.whiteCloud()
                aitools.spawnOnScreen(tempIsland)
                self.actorGroup1.add(tempIsland)
                CloudsToCreate -= 1
                
            TreesToCreate = 3
            while TreesToCreate:
                tempTree = scenery.treeBig()
                aitools.spawnOnScreen(tempTree)
                self.actorGroup1.add(tempTree)
                TreesToCreate -= 1
                
            CloudsToCreate = 4
            while CloudsToCreate:
                tempIsland = scenery.whiteCloudSmall()
                aitools.spawnOnScreen(tempIsland)
                self.actorGroup2.add(tempIsland)
                CloudsToCreate -= 1   

            TreesToCreate = 4
            while TreesToCreate:
                tempTree = scenery.treeSmall()
                aitools.spawnOnScreen(tempTree)
                self.actorGroup2.add(tempTree)
                TreesToCreate -= 1
                
            CloudsToCreate = 6
            while CloudsToCreate:
                tempIsland = scenery.whiteCloudTiny()
                aitools.spawnOnScreen(tempIsland)
                self.actorGroup3.add(tempIsland)
                CloudsToCreate -= 1               

            self.DoOnce = False
          
        
        self.actorGroup3.update()
        self.actorGroup2.update()
        self.actorGroup1.update()
       
        
    
    def draw(self, screen):
        self.screen = screen
        
        self.screen.fill([200,200,234])
        self.update()
        self.render()
        

class pinkScene:
    
    def __init__(self):
        self.actorGroup1 = pygame.sprite.Group()
        self.actorGroup2 = pygame.sprite.Group()
        self.actorGroup3 = pygame.sprite.Group()

        scenery.loadData()
        
        self.DoOnce = True

       
            
    def render(self):
        self.actorGroup3.draw(self.screen)
        self.actorGroup2.draw(self.screen)
        self.actorGroup1.draw(self.screen)


    
    def update(self):
        if self.DoOnce:
            CloudsToCreate = 6
            while CloudsToCreate:
                tempCloud = scenery.blueCloud()
                aitools.spawnOnScreen(tempCloud)
                self.actorGroup1.add(tempCloud)
                CloudsToCreate -= 1
                
            CloudsToCreate = 6
            while CloudsToCreate:
                tempCloud = scenery.blueCloudSmall()
                aitools.spawnOnScreen(tempCloud)
                self.actorGroup2.add(tempCloud)
                CloudsToCreate -= 1
                
            StarsToCreate = 12
            while StarsToCreate:
                tempStar = scenery.smallStar()
                aitools.spawnOnScreen(tempStar)
                self.actorGroup3.add(tempStar)
                StarsToCreate -= 1
            self.DoOnce = False
          
        self.actorGroup1.update()
        self.actorGroup2.update()
        self.actorGroup3.update()
       
        
    
    def draw(self, screen):
        self.screen = screen
        
        self.screen.fill([234,203,200])
        self.update()
        self.render()
        
        

class tutorialScene:
    
    def __init__(self):
        self.actorGroup1 = pygame.sprite.Group()

        scenery.loadData()
        
        self.DoOnce = True

       
            
    def render(self):
        self.actorGroup1.draw(self.screen)


    
    def update(self):
        if self.DoOnce:
            self.DoOnce = False
          
        self.actorGroup1.update()
       
        
    
    def draw(self, screen):
        self.screen = screen
        
        self.screen.fill(FILL_COLOR)
        self.update()
        self.render()