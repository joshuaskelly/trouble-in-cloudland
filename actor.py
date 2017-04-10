import pygame

import animation
import vector

from settings import *


class Actor(pygame.sprite.Sprite):
    """The Generic Actor Class"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.can_collide = False
        self.active = False
        self.hitrect = pygame.Rect(0, 0, 0, 0)
        self.hitrect_offset_x = 0
        self.hitrect_offset_y = 0
        self.object_collided_with = self
        self.bound_style = None
        self.animation_list = animation.Animation()
        self.image = None

    def actor_update(self):
        pass

    def update(self):
        try:
            self.animation_list.update()
            self.image = self.animation_list.image

        except:
            pass

        self.position += self.velocity
        self.check_bounds()
        self.rect.center = (self.position.x, self.position.y)
        self.hitrect.center = (self.position.x + self.hitrect_offset_x, self.position.y + self.hitrect_offset_y)
        
        self.actor_update()

    def check_collision(self, group_checked):
        for object_checked in group_checked:
            if self.hitrect.colliderect(object_checked.hitrect):
                if self.active and object_checked.active:
                    self.object_collided_with = object_checked
                    object_checked.object_collided_with = self
                    self.collide()
                    object_checked.collide()

    def collide(self):
        pass
        
    def check_bounds(self):
        current_x = self.position.x
        current_y = self.position.y
        
        if current_x < self.bounds[LEFT] or current_x > self.bounds[RIGHT] or current_y < self.bounds[TOP] or current_y > self.bounds[BOTTOM]:
            self.out_of_bounds()

    def die(self):
        self.kill()
        del self
        
    def out_of_bounds(self):
        if self.bound_style == BOUND_STYLE_CLAMP:
            if self.position.x < self.bounds[LEFT]:
                self.position = vector.Vector2d(self.bounds[LEFT], self.position.y)
            elif self.position.x > self.bounds[RIGHT]:
                self.position = vector.Vector2d(self.bounds[RIGHT], self.position.y)
            if self.position.y < self.bounds[TOP]:
                self.position = vector.Vector2d(self.position.x, self.bounds[TOP])
            elif self.position.y > self.bounds[BOTTOM]:
                self.position = vector.Vector2d(self.position.x, self.bounds[BOTTOM])
                
        elif self.bound_style == BOUND_STYLE_WRAP:
            if self.position.x < self.bounds[LEFT]:
                self.position = vector.Vector2d(self.bounds[RIGHT], self.position.y)
            elif self.position.x > self.bounds[RIGHT]:
                self.position = (self.bounds[LEFT],self.position.y)
            if self.position.y < self.bounds[TOP]:
                self.position = (self.position.x, self.bounds[BOTTOM])
            elif self.position.y > self.bounds[BOTTOM]:
                self.position = (self.position.x, self.bounds[TOP])
                
        elif self.bound_style == BOUND_STYLE_REFLECT:
            if self.position.x < self.bounds[LEFT]:
                self.position = vector.Vector2d(self.bounds[LEFT], self.position.y)
                self.velocity *= [-1.0, 1.0]
            elif self.position.x > self.bounds[RIGHT]:
                self.position = vector.Vector2d(self.bounds[RIGHT], self.position.y)
                self.velocity *= [-1.0, 1.0]
            if self.position.y < self.bounds[TOP]:
                self.position = vector.Vector2d(self.position.x, self.bounds[TOP])
                self.velocity *= [1.0, -1.0]
            elif self.position.y > self.bounds[BOTTOM]:
                self.position = vector.Vector2d(self.position.x, self.bounds[BOTTOM])
                self.velocity *= [1.0, -1.0]
                
        elif self.bound_style == BOUND_STYLE_KILL:
            self.kill()
            
        elif self.bound_style == BOUND_STYLE_CUSTOM:
            self.custom_bounds()

    def custom_bounds(self):
        pass