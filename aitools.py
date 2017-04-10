import pygame
import math
import random
import utility
import vector

from settings import *
"""Misc Functions"""
def randomLocationOnScreen():
    return (int(random.random() * SCREEN_HEIGHT), int(random.random() * SCREEN_WIDTH))

def pointOffScreen(distance = 32):
    screenSide = int(random.random() * 3 + 1) - 1

    if screenSide == LEFT:
        point = vector.Vector2d(-distance, random.random() * SCREEN_HEIGHT)
    elif screenSide == TOP:
        point = vector.Vector2d(random.random() * SCREEN_WIDTH, -distance)
    elif screenSide == RIGHT:
        point = vector.Vector2d(SCREEN_WIDTH + distance, random.random() * SCREEN_HEIGHT)
    elif screenSide == BOTTOM:
        point = vector.Vector2d(random.random() * SCREEN_WIDTH, SCREEN_HEIGHT + distance)

    return point

"""Spawning Funcitons"""
def spawnAtPoint(object, point):
    object.position = vector.Vector2d(point)

def spawnAwayFromTarget(object, target, distance = 256):

    check = False
    
    while not check:
        object.position = vector.Vector2d((random.random() * object.bounds[RIGHT]),
                                          (random.random() * object.bounds[BOTTOM]))
        check = True

        checkDistance = object.position - target.position
        if checkDistance.getMagnitude() < distance:
            check = False



def spawnOnScreen(object):
    
    object.position = vector.Vector2d(((random.random() * (object.bounds[RIGHT] - object.bounds[LEFT])) + object.bounds[LEFT]),
                                      ((random.random() * (object.bounds[BOTTOM]- object.bounds[TOP])) + object.bounds[TOP]))



def spawnOffScreen(object, distance = 32):

    screenSide = int(random.random() * 3 + 1) - 1

    if screenSide == LEFT:
        object.position = vector.Vector2d(-distance, random.random() * SCREEN_HEIGHT)

    elif screenSide == TOP:
        object.position = vector.Vector2d(random.random() * SCREEN_WIDTH, -distance)

    elif screenSide == RIGHT:
        object.position = vector.Vector2d(SCREEN_WIDTH + distance, random.random() * SCREEN_HEIGHT)

    elif screenSide == BOTTOM:
        object.position = vector.Vector2d(random.random() * SCREEN_WIDTH, SCREEN_HEIGHT + distance)



"""AI Styles"""
def hide(object, hideBehind, hideFrom, offset = 128):

    """Find the location that the actor should go to"""
    goalLocation = hideBehind.position
    offSetDirection = hideBehind.position - hideFrom.position
    offSetDirection.makeNormal()
    goalLocation += (offSetDirection * offset)


    """Send the actor to target location"""
    bearing = goalLocation - object.position

    if bearing.getMagnitude() > object.speed:
        bearing.setMagnitude(object.speed)

    object.velocity = bearing



def goToPoint(object, point):
    bearing = point - object.position
    
    if bearing.getMagnitude() > object.speed:
        bearing.setMagnitude(object.speed)
    
    object.velocity = bearing



def goToTarget(object, target):
    bearing = target.position - object.position

    if bearing.getMagnitude() > object.speed:
        bearing.setMagnitude(object.speed)

    object.velocity = bearing



def arcToPoint(object, targetPoint, degree = 1):
    goalBearing = targetPoint - object.position
    goalBearing.makeNormal()
    goalBearing *= degree

    object.velocity += goalBearing

    object.velocity.setMagnitude(object.speed)


def cardinalDirection(object):
    if (int(random.random() * 2 + 1) - 1):
        if (int(random.random() * 2 + 1) - 1):
            object.velocity = vector.Vector2d(object.speed, 0.0)
        else:
            object.velocity = vector.Vector2d(-object.speed, 0.0)
    else:
        if (int(random.random() * 2 + 1) - 1):
            object.velocity = vector.Vector2d(0.0, object.speed)
        else:
            object.velocity = vector.Vector2d(0.0, -object.speed)



"""AI tools"""
def getClosest(object, targetGroup, targetActors = None):
    tempGroup1 = []
    tempGroup2 = []
    tempGroup3 = []

    searchGroups = []

    try:
        for subGroup in targetGroup:
            for actor in targetGroup:
                pass
            searchGroups.append(subGroup)
    
        for group in searchGroups:
            if targetActors != None:
                try:
                    for target in group:
                        for actor in targetActors:
                            if target.actorType == actor:
                                tempGroup2.append(target)
                except:
                    try:
                        if target.actorType  == targetActors:
                            tempGroup2.append(target)
                    except:
                        pass
            else:
                for target in targetGroup:
                    tempGroup2.append(target)
    
    except:
        if targetActors != None:
            try:
                for target in targetGroup:
                    for actor in targetActors:
                        if target.actorType == actor:
                            tempGroup2.append(target)
            except:
                if target.actorType  == targetActors:
                    tempGroup2.append(target)
        else:
            for target in targetGroup:
                tempGroup2.append(target)

    iteration = 1
    closestDistance = 100000 #abritarily large number
    
    while True:
        targetFound = False

        for target in tempGroup2:
            if abs(target.position.x - object.position.x) < (SCREEN_WIDTH / iteration):
                if abs(target.position.y - object.position.y) < (SCREEN_HEIGHT / iteration):
                    targetFound = True
                    tempGroup1.append(target)
        if iteration == 1 and not targetFound:
            return object
        elif iteration  == 8 or not targetFound:
             for target in tempGroup3:
                targetDistance = target.position - object.position
                if closestDistance > targetDistance.getMagnitude():
                    closetDistance = targetDistance.getMagnitude()
                    closestObject = target

             tempGroup1 = []
             tempGroup2 = []
             tempGroup3 = []
             return target
        else:
            tempGroup3 = tempGroup2
            tempGroup2 = tempGroup1
            tempGroup1 = []

        iteration += 1