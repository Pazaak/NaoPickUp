__author__ = 'maleza'
from header_classes import Robot, Object
import random
import solver
import time
from math import fabs

result = [0]*10
for robs in xrange(1000):
    cajas = []
    robots = []

    for i in xrange(5):
        r1 = int(random.random()*20)
        r2 = int(random.random()*20)
        while r1 == 10 and r2 == 10:
            r1 = int(random.random()*20)
            r2 = int(random.random()*20)
        cajas.append(Object(r1, r2))

    target = Object(10, 10)

    for i in xrange((robs%10)+2):
        r1 = int(random.random()*20)
        r2 = int(random.random()*20)
        while r1 == 10 and r2 == 10:
            r1 = int(random.random()*20)
            r2 = int(random.random()*20)
        robots.append(Robot(r1, r2, ""))

    data0, result0 = solver.branchAndBound2(robots, target, cajas)

    result[(robs%10)] += data0[3]

for i in xrange(10):
    print i, "-", result[i]/100

