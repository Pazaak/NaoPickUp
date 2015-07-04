__author__ = 'maleza'
from header_classes import Robot, Object
import random
import solver
import time
from math import fabs

res0 = [0]*6
res1 = [0]*6
for case in xrange(100):
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

    for i in xrange(5):
        r1 = int(random.random()*20)
        r2 = int(random.random()*20)
        while r1 == 10 and r2 == 10:
            r1 = int(random.random()*20)
            r2 = int(random.random()*20)
        robots.append(Robot(r1, r2, ""))

    """
    target = Object(10, 10)

    robots.append(Robot(0, 0, ""))
    robots.append(Robot(20, 20, ""))

    cajas.append(Object(10, 15))
    cajas.append(Object(5, 3))
    cajas.append(Object(5, 10))
    cajas.append(Object(15, 10))
    cajas.append(Object(17, 15))
    cajas.append(Object(10, 5))
    """

    t0 = time.time()
    data0, result0 = solver.branchAndBound4(robots, target, cajas)
    t1 = time.time()

    res0[0] += data0[4]
    res0[1] += data0[0]
    res0[2] += data0[3]
    res0[3] += data0[2]
    res0[4] += data0[1]
    res0[5] += t1-t0

    """
    print "Iteraciones:", data[4]
    print "Maximo tamanyo de la pila:", data[0]
    print "Extracciones:", data[3]
    print "Estados creados:", data[2]
    print "Estados insertados:", data[1]
    print "Pasos:", data[5]
    print "Pasos distribuidos:", data[6]
    print
    """

    t0 = time.time()
    data1, result1 = solver.branchAndBound5(robots, target, cajas)
    t1 = time.time()

    if fabs(data0[6]-data1[6]) > 0.0001:
        print "ERROR:", data0[6], data1[6]
        break

    res1[0] += data1[4]
    res1[1] += data1[0]
    res1[2] += data1[3]
    res1[3] += data1[2]
    res1[4] += data1[1]
    res1[5] += t1-t0

    """
    print "Iteraciones:", data[4]
    print "Maximo tamanyo de la pila:", data[0]
    print "Extracciones:", data[3]
    print "Estados creados:", data[2]
    print "Estados insertados:", data[1]
    print "Pasos:", data[5]
    print "Pasos distribuidos:", data[6]
    print


    for i in xrange(len(robots)):
        print robots[i]
        for box in result[i]:
            print box
        print
    """
    print case

print; print; print;

print "Algoritmo 1"
print "- Iteraciones:", res0[0]/100
print "- Max tamanyo pila:", res0[1]/100
print "- Extracciones:", res0[2]/100
print "- Creaciones:", res0[3]/100
print "- Inserciones:", res0[4]/100
print "- Tiempo:", res0[5]/100.0
print

print "Algoritmo 2"
print "- Iteraciones:", res1[0]/100
print "- Max tamanyo pila:", res1[1]/100
print "- Extracciones:", res1[2]/100
print "- Creaciones:", res1[3]/100
print "- Inserciones:", res1[4]/100
print "- Tiempo:", res1[5]/100.0
