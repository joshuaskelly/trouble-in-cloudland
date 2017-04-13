import copy
import random

from core import actor, particle
from core.actor import *
from enemies import yurei
from ui import icon, infobubble
from utils import aitools, utility


def load_data():
    BossTut.music = utility.load_sound('bossMusic')
    BossTut.bullet_sound = utility.load_sound('baakeHit')
    BossTut.hurt_sound = utility.load_sound('hurtBoss')
    BossTut.how_to_kill = utility.load_image('howToBoss1')
    BossTut.master_animation_list.build_animation('idle', ['boss1'])
    BossTut.master_animation_list.build_animation('hurt', ['boss1', 'boss1', 'boss1_1', 'boss1_1'])

    BaakeBoss.music = utility.load_sound('bossMusic')
    BaakeBoss.bullet_sound = utility.load_sound('baakeHit')
    BaakeBoss.hurt_sound = utility.load_sound('hurtBoss')
    BaakeBoss.how_to_kill = utility.load_image('howToBoss1')
    BaakeBoss.master_animation_list.build_animation('idle', ['boss0'])
    BaakeBoss.master_animation_list.build_animation('hurt', ['boss0', 'boss0', 'boss0_1', 'boss0_1'])
    
    MoonoBoss.music = utility.load_sound('bossMusic')
    MoonoBoss.bullet_sound = utility.load_sound('baakeHit')
    MoonoBoss.hurt_sound = utility.load_sound('hurtBoss')
    MoonoBoss.shield_break = utility.load_sound('shieldBreak')
    MoonoBoss.shield_restore = utility.load_sound('shieldRestore')
    MoonoBoss.how_to_kill = utility.load_image('howToBoss3')
    MoonoBoss.master_animation_list.build_animation('idle', ['boss2idle_0', 'boss2idle_1', 'boss2idle_2', 'boss2idle_3', 'boss2idle_4', 'boss2idle_5', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0', 'boss2idle_0'])
    MoonoBoss.master_animation_list.build_animation('vulnerable', ['boss2v'])
    MoonoBoss.master_animation_list.build_animation('hurt', ['boss2_1'])
    

####################################################
"""    """    """    MOONO BOSS    """    """    """
####################################################
####################################################
"""    """    """    MOONO BOSS    """    """    """
####################################################


class MoonoBoss(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self, world, target, group_list):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.actor_type = ACTOR_TYPE_BOSS
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = self.bounds = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
        self.can_collide = True
        self.hitrect = pygame.Rect(0, 0, 162, 148)
        self.position = vector.Vector2d(SCREEN_WIDTH + 32, SCREEN_HEIGHT / 2)
        self.velocity = vector.Vector2d(0.0, 0.0)
        
        # UNIQUE VARIABLES
        self.speed = 3
        self.health = (world.level + 1) * 25
        self.life_timer = 0
        self.sequence_list = [[0]]
        self.stunned = 0
        self.world = world
        self.target = target
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.enemy_group = group_list[ENEMY_GROUP]
        self.gave_bonus = False

        # AI VARIABLES
        self.charging = False
        self.time_until_charge = 0
        self.spinning = False
        self.time_until_spin = 0

    def actor_update(self):
        utility.play_music(self.music, True)

        if not self.active and self.health > 0:
            self.active = True

        if self.life_timer <= 30 * FRAMES_PER_SECOND and self.health == (self.world.level + 1) * 25:
            if self.life_timer == 30 * FRAMES_PER_SECOND:
                temp_image = self.how_to_kill
                help_bubble = infobubble.InfoBubble(temp_image, self.target, 5 * FRAMES_PER_SECOND)
                help_bubble.offset = vector.Vector2d(0.0, -100.0)
                self.text_group.add(help_bubble)

            self.life_timer += 1

        if self.active:
            if self.stunned:
                if self.charging:
                    self.speed -= 0.2
                    if self.speed <= 1.75:
                        self.speed = 1.75
                        self.charging = False
                        self.time_until_charge = 10 * FRAMES_PER_SECOND
                
                    self.velocity.make_normal()
                    self.velocity *= self.speed

                self.stunned -= 1
                self.animation_list.play('vulnerable')
                
                if not self.stunned:
                    utility.play_sound(self.shieldRestore, PICKUP_CHANNEL)
                    self.animation_list.play('idle')
                
            else:
                self.current_sequence = 0
                self.process_ai()

        if self.health <= 0:
            self.active = False
            self.die()
            
            if not self.gave_bonus:
                self.world.give_bonus()
                self.gave_bonus = True

    def process_ai(self):
        if self.charging:
            self.speed -= 0.2

            if self.speed <= 2:
                self.speed = 2
                self.charging = False
                self.bound_style = BOUND_STYLE_CUSTOM
                self.time_until_charge = 6 * FRAMES_PER_SECOND
            
            aitools.go_to_target(self, self.target)

        elif self.spinning:
            self.speed += 0.2
            
            if self.speed >= 40:
                self.speed = 15
                self.charging = True
                self.spinning = False
                self.time_until_spin = 7 * FRAMES_PER_SECOND
            
            self.velocity += self.velocity.get_perpendicular().make_normal()
            self.velocity = self.velocity.make_normal() * self.speed

        elif self.health <= (self.world.level + 1) * 7:
            if not self.time_until_charge:
                self.charge()

            elif not self.time_until_spin:
                self.spin()

            else:
                aitools.go_to_target(self, self.target)

        elif self.health <= (self.world.level + 1) * 14:
            if not self.time_until_charge:
                self.charge()

            else:
                aitools.go_to_target(self, self.target)

        else:
            aitools.go_to_target(self, self.target)

    def charge(self):
        self.charging = True
        self.speed = 11

        aitools.go_to_target(self, self.target)
        self.bound_style = BOUND_STYLE_REFLECT

    def spin(self):
        self.spinning = True
        self.bound_style = BOUND_STYLE_REFLECT

    def hurt(self,damage):
        self.health -= damage
        self.animation_list.play('hurt')
        utility.play_sound(self.hurt_sound, BOSS_CHANNEL)

        if self.health <= 0:
            for actor in self.enemy_group:
                actor.S = True

    def die(self):
        self.velocity[1] += .1
        if self.bound_style == BOUND_STYLE_REFLECT:
            self.bound_style = BOUND_STYLE_CUSTOM

        self.stunned -= 1
        self.world.pause_spawning = 1 * FRAMES_PER_SECOND

        if settings_list[PARTICLES] and not self.stunned % 2:
            puffs_to_create = 4
            
            while puffs_to_create and settings_list[PARTICLES]:
                puffs_to_create -= 1
                temp_puff = particle.SmokeParticle(self.position, (1, 0))
                temp_puff.velocity.set_angle(359 * random.random())
                self.effects_group.add(temp_puff)

    def bullet_collide(self, bullet):
        if not self.stunned:
            utility.play_sound(self.bullet_sound, BAAKE_CHANNEL)

            if bullet.collide_style == COLLIDE_STYLE_HURT:
                bullet.die()
            
            elif bullet.collide_style == COLLIDE_STYLE_REFLECT:
                if bullet.position.x < self.position.x - 64:
                    bullet.position = vector.Vector2d(self.position.x - 112, bullet.position.y)
                    bullet.velocity *= (-1.0, 1.0)

                elif bullet.position.x > self.position.x + 64:
                    bullet.position = vector.Vector2d(self.position.x + 112, bullet.position.y)
                    bullet.velocity *= (-1.0, 1.0)

                if bullet.position.y < self.position.y - 64:
                    bullet.position = vector.Vector2d(bullet.position.x, self.position.y - 14)
                    bullet.velocity *= (1.0, -1.0)

                elif bullet.position.y > self.position.y + 64:
                    bullet.position = vector.Vector2d(bullet.position.x, self.position.y + 140)
                    bullet.velocity *= (1.0, -1.0)
    
            elif bullet.collide_style == COLLIDE_STYLE_NOVA:
                utility.play_sound(self.shieldBreak, BAAKE_CHANNEL)
                self.stunned = 2 * FRAMES_PER_SECOND
                self.animation_list.play('vulnerable')
                
                stars_to_create = 15
                
                while stars_to_create:
                    stars_to_create -= 1
                    temp_bullet = particle.StarParticle()
                    temp_vector = vector.Vector2d(120, 0)
                    temp_vector.set_angle(stars_to_create * 24)
                    temp_bullet.position = vector.Vector2d(self.position + temp_vector)
                    temp_bullet.life_timer = .5 * FRAMES_PER_SECOND
                    temp_bullet.velocity = vector.Vector2d(3.0, 0.0)
                    temp_bullet.velocity.set_angle(stars_to_create * 24)

                    self.effects_group.add(temp_bullet)
        
        elif bullet.collide_style != COLLIDE_STYLE_NOVA:
                bullet.die()
                self.hurt(1)

    def custom_bounds(self):
        if self.health <= 0:
            self.kill()

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER and not self.stunned:
            self.object_collided_with.hurt(1)

####################################################
"""    """    """    BAAKE BOSS    """    """    """
####################################################
####################################################
"""    """    """    BAAKE BOSS    """    """    """
####################################################


class BaakeBoss(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self, world, target, group_list):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.actor_type = ACTOR_TYPE_BOSS
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -64, -64, SCREEN_WIDTH + 64, SCREEN_HEIGHT + 64
        self.can_collide = True
        self.hitrect = pygame.Rect(0, 0, 140, 210)
        self.position = vector.Vector2d(-32, SCREEN_HEIGHT / 2)
        self.velocity = vector.Vector2d(0.0, 0.0)
        
        # UNIQUE VARIABLES
        self.speed = 1.75
        self.health = world.level + 2
        self.life_timer = 0
        self.sequence_list = [[0], [0, 0, 1, 1]]
        self.stunned = 0
        self.world = world
        self.target = target
        self.group_list = group_list
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.enemy_group = group_list[ENEMY_GROUP]
        self.eye = icon.Icon('boss0_eye')
        self.text_group.add(self.eye)
        self.gave_bonus = False
        self.current_sequence = 1

        #  AI VARIABLES
        self.charging = False
        self.time_until_charge = 0
        
        #  Additional Challenges
        self.summoned_yurei = False

    def actor_update(self):
        utility.play_music(self.music, True)
        self.place_eye()

        if self.life_timer <= 30 * FRAMES_PER_SECOND and self.health == self.world.level+ 2:
            if self.life_timer == 30 * FRAMES_PER_SECOND:
                temp_image = self.how_to_kill
                help_bubble = infobubble.InfoBubble(temp_image, self.target, 5 * FRAMES_PER_SECOND)
                help_bubble.offset = vector.Vector2d(0.0, -100.0)
                self.text_group.add(help_bubble)

            self.life_timer += 1
            
        if not self.active and self.health > 0:
            self.active = True

        if self.active:
            if self.stunned:
                if self.charging:
                    self.speed -= 0.2
                    if self.speed <= 1.75:
                        self.speed = 1.75
                        self.charging = False
                        self.time_until_charge = 6 * FRAMES_PER_SECOND
                
                    self.velocity.make_normal()
                    self.velocity *= self.speed
                
                self.current_sequence = 1
                self.stunned -= 1

                if not self.stunned:
                    self.text_group.add(self.eye)
                    self.animation_list.play('idle')

                if not self.stunned % 4:
                    puffs_to_create = 4
                    
                    while puffs_to_create and settings_list[PARTICLES]:
                        puffs_to_create -= 1
                        temp_puff = particle.SmokeParticle(self.position, (1, 0))
                        temp_puff.velocity.set_angle(359 * random.random())
                        self.effects_group.add(temp_puff)

            else:
                self.current_sequence = 0
                self.process_ai()

        if self.health <= 0:
            self.active = False
            self.die()
            
            if not self.gave_bonus:
                self.world.give_bonus()
                self.gave_bonus = True

    def place_eye(self):
        self.eye.position[0] = self.position[0]
        self.eye.position[1] = self.position[1] - 10
        self.eye.position = (self.target.position - self.eye.position).make_normal() * 10
        self.eye.position += self.position
        self.eye.position[1] -= 10

    def bullet_collide(self, bullet):
        utility.play_sound(self.bullet_sound, BAAKE_CHANNEL)

        if bullet.collide_style == COLLIDE_STYLE_HURT:
            bullet.die()
        
        elif bullet.collide_style == COLLIDE_STYLE_REFLECT:
            if bullet.position.x < self.position.x - 64:
                bullet.position = vector.Vector2d(self.position.x - 112, bullet.position.y)
                bullet.velocity *= (-1.0, 1.0)

            elif bullet.position.x > self.position.x + 64:
                bullet.position = vector.Vector2d(self.position.x + 112, bullet.position.y)
                bullet.velocity *= (-1.0, 1.0)

            if bullet.position.y < self.position.y - 64:
                bullet.position = vector.Vector2d(bullet.position.x, self.position.y - 14)
                bullet.velocity *= (1.0, -1.0)

            elif bullet.position.y > self.position.y + 64:
                bullet.position = vector.Vector2d(bullet.position.x, self.position.y + 140)
                bullet.velocity *= (1.0, -1.0)

        elif bullet.collide_style == COLLIDE_STYLE_NOVA:
            if not self.stunned:
                self.stunned = 2 * FRAMES_PER_SECOND
                self.hurt(1)
                self.eye.kill()
    
    def hurt(self, damage):
        self.health -= damage
        utility.play_sound(self.hurt_sound, BOSS_CHANNEL)
        self.animation_list.play('hurt')

        if self.health <= self.world.level and self.health != 0:
            self.enemy_group.add(yurei.Yurei(self.group_list))

        if self.health <= 0:
            for actor in self.enemy_group:
                actor.leave_screen = True

    def process_ai(self):
        if self.health <= self.world.level + 1:
            if self.charging:
                self.speed -= 0.2
                if self.speed <= 1.75:
                    self.speed = 1.75
                    self.charging = False
                    self.text_group.add(self.eye)
                    self.time_until_charge = 7 * FRAMES_PER_SECOND
            else:
                if not self.time_until_charge:
                    self.charging = True
                    self.speed = 10
                    self.eye.kill()
                
                self.time_until_charge -= 1
                aitools.go_to_target(self, self.target)

        else:
            aitools.go_to_target(self, self.target)

    def die(self):
        self.stunned -= 1
        self.velocity[1] += .1
        self.world.pause_spawning = 1 * FRAMES_PER_SECOND

        if settings_list[PARTICLES] and not self.stunned % 2:
            puffs_to_create = 4
            
            while puffs_to_create and settings_list[PARTICLES]:
                puffs_to_create -= 1
                temp_puff = particle.SmokeParticle(self.position, (1, 0))
                temp_puff.velocity.set_angle(359 * random.random())
                self.effects_group.add(temp_puff)

    def custom_bounds(self):
        if self.health <= 0:
            self.kill()
            self.eye.kill()

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            if not self.stunned:
                self.object_collided_with.hurt(1)
            
            if self.object_collided_with.position.x < self.position.x - 64:
                self.object_collided_with.position = vector.Vector2d(self.position.x - 112, self.object_collided_with.position.y)

                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= (-1.0, 1.0)
                       
            elif self.object_collided_with.position.x > self.position.x + 64:
                self.object_collided_with.position = vector.Vector2d(self.position.x + 112, self.object_collided_with.position.y)

                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= (-1.0, 1.0)
                    
            if self.object_collided_with.position.y < self.position.y - 64:
                self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x, self.position.y - 138)

                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= (1.0, -1.0)
                    
            elif self.object_collided_with.position.y > self.position.y + 64:
                self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x, self.position.y + 170)

                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= (1.0, -1.0)


####################################################
"""    """    """     BOSS TUT     """    """    """
####################################################
####################################################
"""    """    """     BOSS TUT     """    """    """
####################################################


class BossTut(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self, world, target, group_list):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.actor_type = ACTOR_TYPE_BOSS
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_REFLECT
        self.bounds = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
        self.can_collide = True
        self.hitrect = pygame.Rect(0, 0, 106, 130)
        self.position = vector.Vector2d(-32, SCREEN_HEIGHT / 2)
        self.velocity = vector.Vector2d.zero
        
        # UNIQUE VARIABLES
        self.target = target
        self.world = world
        self.life_timer = 0
        self.speed = 5
        self.health = self.world.level + 2
        self.sequence_list = [[0]]
        self.stunned = 0
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.enemy_group = group_list[ENEMY_GROUP]
        self.gave_bonus = False

        #  AI VARIABLES
        self.spinning = False
        self.time_until_spin = 0
        self.target_point = None
        self.change_direction = 0
        self.emitter = particle.ParticleEmitter(vector.Vector2d.zero, vector.Vector2d(60.0, 5.0),
                                                self.effects_group,
                                                ['rain'],
                                                270.0, 45.0,
                                                0.0, 0.0,
                                                3.0, 2.0,
                                                -1.0)
        
        self.emitter.mount_to(self, vector.Vector2d(0.0, 50.0))

    def actor_update(self):
        if not self.stunned:
            try:
                self.emitter.update()

            except:
                pass

        utility.play_music(self.music, True)
        if not self.active and self.health > 0:
            self.active = True

        if self.life_timer <= 30 * FRAMES_PER_SECOND and self.health == self.world.level + 2:
            if self.life_timer == 30 * FRAMES_PER_SECOND:
                temp_image = self.how_to_kill
                help_bubble = infobubble.InfoBubble(temp_image, self.target, 5 * FRAMES_PER_SECOND)
                help_bubble.offset = vector.Vector2d(0.0, -100.0)
                self.text_group.add(help_bubble)

            self.life_timer += 1

        if self.active:
            if self.stunned:
                self.stunned -= 1

                if not self.stunned % 4:
                    puffs_to_create = 4
                    
                    while puffs_to_create and settings_list[PARTICLES]:
                        puffs_to_create -= 1
                        temp_puff = particle.SmokeParticle(self.position, (1, 0))
                        temp_puff.velocity.set_angle(359 * random.random())
                        self.effects_group.add(temp_puff)

                if not self.stunned:
                    self.animation_list.play('idle')

            else:
                self.current_sequence = 0
                self.process_ai()

        if self.health <= 0:
            self.active = False
            self.die()
            
            if not self.gave_bonus and self.world.world_name != 'Tutorial':
                self.world.give_bonus()
                self.gave_bonus = True

    def bullet_collide(self, bullet):
        utility.play_sound(self.bullet_sound, BAAKE_CHANNEL)

        if bullet.collide_style == COLLIDE_STYLE_HURT:
            bullet.die()
        
        elif bullet.collide_style == COLLIDE_STYLE_REFLECT:
            if bullet.position.x < self.position.x - 64:
                bullet.position = vector.Vector2d(self.position.x - 112, bullet.position.y)
                bullet.velocity *= -1.0, 1.0

            elif bullet.position.x > self.position.x + 64:
                bullet.position = vector.Vector2d(self.position.x + 112, bullet.position.y)
                bullet.velocity *= -1.0, 1.0

            if bullet.position.y < self.position.y - 64:
                bullet.position = vector.Vector2d(bullet.position.x, self.position.y - 14)
                bullet.velocity *= 1.0, -1.0

            elif bullet.position.y > self.position.y + 64:
                bullet.position = vector.Vector2d(bullet.position.x, self.position.y + 140)
                bullet.velocity *= 1.0, -1.0

        elif bullet.collide_style == COLLIDE_STYLE_NOVA:
            if not self.stunned:
                self.stunned = 2 * FRAMES_PER_SECOND
                self.hurt(1)

    def hurt(self, damage):
        self.health -= damage
        self.animation_list.play('hurt')
        utility.play_sound(self.hurt_sound, BOSS_CHANNEL)

        if self.health <= 0:
            for actor in self.enemy_group:
                actor.leave_screen = True

    def process_ai(self):
        if self.health <= self.world.level:
            if self.spinning:
                self.bound_style = BOUND_STYLE_NONE
                self.speed += 0.15

                if self.speed > 25:
                    self.spinning = False
                    self.speed = 5
                    self.time_until_spin = 8 * FRAMES_PER_SECOND
                    self.bound_style = BOUND_STYLE_REFLECT
            
                self.velocity += self.velocity.get_perpendicular().make_normal()
                self.velocity = self.velocity.make_normal() * self.speed

            else:
                if not self.time_until_spin:
                    self.spinning = True
                
                else:
                    self.standard_behavior()

                self.time_until_spin -= 1

        else:
            self.standard_behavior()

    def standard_behavior(self):
        if not self.change_direction:
            self.target_point = vector.Vector2d(random.randint(int(self.target.position[0] - 300), int(self.target.position[0] + 300)), random.randint(int(self.target.position[1] - 300), int(self.target.position[1] + 300)))
            self.change_direction = 30

        self.change_direction -= 1
        aitools.arc_to_point(self, self.target_point, 0.5)

    def die(self):
        self.emitter = None
        
        if self.world.world_name == 'Tutorial':
            self.world.boss_dead = True

        self.velocity[1] += .1
        self.bound_style = BOUND_STYLE_CUSTOM

        self.stunned -= 1
        self.world.pause_spawning = 1 * FRAMES_PER_SECOND

        if settings_list[PARTICLES] and not self.stunned % 2:
            puffs_to_create = 4
            
            while puffs_to_create and settings_list[PARTICLES]:
                puffs_to_create -= 1
                temp_puff = particle.SmokeParticle(self.position, (1, 0))
                temp_puff.velocity.set_angle(359 * random.random())
                self.effects_group.add(temp_puff)

    def custom_bounds(self):
        if self.health <= 0:
            self.kill()

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            if not self.stunned:
                self.object_collided_with.hurt(1)
            
            if self.object_collided_with.position.x < self.position.x - 64:
                self.object_collided_with.position = vector.Vector2d(self.position.x - 112, self.object_collided_with.position.y)

                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= (-1.0, 1.0)
                       
            elif self.object_collided_with.position.x > self.position.x + 64:
                self.object_collided_with.position = vector.Vector2d(self.position.x + 112, self.object_collided_with.position.y)

                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= (-1.0, 1.0)
                    
            if self.object_collided_with.position.y < self.position.y - 64:
                self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x, self.position.y - 138)

                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= (1.0, -1.0)
                    
            elif self.object_collided_with.position.y > self.position.y + 64:
                self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x, self.position.y + 170)

                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= (1.0, -1.0)
