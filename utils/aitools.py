import random

import vector
from settings import *


# Misc Functions


def random_location_on_screen():
    return int(random.random() * SCREEN_HEIGHT), int(random.random() * SCREEN_WIDTH)


def point_off_screen(distance=32):
    screen_side = int(random.random() * 3 + 1) - 1

    if screen_side == LEFT:
        point = vector.Vector2d(-distance, random.random() * SCREEN_HEIGHT)
    elif screen_side == TOP:
        point = vector.Vector2d(random.random() * SCREEN_WIDTH, -distance)
    elif screen_side == RIGHT:
        point = vector.Vector2d(SCREEN_WIDTH + distance, random.random() * SCREEN_HEIGHT)
    elif screen_side == BOTTOM:
        point = vector.Vector2d(random.random() * SCREEN_WIDTH, SCREEN_HEIGHT + distance)

    return point

# Spawning Functions


def spawn_at_point(actor, point):
    actor.position = vector.Vector2d(point)


def spawn_away_from_target(actor, target, distance=256):
    check = False
    
    while not check:
        actor.position = vector.Vector2d((random.random() * actor.bounds[RIGHT]),
                                         (random.random() * actor.bounds[BOTTOM]))
        check = True

        check_distance = actor.position - target.position
        if check_distance.get_magnitude() < distance:
            check = False


def spawn_on_screen(actor):
    """Position the actor randomly on the screen such that their bounds are
    contained within the screen rect"""

    actor.position = vector.Vector2d(((random.random() * (actor.bounds[RIGHT] - actor.bounds[LEFT])) + actor.bounds[LEFT]),
                                     ((random.random() * (actor.bounds[BOTTOM] - actor.bounds[TOP])) + actor.bounds[TOP]))


def spawn_off_screen(actor, distance=32):
    screen_side = int(random.random() * 3 + 1) - 1

    if screen_side == LEFT:
        actor.position = vector.Vector2d(-distance, random.random() * SCREEN_HEIGHT)

    elif screen_side == TOP:
        actor.position = vector.Vector2d(random.random() * SCREEN_WIDTH, -distance)

    elif screen_side == RIGHT:
        actor.position = vector.Vector2d(SCREEN_WIDTH + distance, random.random() * SCREEN_HEIGHT)

    elif screen_side == BOTTOM:
        actor.position = vector.Vector2d(random.random() * SCREEN_WIDTH, SCREEN_HEIGHT + distance)


# AI Styles
def hide(actor, hide_behind, hide_from, offset=128):
    # Find the location that the actor should go to
    goal_location = hide_behind.position
    offset_direction = hide_behind.position - hide_from.position
    offset_direction.make_normal()
    goal_location += (offset_direction * offset)

    # Send the actor to target location
    bearing = goal_location - actor.position

    if bearing.get_magnitude() > actor.speed:
        bearing.set_magnitude(actor.speed)

    actor.velocity = bearing


def go_to_point(actor, point):
    bearing = point - actor.position
    
    if bearing.get_magnitude() > actor.speed:
        bearing.set_magnitude(actor.speed)
    
    actor.velocity = bearing


def go_to_target(actor, target):
    bearing = target.position - actor.position

    if bearing.get_magnitude() > actor.speed:
        bearing.set_magnitude(actor.speed)

    actor.velocity = bearing


def arc_to_point(actor, target_point, degree=1):
    goal_bearing = target_point - actor.position
    goal_bearing.make_normal()
    goal_bearing *= degree

    actor.velocity += goal_bearing
    actor.velocity.set_magnitude(actor.speed)


def cardinal_direction(actor):
    if int(random.random() * 2 + 1) - 1:
        if int(random.random() * 2 + 1) - 1:
            actor.velocity = vector.Vector2d(actor.speed, 0.0)

        else:
            actor.velocity = vector.Vector2d(-actor.speed, 0.0)

    else:
        if int(random.random() * 2 + 1) - 1:
            actor.velocity = vector.Vector2d(0.0, actor.speed)

        else:
            actor.velocity = vector.Vector2d(0.0, -actor.speed)


# AI tools
def get_closest(actor, target_group, target_actors=None):
    temp_group1 = []
    temp_group2 = []
    temp_group3 = []

    search_groups = []

    try:
        for subGroup in target_group:
            for actor in target_group:
                pass

            search_groups.append(subGroup)
    
        for group in search_groups:
            if target_actors:
                try:
                    for target in group:
                        for actor in target_actors:
                            if target.actor_type == actor:
                                temp_group2.append(target)

                except:
                    try:
                        if target.actor_type == target_actors:
                            temp_group2.append(target)

                    except:
                        pass
            else:
                for target in target_group:
                    temp_group2.append(target)
    
    except:
        if target_actors:
            try:
                for target in target_group:
                    for actor in target_actors:
                        if target.actor_type == actor:
                            temp_group2.append(target)

            except:
                if target.actor_type == target_actors:
                    temp_group2.append(target)

        else:
            for target in target_group:
                temp_group2.append(target)

    iteration = 1
    closest_distance = 100000
    closest_object = None
    
    while True:
        target_found = False

        for target in temp_group2:
            if abs(target.position.x - actor.position.x) < (SCREEN_WIDTH / iteration):
                if abs(target.position.y - actor.position.y) < (SCREEN_HEIGHT / iteration):
                    target_found = True
                    temp_group1.append(target)

        if iteration == 1 and not target_found:
            return actor

        elif iteration == 8 or not target_found:
            for target in temp_group3:
                target_distance = target.position - actor.position

                if closest_distance > target_distance.get_magnitude():
                    closest_distance = target_distance.get_magnitude()
                    closest_object = target

            temp_group1 = []
            temp_group2 = []
            temp_group3 = []

            # TODO: Should this return closest_object?
            return target

        else:
            temp_group3 = temp_group2
            temp_group2 = temp_group1
            temp_group1 = []

        iteration += 1
