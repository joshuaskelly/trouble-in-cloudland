import copy
import random

import actor
from actor import *


def load_data():
    Cloud.master_animation_list.build_animation('Idle', ['cloud'])
    CloudSmall.master_animation_list.build_animation('Idle', ['cloud1'])
    IslandBig.master_animation_list.build_animation('Idle', ['island01'])
    IslandSmall.master_animation_list.build_animation('Idle', ['island02'])
    WhiteCloud.master_animation_list.build_animation('Idle', ['cloud2'])
    WhiteCloudSmall.master_animation_list.build_animation('Idle', ['cloud3'])
    WhiteCloudTiny.master_animation_list.build_animation('Idle', ['cloud4'])
    TreeBig.master_animation_list.build_animation('Idle', ['tree'])
    TreeSmall.master_animation_list.build_animation('Idle', ['tree1'])
    BlueCloud.master_animation_list.build_animation('Idle', ['cloudBlue'])
    BlueCloudSmall.master_animation_list.build_animation('Idle', ['cloudBlueSmall'])
    SmallStar.master_animation_list.build_animation('Idle', ['pstaar0'])


class Cloud(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -512, 256, SCREEN_WIDTH + 512, SCREEN_HEIGHT + 256
        self.can_collide = False
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
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -256, 256, SCREEN_WIDTH + 256, SCREEN_HEIGHT + 128
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 0.5 + 1.5, 0.0)
        
        # UNIQUE VARIABLES
        self.speed = random.random() * 2.0
        self.change_direction = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()

        
class IslandBig(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -512, 384, SCREEN_WIDTH + 256, SCREEN_HEIGHT - 64
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d(random.random() * 0.5 + 1.5, 0.0)
        
        # UNIQUE VARIABLES
        self.speed = random.random() * 2.0
        self.change_direction = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d((random.random() * self.bounds[LEFT]) - 128, ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        

class IslandSmall(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -256, 384, SCREEN_WIDTH + 256, SCREEN_HEIGHT - 128
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d(random.random() * 0.25 + 0.5, 0.0)
        
        # UNIQUE VARIABLES
        self.speed = random.random() * 2.0
        self.change_direction = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d((random.random() * self.bounds[LEFT]) - 128, (((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP])))
        
    def custom_bounds(self):
        self.spawn()
        

class WhiteCloud(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -512, 512, SCREEN_WIDTH + 512, SCREEN_HEIGHT
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 1.0 + 2.5, 0.0)

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()

        
class WhiteCloudSmall(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -256, 384, SCREEN_WIDTH + 256, SCREEN_HEIGHT
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 0.5 + 1.5, 0.0)
        
        # UNIQUE VARIABLES
        self.speed = random.random() * 2.0
        self.change_direction = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()


class WhiteCloudTiny(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -256, 384, SCREEN_WIDTH + 384, SCREEN_HEIGHT - 128
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(random.random() * 0.5 + 0.5, 0.0)
        
        # UNIQUE VARIABLES
        self.speed = random.random() * 2.0
        self.change_direction = 0

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(random.random() * (self.bounds[LEFT] - (SCREEN_WIDTH + 256)), ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        

class TreeBig(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -768, 384, SCREEN_WIDTH + 256, SCREEN_HEIGHT - 100
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(2.5, 0.0)

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d((random.random() * -384) - 300, ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()
        

class TreeSmall(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -768, 600, SCREEN_WIDTH + 256, SCREEN_HEIGHT + 64
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.spawn()
        self.velocity = vector.Vector2d(1.0, 0.0)

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d((random.random() * -384) - 300, ((random.random() * (self.bounds[BOTTOM] - self.bounds[TOP])) + self.bounds[TOP]))
        
    def custom_bounds(self):
        self.spawn()

        
class BlueCloud(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -256, -108, SCREEN_WIDTH + 150, SCREEN_HEIGHT + 256
        self.can_collide = False
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


class BlueCloudSmall(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -256, -128, SCREEN_WIDTH + 128, SCREEN_HEIGHT + 256
        self.can_collide = False
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
        

class SmallStar(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -32, -32, SCREEN_WIDTH, SCREEN_HEIGHT + 64
        self.can_collide = False
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d(0.0, -1.0)

    def actor_update(self):
        pass
    
    def spawn(self):
        self.position = vector.Vector2d(((random.random() * (self.bounds[RIGHT] - self.bounds[LEFT])) + self.bounds[LEFT]),
                                        ((random.random() * 32.0) + 768))

    def custom_bounds(self):
        self.spawn()
