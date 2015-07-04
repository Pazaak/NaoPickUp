__author__ = 'maleza'

import almath
from math import pi, atan, sqrt, cos, sin
import time
from naoqi import ALProxy

robot1 = False
robot2 = True
real = False

if robot1:
    if real:
        motionProxy1 = ALProxy("ALMotion", "192.168.1.5", 9559)
        locationProxy1 = ALProxy("ALLocalization", "192.168.1.5", 9559)
    else:
        motionProxy1 = ALProxy("ALMotion", "127.0.0.1", 56294)
        locationProxy1 = ALProxy("ALLocalization", "127.0.0.1", 56294)
else:
    motionProxy1 = None
    locationProxy1 = None

if robot2:
    if real:
        motionProxy2 = ALProxy("ALMotion", "192.168.1.5", 9559)
        locationProxy2 = ALProxy("ALLocalization", "192.168.1.5", 9559)
    else:
        motionProxy2 = ALProxy("ALMotion", "127.0.0.1", 54605)
        locationProxy2 = ALProxy("ALLocalization", "127.0.0.1", 54605)
else:
    motionProxy2 = None
    locationProxy2 = None

def calculeAngle(souX, souY, tarX, tarY):
    if tarY == souY:
        if tarX-souX < 0:
            return pi
        return 0
    if tarX == souX:
        if tarY-souY < 0:
            return -pi/2
        return pi/2
    if tarX-souX < 0:
        if tarY-souY < 0:
            return -pi+atan(float(tarY-souY)/(tarX-souX))
        return pi+atan(float(tarY-souY)/(tarX-souX))
    return atan(float(tarY-souY)/(tarX-souX))

print
print
print
print "-------------------------------------"
print "Desplazamiento directo"
print "-------------------------------------"


pos1 = almath.Pose2D([0, 0, 0])
pos2 = almath.Pose2D([0, 0, 0])
if robot1: locationProxy1.learnHome()
if robot2: locationProxy2.learnHome()
if robot1: pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
if robot2: pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
if robot1:
    motionProxy1.moveTo(0.3-pos1.x, 0.5-pos1.y, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
    motionProxy1.moveTo(1.0-pos1.x, 1.0-pos1.y, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    motionProxy1.moveTo(0.5-pos1.x, 1.0-pos1.y, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
if robot2:
    motionProxy2.moveTo(0.3-pos2.x, 0.5-pos2.y, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
    motionProxy2.moveTo(1.0-pos2.x, 1.0-pos2.y, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    motionProxy2.moveTo(0.5-pos2.x, 1.0-pos2.y, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
if robot1:
    motionProxy1.moveTo(1.0-pos1.x, 1.0-pos1.y, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    motionProxy1.moveTo(1.0-pos1.x, 0.5-pos1.y, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
if robot2:
    motionProxy2.moveTo(1.0-pos2.x, 1.0-pos2.y, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    motionProxy2.moveTo(1.0-pos2.x, 0.5-pos2.y, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
if robot1:
    motionProxy1.moveTo(1.0-pos1.x, 1.0-pos1.y, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    motionProxy1.moveTo(0.0-pos1.x, 0.0-pos1.y, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Origen", pos1
if robot2:
    motionProxy2.moveTo(1.0-pos2.x, 1.0-pos2.y, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    motionProxy2.moveTo(0.0-pos2.x, 0.0-pos2.y, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Origen", pos2

print
print
print
print "-------------------------------------"
print "Desplazamiento con giro previo"
print "-------------------------------------"

pos1 = almath.Pose2D([0, 0, 0])
pos2 = almath.Pose2D([0, 0, 0])
if robot1: locationProxy1.learnHome()
if robot2: locationProxy2.learnHome()
if robot1: pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
if robot2: pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
if robot1:
    alpha = calculeAngle(pos1.x, pos1.y, 0.3, 0.5) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy1.moveTo(0, 0, alpha)
    motionProxy1.waitUntilMoveIsFinished()
    x = 0.3-pos1.x
    y = 0.5-pos1.y
    motionProxy1.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
    alpha = calculeAngle(pos1.x, pos1.y, 1.0, 1.0) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy1.moveTo(0, 0, alpha)
    motionProxy1.waitUntilMoveIsFinished()
    x = 1.0-pos1.x
    y = 1.0-pos1.y
    motionProxy1.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    alpha = calculeAngle(pos1.x, pos1.y, 0.5, 1.0) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy1.moveTo(0, 0, alpha)
    motionProxy1.waitUntilMoveIsFinished()
    x = 0.5-pos1.x
    y = 1.0-pos1.y
    motionProxy1.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
if robot2:
    alpha = calculeAngle(pos2.x, pos2.y, 0.3, 0.5) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy2.moveTo(0, 0, alpha)
    motionProxy2.waitUntilMoveIsFinished()
    x = 0.3-pos2.x
    y = 0.5-pos2.y
    motionProxy2.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
    alpha = calculeAngle(pos2.x, pos2.y, 1.0, 1.0) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy2.moveTo(0, 0, alpha)
    motionProxy2.waitUntilMoveIsFinished()
    x = 1.0-pos2.x
    y = 1.0-pos2.y
    motionProxy2.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    alpha = calculeAngle(pos2.x, pos2.y, 0.5, 1.0) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy2.moveTo(0, 0, alpha)
    motionProxy2.waitUntilMoveIsFinished()
    x = 0.5-pos2.x
    y = 1.0-pos2.y
    motionProxy2.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
if robot1:
    alpha = calculeAngle(pos1.x, pos1.y, 1.0, 1.0) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy1.moveTo(0, 0, alpha)
    motionProxy1.waitUntilMoveIsFinished()
    x = 1.0-pos1.x
    y = 1.0-pos1.y
    motionProxy1.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    alpha = calculeAngle(pos1.x, pos1.y, 1.0, 0.5) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy1.moveTo(0, 0, alpha)
    motionProxy1.waitUntilMoveIsFinished()
    x = 1.0-pos1.x
    y = 0.5-pos1.y
    motionProxy1.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
if robot2:
    alpha = calculeAngle(pos2.x, pos2.y, 1.0, 1.0) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy2.moveTo(0, 0, alpha)
    motionProxy2.waitUntilMoveIsFinished()
    x = 1.0-pos2.x
    y = 1.0-pos2.y
    motionProxy2.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    alpha = calculeAngle(pos2.x, pos2.y, 1.0, 0.5) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy2.moveTo(0, 0, alpha)
    motionProxy2.waitUntilMoveIsFinished()
    x = 1.0-pos2.x
    y = 0.5-pos2.y
    motionProxy2.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
if robot1:
    alpha = calculeAngle(pos1.x, pos1.y, 1.0, 1.0) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy1.moveTo(0, 0, alpha)
    motionProxy1.waitUntilMoveIsFinished()
    x = 1.0-pos1.x
    y = 1.0-pos1.y
    motionProxy1.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    motionProxy1.moveTo(0, 0, 0 - pos1.theta)
    motionProxy1.waitUntilMoveIsFinished()
    x = -pos1.x
    y = -pos1.y
    motionProxy1.moveTo(x, y, 0)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Origen", pos1
if robot2:
    alpha = calculeAngle(pos2.x, pos2.y, 1.0, 1.0) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    motionProxy2.moveTo(0, 0, alpha)
    motionProxy2.waitUntilMoveIsFinished()
    x = 1.0-pos2.x
    y = 1.0-pos2.y
    motionProxy2.moveTo(sqrt(x*x+y*y), 0, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    motionProxy2.moveTo(0, 0, -pos2.theta)
    motionProxy2.waitUntilMoveIsFinished()
    x = -pos2.x
    y = -pos2.y
    motionProxy2.moveTo(x, y, 0)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Origen", pos2

print
print
print
print "-------------------------------------"
print "Desplazamiento con giro incorporado"
print "-------------------------------------"

pos1 = almath.Pose2D([0, 0, 0])
pos2 = almath.Pose2D([0, 0, 0])
if robot1: locationProxy1.learnHome()
if robot2: locationProxy2.learnHome()
if robot1: pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
if robot2: pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
if robot1:
    alpha = calculeAngle(pos1.x, pos1.y, 0.3, 0.5) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 0.3-pos1.x
    y = 0.5-pos1.y
    theta = -pos1.theta
    motionProxy1.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
    alpha = calculeAngle(pos1.x, pos1.y, 1.0, 1.0) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 1.0-pos1.x
    y = 1.0-pos1.y
    theta = -pos1.theta
    motionProxy1.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    alpha = calculeAngle(pos1.x, pos1.y, 0.5, 1.0) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 0.5-pos1.x
    y = 1.0-pos1.y
    theta = -pos1.theta
    motionProxy1.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
if robot2:
    alpha = calculeAngle(pos2.x, pos2.y, 0.3, 0.5) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 0.3-pos2.x
    y = 0.5-pos2.y
    theta = -pos2.theta
    motionProxy2.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
    alpha = calculeAngle(pos2.x, pos2.y, 1.0, 1.0) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 1.0-pos2.x
    y = 1.0-pos2.y
    theta = -pos2.theta
    motionProxy2.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    alpha = calculeAngle(pos2.x, pos2.y, 0.5, 1.0) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 0.5-pos2.x
    y = 1.0-pos2.y
    theta = -pos2.theta
    motionProxy2.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
if robot1:
    alpha = calculeAngle(pos1.x, pos1.y, 1.0, 1.0) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 1.0-pos1.x
    y = 1.0-pos1.y
    theta = -pos1.theta
    motionProxy1.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    alpha = calculeAngle(pos1.x, pos1.y, 1.0, 0.5) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 1.0-pos1.x
    y = 0.5-pos1.y
    theta = -pos1.theta
    motionProxy1.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Caja", pos1
if robot2:
    alpha = calculeAngle(pos2.x, pos2.y, 1.0, 1.0) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 1.0-pos2.x
    y = 1.0-pos2.y
    theta = -pos2.theta
    motionProxy2.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    alpha = calculeAngle(pos2.x, pos2.y, 1.0, 0.5) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 1.0-pos2.x
    y = 0.5-pos2.y
    theta = -pos2.theta
    motionProxy2.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2
if robot1:
    alpha = calculeAngle(pos1.x, pos1.y, 1.0, 1.0) - pos1.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 1.0-pos1.x
    y = 1.0-pos1.y
    theta = -pos1.theta
    motionProxy1.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Contenedor", pos1
    x = -pos1.x
    y = -pos1.y
    theta = -pos1.theta
    motionProxy1.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), theta)
    motionProxy1.waitUntilMoveIsFinished()
    pos1 = almath.Pose2D(locationProxy1.getRobotPosition(False))
    print "1:Origen", pos1
if robot2:
    alpha = calculeAngle(pos2.x, pos2.y, 1.0, 1.0) - pos2.theta
    if alpha > pi+0.0001:
        alpha -= 2*pi
    if alpha < -pi-0.0001:
        alpha += 2*pi
    x = 1.0-pos2.x
    y = 1.0-pos2.y
    theta = -pos2.theta
    motionProxy2.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), alpha)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Contenedor", pos2
    x = -pos2.x
    y = -pos2.y
    theta = -pos2.theta
    motionProxy2.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), theta)
    motionProxy2.waitUntilMoveIsFinished()
    pos2 = almath.Pose2D(locationProxy2.getRobotPosition(False))
    print "2:Caja", pos2