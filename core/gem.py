import copy

import actor
import bullet
from actor import *
from ui import text, infobubble
from utils import utility


def load_data():
    DamageX2.pickup_sound = utility.load_sound('doubleDamage')
    DamageX2.master_animation_list.build_animation('Idle', ['geemred'])
    DamageX2.master_animation_list.build_animation('Blink', ['geemred', 'blank'])
    
    Nova.pickup_sound = utility.load_sound('nova')
    Nova.master_animation_list.build_animation('Idle', ['boom'])
    Nova.master_animation_list.build_animation('Blink', ['boom', 'blank'])

    Reflect.pickup_sound = utility.load_sound('reflect')
    Reflect.master_animation_list.build_animation('Idle', ['geemblue'])
    Reflect.master_animation_list.build_animation('Blink', ['geemblue', 'blank'])

    DualShot.pickup_sound = utility.load_sound('dualShot')
    DualShot.master_animation_list.build_animation('Idle', ['geemgreen'])
    DualShot.master_animation_list.build_animation('Blink', ['geemgreen', 'blank'])

    FastShot.pickup_sound = utility.load_sound('fastShot')
    FastShot.master_animation_list.build_animation('Idle', ['geemorange'])
    FastShot.master_animation_list.build_animation('Blink', ['geemorange', 'blank'])


class Gem(actor.Actor):
    def __init__(self):
        actor.Actor.__init__(self)

        self.actor_type = ACTOR_TYPE_PICKUP
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -16, -16, SCREEN_WIDTH + 16, SCREEN_HEIGHT + 16
        self.bonusTime = 0
        self.life_timer = 5 * FRAMES_PER_SECOND

    def actor_update(self):
        if not self.active:
            self.active = True
            
        if not self.life_timer:
            self.die()
            
        self.life_timer -= 1
            
        if self.life_timer < 2 * FRAMES_PER_SECOND:
            self.animation_list.play('Blink')

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            utility.play_sound(self.pickup_sound, PICKUP_CHANNEL)
            self.display_text()
            self.give_bonus()
            self.die()

    def display_text(self):
        pass

    def custom_bounds(self):
        if self.position.x < 20.0:
            self.position = vector.Vector2d(20.0, self.position.y)
        
        if self.position.y < 20.0:
            self.position = vector.Vector2d(self.position.x, 20.0)
        
        if self.position.x > SCREEN_WIDTH - 20.0:
            self.position = vector.Vector2d(SCREEN_WIDTH - 20.0, self.position.y)
        
        if self.position.y > SCREEN_HEIGHT - 20.0:
            self.position = vector.Vector2d(self.position.x, SCREEN_HEIGHT - 20.0)

    def die(self):
        self.active = False
        self.kill()


class DamageX2(Gem):
    master_animation_list = animation.Animation()
    
    def __init__(self, position, text_group):
        Gem.__init__(self)
        
        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()  
        self.hitrect = self.rect
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        # UNIQUE VARIABLES
        self.text_group = text_group
        
    def display_text(self):
        temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Double Damage!').image
        help_bubble = infobubble.InfoBubble(temp_image, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        help_bubble.offset = vector.Vector2d(0.0, -100.0)
        self.text_group.add(help_bubble)

    def give_bonus(self):
        self.object_collided_with.damage_bonus += 4 * FRAMES_PER_SECOND
        self.object_collided_with.bullet_damage = 2


class Nova(Gem):
    master_animation_list = animation.Animation()
    
    def __init__(self, position, text_group, effects_group):
        Gem.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.hitrect = self.rect
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        # UNIQUE VARIABLES
        self.text_group = text_group
        self.effects_group = effects_group
        
    def display_text(self):
        temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Nova!').image
        help_bubble = infobubble.InfoBubble(temp_image, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        help_bubble.offset = vector.Vector2d(0.0, -100.0)
        self.text_group.add(help_bubble)

    def give_bonus(self):
        stars_to_create = 15

        while stars_to_create:
            stars_to_create -= 1

            temp_bullet = bullet.Bullet(self.position,
                                        (BULLET_SPEED, 0),
                                        self.effects_group,
                                        0,
                                        BOUND_STYLE_KILL,
                                        COLLIDE_STYLE_NOVA)
            
            temp_bullet.set_life_timer(13)
            temp_bullet.animation_list.play('Nova')
            temp_bullet.velocity.set_angle(stars_to_create * 24)
            
            # Bullet damage doesn't matter since these bullets automatically 
            # kill whatever they touch
            temp_bullet.set_owner(self.object_collided_with)
            self.object_collided_with.bullet_group.add(temp_bullet)


class Reflect(Gem):
    master_animation_list = animation.Animation()

    def __init__(self, position, text_group):
        Gem.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect() 
        self.hitrect = self.rect
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        # UNIQUE VARIABLES
        self.text_group = text_group

    def display_text(self):
        temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Reflect!').image
        help_bubble = infobubble.InfoBubble(temp_image, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        help_bubble.offset = vector.Vector2d(0.0, -100.0)
        self.text_group.add(help_bubble)

    def give_bonus(self):
        self.object_collided_with.bullet_bound_style = BOUND_STYLE_REFLECT
        self.object_collided_with.bullet_collide_style = COLLIDE_STYLE_REFLECT
        self.object_collided_with.reflect_bonus += 2.5 * FRAMES_PER_SECOND


class DualShot(Gem):
    master_animation_list = animation.Animation()

    def __init__(self, position, text_group):
        Gem.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect() 
        self.hitrect = self.rect
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        # UNIQUE VARIABLES
        self.text_group = text_group

    def display_text(self):
        temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Dual Shot!').image
        help_bubble = infobubble.InfoBubble(temp_image, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        help_bubble.offset = vector.Vector2d(0.0, -100.0)
        self.text_group.add(help_bubble)

    def give_bonus(self):
        self.object_collided_with.dual_shot += 3 * FRAMES_PER_SECOND


class FastShot(Gem):
    master_animation_list = animation.Animation()

    def __init__(self, position, text_group):
        Gem.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect() 
        self.hitrect = self.rect
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        # UNIQUE VARIABLES
        self.text_group = text_group

    def display_text(self):
        temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Fast Shot!').image
        help_bubble = infobubble.InfoBubble(temp_image, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        help_bubble.offset = vector.Vector2d(0.0, -100.0)
        self.text_group.add(help_bubble)

    def give_bonus(self):
        self.object_collided_with.fast_shot += 3 * FRAMES_PER_SECOND
        self.object_collided_with.resetFireTimer = 1
