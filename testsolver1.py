__author__ = 'maleza'
from header_classes import Robot, Object
import random
import solver
import time
from math import fabs

result = 0
for robs in xrange(10):
    cajas = []
    robots = []

    for i in xrange(7):
        r1 = int(random.random()*20)
        r2 = int(random.random()*20)
        while r1 == 10 and r2 == 10:
            r1 = int(random.random()*20)
            r2 = int(random.random()*20)
        cajas.append(Object(r1, r2))

    target = Object(10, 10)

    for i in xrange(2):
        r1 = int(random.random()*20)
        r2 = int(random.random()*20)
        while r1 == 10 and r2 == 10:
            r1 = int(random.random()*20)
            r2 = int(random.random()*20)
        robots.append(Robot(r1, r2, ""))

    data0, result0 = solver.branchAndBound2(robots, target, cajas)

    result += data0[3]

print result/10

