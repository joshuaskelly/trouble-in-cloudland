import random

from utils import vector
from utils.settings import *


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
def get_closest(search_actor, test_group_list, actor_type_list=None):
    """Find the closest actor.
    
    Arguments:
    search_actor: The actor that you want to find the closest other actor
    test_group_list: The actor groups that you want to test, expects a list of lists
    actors_type_list: The actor types you want to test, expects a list of actor types
    
    Returns closest actor or self
    """
    test_actor_list = []

    if not actor_type_list:
        for test_group in test_group_list:
            for test_actor in test_group:
                test_actor_list.append(test_actor)
    else:
        for test_group in test_group_list:
            for test_actor in test_group:
                if test_actor.actor_type in actor_type_list:
                    test_actor_list.append(test_actor)

    closest_distance = 100000
    closest_object = None

    if not test_actor_list:
        return search_actor

    for test_actor in test_actor_list:
        test_actor_distance = test_actor.position - search_actor.position

        if closest_distance > test_actor_distance.get_magnitude():
            closest_distance = test_actor_distance.get_magnitude()
            closest_object = test_actor

    return closest_object
