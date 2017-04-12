import copy

import actor
from actor import *
from ui import text, infobubble
from utils import utility


def load_data():
    Balloon.pickup_sound = utility.load_sound('pop')
    Bonus250.master_animation_list.build_animation('Idle', ['balloonblue'])
    Bonus500.master_animation_list.build_animation('Idle', ['balloongreen'])

    BonusX2.master_animation_list.build_animation('Idle', ['balloonred'])
    BonusX2.pickup_sound = utility.load_sound('doublePoints')
    BonusCombo.master_animation_list.build_animation('Idle', ['balloonyellow'])
    BonusCombo.pickup_sound = utility.load_sound('combo')


class Balloon(actor.Actor):
    def __init__(self):
        actor.Actor.__init__(self)
        self.actor_type = ACTOR_TYPE_PICKUP
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = -32, -32, SCREEN_WIDTH + 32, SCREEN_HEIGHT + 32
        
        # MOVEMENT VARIABLES
        self.wave = 0
        self.move_right = True
        self.x_movement = 1
        self.velocity = vector.Vector2d.zero

    def actor_update(self):
        self.active = True
        
        if self.move_right:
            self.wave -= 1
            if self.wave < -0.20 * FRAMES_PER_SECOND:
                self.move_right = False
        else:
            self.wave += 1
            if self.wave > FRAMES_PER_SECOND:
                self.move_right = True

        self.x_movement = (self.wave / FRAMES_PER_SECOND) * 1.5
        self.velocity = vector.Vector2d(self.x_movement, -3)

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            utility.play_sound(self.pickup_sound)
            self.die()


class Bonus250(Balloon):
    master_animation_list = animation.Animation()

    def __init__(self, position, text_group):
        Balloon.__init__(self)
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')

        self.rect = self.image.get_rect()        
        self.hitrect = pygame.Rect(0,0,60,60)
        self.hitrect_offset_y = -5
        
        self.text_group = text_group
        self.position = vector.Vector2d(position)

    def die(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.increment_score(250, self.position, self.text_group)
        
        self.active = False
        self.kill()
        del self


class Bonus500(Balloon):
    master_animation_list = animation.Animation()

    def __init__(self, position, text_group):
        Balloon.__init__(self)
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')

        self.rect = self.image.get_rect()        
        self.hitrect = pygame.Rect(0, 0, 60, 60)
        self.hitrect_offset_y = -5
        
        self.text_group = text_group
        self.position = vector.Vector2d(position)

    def die(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.increment_score(500, self.position, self.text_group)
        
        self.active = False
        self.kill()
        del self


class BonusX2(Balloon):
    master_animation_list = animation.Animation()

    def __init__(self, position, text_group):
        Balloon.__init__(self)
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')

        self.rect = self.image.get_rect()        
        self.hitrect = pygame.Rect(0, 0, 60, 60)
        self.hitrect_offset_y = -5
        
        self.position = vector.Vector2d(position)
        self.text_group = text_group

    def die(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.point_bonus += 5 * FRAMES_PER_SECOND
            temp_image = text.Text(FONT_PATH, 30, FONT_COLOR, 'Double Points!', 1).image
            
            help_bubble = infobubble.InfoBubble(temp_image, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
            help_bubble.offset = vector.Vector2d(0.0, -100.0)
            self.text_group.add(help_bubble)
        
        self.active = False
        self.kill()
        del self


class BonusCombo(Balloon):
    master_animation_list = animation.Animation()

    def __init__(self, position, text_group):
        Balloon.__init__(self)
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')

        self.rect = self.image.get_rect()        
        self.hitrect = pygame.Rect(0, 0, 60, 60)
        self.hitrect_offset_y = -5
        
        self.position = vector.Vector2d(position)
        self.text_group = text_group

    def die(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.combo_bonus += 5 * FRAMES_PER_SECOND
            temp_image = text.Text(FONT_PATH, 30, FONT_COLOR, 'Combo Time!', 1).image
            
            help_bubble = infobubble.InfoBubble(temp_image, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
            help_bubble.offset = vector.Vector2d(0.0, -100.0)
            self.text_group.add(help_bubble)
        
        self.active = False
        self.kill()
        del self
