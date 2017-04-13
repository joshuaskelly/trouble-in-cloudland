import copy
import random

from core import actor
from core.actor import *


def load_data():
    SmokeParticle.master_animation_list.build_animation('Idle', ['ppuff'])
    StarParticle.master_animation_list.build_animation('Idle', ['pstaar0', 'pstaar1', 'pstaar2'])
    HeartParticle.master_animation_list.build_animation('Idle', ['pheart'])
    RainParticle.master_animation_list.build_animation('Idle', ['prain'])


class SmokeParticle(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self, position, velocity):
        actor.Actor.__init__(self)
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.can_collide = False
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d(velocity)
        self.life_timer = int(.5 * FRAMES_PER_SECOND)
        self.speed = 3
        self.velocity.set_magnitude(self.speed)

    def actor_update(self):
        if self.life_timer == 0:
            self.die()
            
        self.life_timer -= 1
        self.velocity += (0.0, -.75)


class StarParticle(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.can_collide = False
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.up
        self.life_timer = int(.15 * FRAMES_PER_SECOND)
        self.speed = 1
        self.velocity.set_magnitude(self.speed)
        
    def actor_update(self):
        if self.life_timer == 0:
            self.die()
            
        self.life_timer -= 1


class HeartParticle(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)
        
        self.name = 'Heart Particle'
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.can_collide = False
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.up
        self.life_timer = int(.5 * FRAMES_PER_SECOND)

    def actor_update(self):
        if self.life_timer == 0:
            self.die()
            
        self.life_timer -= 1


class RainParticle(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.can_collide = False
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = 0, -512, SCREEN_WIDTH, SCREEN_HEIGHT
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.up
        self.life_timer = -1
        
    def actor_update(self):
        if self.life_timer == 0:
            self.die()
            
        self.life_timer -= 1
        self.velocity += 0.0, 2.0


class ParticleEmitter(object):
    def __init__(self, position, position_jitter, effects_group, particle_data, emission_angle, emission_angle_jitter, emission_speed, emission_speed_jitter, emission_rate, emission_count, life_timer=-1):
        self.life_timer = life_timer
        self.particle_data = particle_data
        self.emission_angle = emission_angle
        self.emission_angle_jitter = emission_angle_jitter
        self.emission_speed = emission_speed
        self.emission_speed_jitter = emission_speed_jitter
        self.emission_rate = emission_rate
        self.emission_count = emission_count
        self.offset = vector.Vector2d.zero
        self.emission_vector = vector.Vector2d.up
        self.position = position
        self.position_jitter = position_jitter
        self.mount = None
        self.effects_group = effects_group

    def update(self):
        try:
            if settings_list[PARTICLES]:
                if self.life_timer:
                    if self.mount:
                        self.position = self.mount.position + self.offset
                        
                    if not self.life_timer % self.emission_rate:
                        for particle in self.particle_data:
                            particle_count = self.emission_count
                            while particle_count:
                                self.create_particle(particle)
                                particle_count -= 1
                            
                    self.life_timer -= 1
                
        except:
            pass
        
    def create_particle(self, particle):
        self.emission_vector.set_magnitude(self.emission_speed + (random.random() * 2 * self.emission_speed_jitter) - (self.emission_speed_jitter))
        self.emission_vector.set_angle(self.emission_angle + (random.random() * 2 * self.emission_angle_jitter) - (self.emission_angle_jitter))
        
        if particle == 'heart':
            temp_particle = HeartParticle()
            
        elif particle == 'star':
            temp_particle = StarParticle()

        elif particle == 'puff':
            temp_particle = SmokeParticle((0, 0), (0, 0))
            
        elif particle == 'rain':
            temp_particle = RainParticle()

        temp_particle.position = self.position + (((random.random() * 2.0)-1.0) * self.position_jitter)
        temp_particle.velocity = self.emission_vector.copy()
        
        self.effects_group.add(temp_particle)

    def mount_to(self, object, offset = vector.Vector2d.zero):
        self.mount = object
        self.offset = offset


class DeathEmitter(object):
    def __init__(self, position, particle_group):
        self.particle_group = particle_group
        self.position = vector.Vector2d(position)

    def run(self):
        if settings_list[PARTICLES]:
            particles_to_create = 4
            while particles_to_create:
                temp_velocity = vector.Vector2d(1, 0)
                temp_velocity.set_angle(random.random() * 360)
                temp_velocity.set_magnitude(5.0)
                
                temp_particle = SmokeParticle(self.position, temp_velocity)
                
                self.particle_group.add(temp_particle)
                
                particles_to_create -= 1
