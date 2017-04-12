import actor

from actor import *


class Icon(actor.Actor):
    def __init__(self, image_file):
        actor.Actor.__init__(self)
        
        self.animation_list = animation.Animation()
        self.animation_list.build_animation('Idle', [image_file])
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        
        self.rect = self.image.get_rect()
        
        self.position = vector.Vector2d(26, 68)
        self.velocity = vector.Vector2d.zero
        
        self.bounds = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
