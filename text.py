import sys
import pygame
import utility
import vector

from utility import *  

class Text(pygame.sprite.Sprite):
    def __init__(self, fontType, fontSize = 12, color = (0,0,0), text = "", lifeTimer = -1, textIndex = 0):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        
        self.textIndex = textIndex
        self.text = text
        self.color = color
        self.fontType = fontType
        
        self.fontSize = fontSize
        self.lifeTimer = lifeTimer
        self.alignment = TOP_LEFT
        self.buildImage()
        self.position = vector.Vector2d(0, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if not (self.lifeTimer == -1):
            if not self.lifeTimer:
                self.kill()
    
            self.lifeTimer -= 1
            
        if self.alignment == TOP_LEFT:
            self.rect.topleft = (self.position.x, self.position.y)
        
        elif self.alignment == TOP_MIDDLE:
            self.rect.midtop = (self.position.x, self.position.y)
        
        elif self.alignment == TOP_RIGHT:
            self.rect.topright = (self.position.x, self.position.y)
        
        elif self.alignment == CENTER_LEFT:
            self.rect.midleft = (self.position.x, self.position.y)
        
        elif self.alignment == CENTER_MIDDLE:
            self.rect.center = (self.position.x, self.position.y)
        
        elif self.alignment == CENTER_RIGHT:
            self.rect.midright = (self.position.x, self.position.y)

        elif self.alignment == BOTTOM_LEFT:
            self.rect.bottomleft = (self.position.x, self.position.y)

        elif self.alignment == BOTTOM_MIDDLE:
            self.rect.midbottom = (self.position.x, self.position.y)

        elif self.alignment == BOTTOM_RIGHT:
            self.rect.bottomright = (self.position.x, self.position.y)

    def setFont(self, fontSize, color, fontType):
        self.color = color
        self.fontType = fontType
        self.fontSize = fontSize
        self.buildImage()

    def set_text(self, text):
        self.text = text
        self.buildImage()
    
    def getText(self):
        return self.text

    def setColor(self, (rValue, gValue, bValue)):
        self.color = rValue, gValue, bValue
    
    def getColor(self):
        return self.color
        
    def getPosition(self):
        """This method returns the sprite's position"""
        return [self.position.x, self.position.y]

    def setPosition(self, (setX, setY)):
        """This method sets the sprite's position"""
        self.position.x = setX
        self.position.y = setY

    def mouseOver(self):
        mousePosition = list(pygame.mouse.get_pos())
        if ( mousePosition[0] > self.rect.left ) and ( mousePosition[0] < self.rect.right ) and ( mousePosition[1] > self.rect.top ) and ( mousePosition[1] < self.rect.bottom ):
            return True
        else:
            return False
        
    def mouseOverDump(self):
        print "Mouse Position: ", list(pygame.mouse.get_pos())
        print "[Rect Dimensions: ", "<LEFT: ", self.rect.left, ">", "<RIGHT: ", self.rect.right, ">", "<TOP: ", self.rect.top, ">", "<BOTTOM: ", self.rect.bottom, ">]"

    def setTimer(self, lifeTimer):
        self.lifeTimer = lifeTimer
    
    def set_alignment(self, alignment):
        self.alignment = alignment

    def copy(self):
        newObject = Text(self.fontType,self.fontSize,self.color,self.text,self.lifeTimer)
        newObject.set_alignment(self.alignment)
        
        return newObject

    def buildImage(self):
        self.fontObject = pygame.font.Font(self.fontType, self.fontSize)
        self.image = self.fontObject.render(str(self.text), ANTI_ALIAS, self.color)
        self.rect = self.image.get_rect()

class TextSurface:
    def __init__(self,fontType,fontSize,color,text):
        fontObject = pygame.font.Font(fontType, fontSize)
        self.image = fontObject.render(str(text), ANTI_ALIAS, color)