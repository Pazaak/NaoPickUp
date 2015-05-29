__author__ = 'maleza'

import almath
from math import pi, atan, sqrt
import time
from naoqi import ALProxy

motionProxy = ALProxy("ALMotion", "192.168.1.5", 9559)
talkProxy = ALProxy("ALTextToSpeech", "192.168.1.5", 9559)

def calculeAngle(souX, souY, tarX, tarY):
    if tarY-souY == 0:
        if tarX-souX < 0: return pi
        elif tarX-souX > 0: return 0
    elif tarX-souX != 0:
        return atan(float(tarY-souY)/(tarX-souX))
    elif tarY-souY < 0:
        return pi/2
    elif tarY-souY > 0:
        return -pi/2
    else:
        return 0

motionProxy.post.moveTo(1, 1, 0)
motionProxy.waitUntilMoveIsFinished()



