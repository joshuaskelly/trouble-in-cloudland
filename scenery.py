import pygame
import actor
import utility
import random
import animation
import copy
import aitools

from actor import *

def loadData():
    Cloud.MasterAnimationList.buildAnimation("Idle", ["cloud"])   
    CloudSmall.MasterAnimationList.buildAnimation("Idle", ["cloud1"])
    IslandBig.MasterAnimationList.buildAnimation("Idle", ["island01"]) 
    IslandSmall.MasterAnimationList.buildAnimation("Idle", ["island02"])
    whiteCloud.MasterAnimationList.buildAnimation("Idle", ["cloud2"])
    whiteCloudSmall.MasterAnimationList.buildAnimation("Idle", ["cloud3"])
    whiteCloudTiny.MasterAnimationList.buildAnimation("Idle", ["cloud4"])
    treeBig.MasterAnimationList.buildAnimation("Idle", ["tree"])
    treeSmall.MasterAnimationList.buildAnimation("Idle", ["tree1"])
    blueCloud.MasterAnimationList.buildAnimation("Idle", ["cloudBlue"])
    blueCloudSmall.MasterAnimationList.buildAnimation("Idle", ["cloudBlueSmall"])
    smallStar.MasterAnimationList.buildAnimation("Idle", ["pstaar0"])
        
class Cloud(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-512,256,SCREEN_WIDTH + 512,SCREEN_HEIGHT + 256]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 1.0 + 2.5, 0.0)


    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        


class CloudSmall(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-256,256,SCREEN_WIDTH + 256,SCREEN_HEIGHT + 128]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 0.5 + 1.5, 0.0)
        
        """   UNIQUE VARIABLES   """
        self.speed = random.random() * 2.0
        self.changeDirection = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        
        
        
class IslandBig(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-512,384,SCREEN_WIDTH + 256,SCREEN_HEIGHT - 64]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d(random.random() * 0.5 + 1.5, 0.0)
        
        """   UNIQUE VARIABLES   """
        self.speed = random.random() * 2.0
        self.changeDirection = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d((random.random() * self.bounds[LEFT]) - 128, ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        

class IslandSmall(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-256,384,SCREEN_WIDTH + 256,SCREEN_HEIGHT - 128]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d(random.random() * 0.25 + 0.5, 0.0)
        
        """   UNIQUE VARIABLES   """
        self.speed = random.random() * 2.0
        self.changeDirection = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d((random.random() * self.bounds[LEFT]) - 128, (((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP])))
        
    def custom_bounds(self):
        self.spawn()
        

        
class whiteCloud(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-512,512,SCREEN_WIDTH + 512,SCREEN_HEIGHT]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 1.0 + 2.5, 0.0)


    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        
        
        
class whiteCloudSmall(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-256,384,SCREEN_WIDTH + 256,SCREEN_HEIGHT]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 0.5 + 1.5, 0.0)
        
        """   UNIQUE VARIABLES   """
        self.speed = random.random() * 2.0
        self.changeDirection = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        
class whiteCloudTiny(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-256,384,SCREEN_WIDTH + 384,SCREEN_HEIGHT - 128]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 0.5 + 0.5, 0.0)
        
        """   UNIQUE VARIABLES   """
        self.speed = random.random() * 2.0
        self.changeDirection = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        
        

class treeBig(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-768,384,SCREEN_WIDTH + 256,SCREEN_HEIGHT - 100]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(2.5, 0.0)


    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d((random.random() * -384) - 300, ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        #print "<OutOfBounds: " + str(self.position) + ">"
        self.spawn()
        
        
        
class treeSmall(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):
    
        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-768,600,SCREEN_WIDTH + 256,SCREEN_HEIGHT + 64]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(1.0, 0.0)
    
    
    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d((random.random() * -384) - 300, ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        #print "<OutOfBounds: " + str(self.position) + ">"
        self.spawn()
        
        
        
class blueCloud(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        #self.bounds = [-256,-150,SCREEN_WIDTH + 512,SCREEN_HEIGHT + 512]
        self.bounds = [-256,-108,SCREEN_WIDTH + 150,SCREEN_HEIGHT + 256]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(1.25, -4.0)


    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(((random.random() * (self.bounds[RIGHT] - self.bounds[LEFT])) + self.bounds[LEFT]),
                                        ((random.random() * 128) + 1024))
        
    def custom_bounds(self):
        self.spawn()
        
        

class blueCloudSmall(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-256,-128,SCREEN_WIDTH + 128,SCREEN_HEIGHT + 256]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(.75, -2.5)


    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(((random.random() * (self.bounds[RIGHT] - self.bounds[LEFT])) + self.bounds[LEFT]),
                                        ((random.random() * 128) + 768))
        
    def custom_bounds(self):
        self.spawn()        
        
        
        
class smallStar(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)     
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-32,-32,SCREEN_WIDTH,SCREEN_HEIGHT + 64]
                
        self.canCollide = False
        
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d(0.0, -1.0)


    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(((random.random() * (self.bounds[RIGHT] - self.bounds[LEFT])) + self.bounds[LEFT]),
                                        ((random.random() * 32.0) + 768))
    def custom_bounds(self):
        self.spawn()
