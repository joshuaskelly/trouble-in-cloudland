import copy
import random

from core import actor, particle
from core.actor import *


def load_data():
    Bullet.master_animation_list.build_animation('Idle', ['staar0', 'staar1', 'staar2', 'staar3', 'staar4', 'staar5'])
    Bullet.master_animation_list.build_animation('Reflect', ['staar10', 'staar11', 'staar12', 'staar13', 'staar14', 'staar15'])
    Bullet.master_animation_list.build_animation('Damage', ['staar20', 'staar21', 'staar22', 'staar23', 'staar24', 'staar25'])
    Bullet.master_animation_list.build_animation('DamageReflect', ['staar20', 'staar21', 'staar22', 'staar13', 'staar14', 'staar15'])
    Bullet.master_animation_list.build_animation('Nova', ['staar30', 'staar31', 'staar32', 'staar33', 'staar34', 'staar35'])


class Bullet(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self, position, velocity, effects_group, damage=1, default_bound_style=BOUND_STYLE_KILL, default_collide_style=COLLIDE_STYLE_HURT):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.actor_type = ACTOR_BULLET
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()

        if default_collide_style == COLLIDE_STYLE_NOVA:
            self.bound_style = BOUND_STYLE_NONE
        else:
            self.bound_style = default_bound_style

        self.bounds = -32, -32,SCREEN_WIDTH + 32, SCREEN_HEIGHT + 32
        self.can_collide = False
        self.hitrect = self.rect
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d(velocity)
        self.effects_group = effects_group
        self.owner = self

        # UNIQUE VARIABLES
        self.collide_style = default_collide_style
        self.damage = damage
        self.life_timer = 2 * FRAMES_PER_SECOND
        self.sequence_list = [[0, 1, 2, 3, 4, 5], [0]]

    def actor_update(self):
        if self.collide_style == COLLIDE_STYLE_NOVA:
            self.velocity += self.velocity.get_perpendicular().make_normal() * 5
        
        if not self.life_timer % 3 and settings_list[PARTICLES]:
            temp_particle = particle.StarParticle()
            temp_particle.position = self.position.copy()
            self.effects_group.add(temp_particle)
        
        self.active = True
        self.life_timer -=  1
        
        if self.life_timer == 0:
            self.die()

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_TYPE_BOSS:
            self.object_collided_with.bullet_collide(self)

        elif self.collide_style == COLLIDE_STYLE_HURT:
            if self.object_collided_with.actor_type == ACTOR_TYPE_ENEMY:
                self.object_collided_with.health -= self.damage

            self.die()
         
        elif self.collide_style == COLLIDE_STYLE_REFLECT:
            if self.object_collided_with.actor_type == ACTOR_TYPE_BAAKE:
                if self.position.x < self.object_collided_with.position.x - 64:
                    self.position = vector.Vector2d(self.object_collided_with.position.x - 104, self.position.y)
                    self.velocity *= -1.0, 1.0

                elif self.position.x > self.object_collided_with.position.x + 64:
                    self.position = vector.Vector2d(self.object_collided_with.position.x + 104, self.position.y)
                    self.velocity *= -1.0, 1.0

                if self.position.y < self.object_collided_with.position.y - 32:
                    self.position = vector.Vector2d(self.position.x, self.object_collided_with.position.y - 104)
                    self.velocity *= 1.0, -1.0

                elif self.position.y > self.object_collided_with.position.y + 32:
                    self.position = vector.Vector2d(self.position.x, self.object_collided_with.position.y + 104)
                    self.velocity *= 1.0, -1.0

            else:
                    self.object_collided_with.health -= self.damage
                    self.die()

        elif self.collide_style == COLLIDE_STYLE_NOVA:
            if self.object_collided_with.actor_type == ACTOR_TYPE_ENEMY:
                self.object_collided_with.health = 0
        
        elif self.collide_style == COLLIDE_STYLE_NONE:
            pass
        
    def die(self):
        if self.object_collided_with.actor_type == ACTOR_TYPE_BAAKE:
            if settings_list[PARTICLES]:
                stars_to_create = 1
            
                while stars_to_create:
                    stars_to_create -= 1
                    temp_puff = particle.SmokeParticle(self.position, (1, 0))
                    temp_puff.velocity.set_angle(359 * random.random())
                    self.effects_group.add(temp_puff)

        self.kill()

    def set_owner(self, new_owner):
        self.owner = new_owner
        
    def set_life_timer(self, new_life):
        self.life_timer = new_life
