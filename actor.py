import utility
import settings
import pygame
import vector
import animation

from settings import *

class Actor(pygame.sprite.Sprite):
    """The Generic Actor Class"""

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        
        """   DEFAULT VARIABLES   """
        self.canCollide = False
        self.active = False
        self.hitrect = pygame.Rect(0,0,0,0)
        self.hitrectOffsetX = 0
        self.hitrectOffsetY = 0
        self.objectCollidedWith = self
        self.boundStyle = None



    def actorUpdate(self):
        pass
    
    
    
    def update(self):
        """**********Animation**********"""
        try:
            self.animationList.update()
            self.image = self.animationList.image
        except:
            pass
        
        

        """*******Translation*******"""
        self.position += self.velocity
        self.checkBounds()

        """Place the image at its new posistion"""
        self.rect.center = (self.position.x, self.position.y)
        self.hitrect.center = (self.position.x + self.hitrectOffsetX, self.position.y + self.hitrectOffsetY)
        
        """Run custom Actor code"""
        self.actorUpdate()



    def checkCollision(self, groupChecked):
        for objectChecked in groupChecked:
            if self.hitrect.colliderect(objectChecked.hitrect):
                if self.active and objectChecked.active:
                    self.objectCollidedWith = objectChecked
                    objectChecked.objectCollidedWith = self
                    self.collide()
                    objectChecked.collide()



    def collide(self):
        pass
        
        
        
    def checkBounds(self):
        curX = self.position.x
        curY = self.position.y
        
        if curX < self.bounds[LEFT] or curX > self.bounds[RIGHT] or curY < self.bounds[TOP] or curY > self.bounds[BOTTOM]:            
            self.outOfBounds()


            
    def die(self):
        self.kill()
        del self
        
            
            
    def outOfBounds(self):
        if self.boundStyle == BOUND_STYLE_CLAMP:
            if self.position.x < self.bounds[LEFT]:
                self.position = vector.vector2d(self.bounds[LEFT],self.position.y)
            elif self.position.x > self.bounds[RIGHT]:
                self.position = vector.vector2d(self.bounds[RIGHT],self.position.y)
            if self.position.y < self.bounds[TOP]:
                self.position = vector.vector2d(self.position.x, self.bounds[TOP])
            elif self.position.y > self.bounds[BOTTOM]:
                self.position = vector.vector2d(self.position.x, self.bounds[BOTTOM])
                
        elif self.boundStyle == BOUND_STYLE_WRAP:
            if self.position.x < self.bounds[LEFT]:
                self.position = vector.vector2d(self.bounds[RIGHT],self.position.y)
            elif self.position.x > self.bounds[RIGHT]:
                self.position = (self.bounds[LEFT],self.position.y)
            if self.position.y < self.bounds[TOP]:
                self.position = (self.position.x, self.bounds[BOTTOM])
            elif self.position.y > self.bounds[BOTTOM]:
                self.position = (self.position.x, self.bounds[TOP])
                
        elif self.boundStyle == BOUND_STYLE_REFLECT:
            if self.position.x < self.bounds[LEFT]:
                self.position = vector.vector2d(self.bounds[LEFT],self.position.y)
                self.velocity *= [-1.0, 1.0]
            elif self.position.x > self.bounds[RIGHT]:
                self.position = vector.vector2d(self.bounds[RIGHT],self.position.y)
                self.velocity *= [-1.0, 1.0]
            if self.position.y < self.bounds[TOP]:
                self.position = vector.vector2d(self.position.x, self.bounds[TOP])
                self.velocity *= [1.0, -1.0]
            elif self.position.y > self.bounds[BOTTOM]:
                self.position = vector.vector2d(self.position.x, self.bounds[BOTTOM])
                self.velocity *= [1.0, -1.0]
                
        elif self.boundStyle == BOUND_STYLE_KILL:
            self.kill()
            
        elif self.boundStyle == BOUND_STYLE_CUSTOM:
            self.customBounds()

