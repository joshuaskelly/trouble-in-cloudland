import animation
import utility
import pygame
import actor
import bullet
import vector
import random
import text
import copy
import particle
import infoBubble

from actor import *


def loadData():
    Player.MasterAnimationList.buildAnimation("Idle", ["kuunIdle"])
    Player.MasterAnimationList.buildAnimation("Fire", ["kuunShoot"])
    Player.MasterAnimationList.buildAnimation("HurtIdle", ["kuunIdle","blank"])
    Player.MasterAnimationList.buildAnimation("HurtFire", ["kuunShoot","blank"])
    Player.MasterAnimationList.buildAnimation("Die", ["kuunDie"])

    Player.NUM_OW_SOUNDS = 2 #plus one for a total of 3
    Player.loseLifeSound.append(utility.loadSound("ow1"))
    Player.loseLifeSound.append(utility.loadSound("ow2"))
    Player.loseLifeSound.append(utility.loadSound("ow3"))

    Player.NUM_FIRE_SOUNDS = 2 #plus one for total of 3
    Player.fireSound.append(utility.loadSound("shot1"))
    Player.fireSound.append(utility.loadSound("shot2"))
    Player.fireSound.append(utility.loadSound("shot3"))

    Player.deathSound.append(utility.loadSound("playerDeath1"))
    Player.deathSound.append(utility.loadSound("playerDeath2"))
    Player.deathSound.append(utility.loadSound("playerDeath3"))

    Player.extraLifeSound = utility.loadSound("extraLife")


class Player(actor.Actor):
    deathSound = []
    fireSound = []
    loseLifeSound = []
    MasterAnimationList = animation.Animation()

    def __init__(self, bullet_group, effects_group, life_board, score_board):
        """Player character class"""

        # COMMON VARIABLES
        actor.Actor.__init__(self)
        self.actorType = ACTOR_PLAYER
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_REFLECT
        self.bounds = [0 + 46, 0 + 60, SCREEN_WIDTH - 46, SCREEN_HEIGHT - 32]
        self.canCollide = True
        self.hitrect = pygame.Rect(0, 0, 80, 90)
        self.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        self.velocity = vector.Vector2d.zero

        # UNIQUE VARIABLES
        self.bullet_speed = BULLET_SPEED
        self.default_fire_timer = 2
        self.reset_fire_timer = self.default_fire_timer
        self.fire_timer = self.reset_fire_timer
        self.max_speed = 54
        self.hitrect_offset_y = -15
        self.score = 0
        self.lives = 3
        self.stun_timer = 0
        self.life_board = life_board
        self.score_board = score_board
        self.life_board.set_text('x' + str(self.lives))
        self.score_board.set_text(self.score)
        self.next_bonus = 50000
        
        self.dying = 0
        self.dead = False

        # BONUS VARIABLES
        self.damage_bonus = 0
        self.reflect_bonus = 0
        self.dual_shot = 0
        self.fast_shot = 0
        self.point_bonus = 0
        self.combo_bonus = 0
        self.combo_kills = 0

        # BULLET VARIABLES
        self.bullet_damage = 1
        self.bullet_bound_style = BOUND_STYLE_KILL
        self.bullet_collide_style = COLLIDE_STYLE_HURT
        self.bullet_group = bullet_group
        self.effects_group = effects_group

        # SOUND VARIABLES
        self.current_sound = 0

    def actor_update(self):
        if self.lives <= 0:
            self.active = False
            self.velocity -= vector.Vector2d(0.0, -0.3)
            self.die()
            return
        
        if not self.damage_bonus:
            self.bullet_damage = 1
        if not self.reflect_bonus:
            self.bullet_bound_style = BOUND_STYLE_KILL
            self.bullet_collide_style = COLLIDE_STYLE_HURT
        if not self.fast_shot:
            self.reset_fire_timer = self.default_fire_timer

        if self.point_bonus: self.point_bonus -= 1
        if self.damage_bonus: self.damage_bonus -= 1
        if self.reflect_bonus: self.reflect_bonus -= 1
        if self.dual_shot: self.dual_shot -= 1
        if self.stun_timer: self.stun_timer -= 1
        if self.fast_shot: self.fast_shot -= 1

        if self.combo_bonus:
            self.combo_bonus -= 1

            if not self.combo_bonus:
                combo_counter = 0
                bonus_points = 0

                while combo_counter <= self.combo_kills:
                    combo_counter += 1
                    bonus_points += combo_counter * 25

                self.increment_score_no_text(bonus_points)
                temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Combo Points:" + str(bonus_points) + "!").image
                help_bubble = infoBubble.infoBubble(temp_image, self,1.5 * FRAMES_PER_SECOND)
                help_bubble.offset = vector.Vector2d(0.0, -100.0)
                self.bullet_group.add(help_bubble)
                self.combo_kills = 0

        self.fire_timer -= 1
        self.velocity *= .95

        if not self.active:
            self.active = True

        if not self.fire_timer:
            self.animation_list.stop("Idle", self.animation_list.current_frame)

        if self.stun_timer:
            self.animation_list.play("HurtIdle", self.animation_list.current_frame)
            
    def die(self):
        if self.dying == 0:
            death_type = int(random.random() * 3)
            
            if death_type == 0:
                temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Blast!").image
                utility.play_sound(self.deathSound[0], OW_CHANNEL)
            elif death_type == 1:
                temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Oh No!").image
                utility.play_sound(self.deathSound[1], OW_CHANNEL)
            elif death_type == 2:
                temp_image = text.TextSurface(FONT_PATH, 30,FONT_COLOR, "Bother!").image
                utility.play_sound(self.deathSound[2], OW_CHANNEL)
            
            self.animation_list.play("Die")
            self.bounds = [-1000, -1000, SCREEN_WIDTH + 1000, SCREEN_HEIGHT + 32]
            self.bound_style = BOUND_STYLE_CUSTOM
                
            help_bubble = infoBubble.infoBubble(temp_image, self, 5 * FRAMES_PER_SECOND)
            help_bubble.offset = vector.Vector2d(0.0, -100.0)
            self.bullet_group.add(help_bubble)
        
        self.dying += 1
        
        if settings_list[PARTICLES] and not self.dying % 2:
            puffs_to_create = 4
            
            while puffs_to_create:
                puffs_to_create -= 1
                temp_puff = particle.smokeParticle(self.position, (1, 0))
                temp_puff.velocity.setAngle(359 * random.random())
                self.effects_group.add(temp_puff)
                
    def custom_bounds(self):
        self.dead = True

    def hurt(self, value):
        if self.stun_timer <= 0:
            self.animation_list.play("HurtIdle", self.animation_list.current_frame)
            self.lives -= value
            sound_to_play = random.randint(0, 2)

            if self.lives != 0:
                utility.play_sound(self.loseLifeSound[sound_to_play], OW_CHANNEL)

            self.life_board.set_text('x' + str(self.lives))
            self.stun_timer = 1.5 * FRAMES_PER_SECOND

    def increment_score_no_text(self, value):
        self.score += value
        self.score_board.set_text(self.score)
        
        if self.score > self.next_bonus:
            utility.play_sound(self.extraLifeSound, OW_CHANNEL)
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Extra Life!").image
            
            help_bubble = infoBubble.infoBubble(temp_image, self, 1.5 * FRAMES_PER_SECOND)
            help_bubble.offset = vector.Vector2d(0.0, -100.0)
            self.effects_group.add(help_bubble)

            self.lives += 1
            self.life_board.set_text('x' + str(self.lives))
            self.next_bonus += 50000

    def increment_score(self, value, textPosition, textGroup):
        if self.combo_bonus and value <= 250:
            self.combo_bonus += int(.2 * FRAMES_PER_SECOND)
            self.combo_kills += 1
            temp_image = text.Text(FONT_PATH, 30, FONT_COLOR, "x" + str(self.combo_kills) + "!").image
            
            help_bubble = infoBubble.infoBubble(temp_image, self, 0.5 * FRAMES_PER_SECOND)
            help_bubble.offset = vector.Vector2d(0.0, -100.0)
            self.bullet_group.add(help_bubble)

        if self.point_bonus:
            value *= 2

        temp_text = text.Text(FONT_PATH, 36, FONT_COLOR, str(value), 15)
        temp_text.set_alignment(CENTER_MIDDLE)
        temp_text.position = vector.Vector2d(textPosition)
        textGroup.add(temp_text)

        self.score += value
        self.score_board.set_text(self.score)
        
        if self.score >= self.next_bonus:
            utility.play_sound(self.extraLifeSound, OW_CHANNEL)
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Extra Life!").image
            
            help_bubble = infoBubble.infoBubble(temp_image, self, 1.5 * FRAMES_PER_SECOND)
            help_bubble.offset = vector.Vector2d(0.0, -100.0)
            textGroup.add(help_bubble)

            self.lives += 1
            self.life_board.set_text('x' + str(self.lives))
            self.next_bonus += 50000

    def fire(self):        
        if self.stun_timer:
            self.animation_list.play("HurtFire", self.animation_list.current_frame)
        else:
            self.animation_list.play("Fire")

        if (self.fire_timer <= 0):
            utility.play_sound(self.fireSound[random.randint(0, 2)], PLAYER_CHANNEL)
            if self.velocity:
                bulletVelocity = vector.Vector2d(self.velocity)
                bulletVelocity.setMagnitude(self.bullet_speed)
                
                newBullet = bullet.Bullet((self.position),
                                          (bulletVelocity),
                                          self.effects_group,
                                          self.bullet_damage,
                                          self.bullet_bound_style,
                                          self.bullet_collide_style)
                newBullet.setOwner(self)
                if self.reflect_bonus and self.damage_bonus:
                    newBullet.animation_list.play("DamageReflect")
                elif self.bullet_collide_style == COLLIDE_STYLE_REFLECT: newBullet.animation_list.play("Reflect")
                elif self.bullet_damage > 1: newBullet.animation_list.play("Damage")

                self.bullet_group.add(newBullet)
                self.fire_timer = self.reset_fire_timer

            if self.dual_shot:
                if self.velocity:
                    bulletVelocity = vector.Vector2d(self.velocity * -1)
                    bulletVelocity.setMagnitude(self.bullet_speed)
                    
                    newBullet = bullet.Bullet((self.position),
                                              (bulletVelocity),
                                              self.effects_group,
                                              self.bullet_damage,
                                              self.bullet_bound_style,
                                              self.bullet_collide_style)
                    newBullet.setOwner(self)
                    if self.reflect_bonus and self.damage_bonus:
                        newBullet.animation_list.play("DamageReflect")
                    elif self.bullet_collide_style == COLLIDE_STYLE_REFLECT: newBullet.animation_list.play("Reflect")
                    elif self.bullet_damage > 1: newBullet.animation_list.play("Damage")

                    self.bullet_group.add(newBullet)
    
    def setVelocity(self, newVelocity):
        self.velocity = newVelocity
        
        if newVelocity.getMagnitude() > self.max_speed:
            self.velocity.setMagnitude(self.max_speed)