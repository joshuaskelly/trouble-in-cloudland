import random

from core import actor, balloon, gem, particle
from core.actor import *
from utils import utility


class Enemy(actor.Actor):
    death_sound = None

    def __init__(self):
        actor.Actor.__init__(self)

        # COMMON VARIABLES
        self.actor_type = ACTOR_TYPE_ENEMY
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = -32, -32, (SCREEN_WIDTH + 32), (SCREEN_HEIGHT + 32)
        self.can_collide = True
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero
        self.boss_fight = False
        self.drop_item = False
        self.drop_balloon = False
        self.powerup_group = []

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)

    def item_drop(self):
        if self.drop_item:
            self.powerup_group.add(
                gem.Nova(self.position, self.text_group, self.effects_group))

        elif self.boss_fight:
            random_number = int(random.random() * 25)
            
            if not random_number:
                self.powerup_group.add(
                    gem.Reflect(self.position, self.text_group))
            elif random_number == 1:
                self.powerup_group.add(
                    gem.DamageX2(self.position, self.text_group))
            elif random_number == 2:
                self.powerup_group.add(
                    gem.FastShot(self.position, self.text_group))
            elif random_number == 3:
                self.powerup_group.add(
                    gem.DualShot(self.position, self.text_group))

        elif self.object_collided_with.owner.combo_bonus:
            self.object_collided_with.owner.increment_score(100, self.position, self.text_group)

            random_number = int(random.random() * 6 + 1)
    
            if random_number == 1:
                random_number = int(random.random() * 100 + 1)

                if random_number <= 25:
                    self.powerup_group.add(
                        balloon.Bonus250(self.position, self.text_group))
                elif random_number <= 40:
                    self.powerup_group.add(
                        balloon.Bonus500(self.position, self.text_group))
                elif random_number <= 50:
                    self.powerup_group.add(
                        balloon.BonusX2(self.position, self.text_group))
                elif random_number <= 60:
                    self.powerup_group.add(
                        gem.DualShot(self.position, self.text_group))
                elif random_number <= 70:
                    self.powerup_group.add(
                        gem.FastShot(self.position, self.text_group))
                elif random_number <= 80:
                    self.powerup_group.add(
                        gem.DamageX2(self.position, self.text_group))
                elif random_number <= 90:
                    self.powerup_group.add(
                        gem.Reflect(self.position, self.text_group))
                else:
                    self.powerup_group.add(
                        gem.Nova(self.position, self.text_group, self.effects_group))

        else:
            self.object_collided_with.owner.increment_score(100, self.position, self.text_group)

            random_number = int(random.random() * 6 + 1)
    
            if random_number == 1:
                random_number = int(random.random() * 100 + 1)

                if random_number <= 25:
                    self.powerup_group.add(
                        balloon.Bonus250(self.position, self.text_group))
                elif random_number <= 40:
                    self.powerup_group.add(
                        balloon.Bonus500(self.position, self.text_group))
                elif random_number <= 45:
                    self.powerup_group.add(
                        balloon.BonusCombo(self.position, self.text_group))
                elif random_number <= 50:
                    self.powerup_group.add(
                        balloon.BonusX2(self.position, self.text_group))
                elif random_number <= 60:
                    self.powerup_group.add(
                        gem.DualShot(self.position, self.text_group))
                elif random_number <= 70:
                    self.powerup_group.add(
                        gem.FastShot(self.position, self.text_group))
                elif random_number <= 80:
                    self.powerup_group.add(
                        gem.DamageX2(self.position, self.text_group))
                elif random_number <= 90:
                    self.powerup_group.add(
                        gem.Reflect(self.position, self.text_group))
                else:
                    self.powerup_group.add(
                        gem.Nova(self.position, self.text_group, self.effects_group))

    def die(self):
        utility.play_sound(self.death_sound)
        particle.DeathEmitter(self.position, self.effects_group).run()
        self.item_drop()
        self.active = False
        self.emitter = None
        self.death_emitter = None
        self.kill()
        del self
