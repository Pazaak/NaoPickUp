__author__ = 'maleza'
from header_classes import Robot, Object
import random
import solver

cajas = []
robots = []
"""
for i in xrange(10):
    r1 = int(random.random()*100)
    r2 = int(random.random()*100)
    while r1 == 50 and r2 == 50:
        r1 = int(random.random()*100)
        r2 = int(random.random()*100)
    cajas.append(Object(r1, r2))

target = Object(50, 50)



for i in xrange(10):
    r1 = int(random.random()*100)
    r2 = int(random.random()*100)
    while r1 == 50 and r2 == 50:
        r1 = int(random.random()*100)
        r2 = int(random.random()*100)
    robots.append(Robot(r1, r2, ""))
"""
target = Object(10, 10)

robots.append(Robot(0, 0, ""))
robots.append(Robot(20, 20, ""))

cajas.append(Object(10, 15))
cajas.append(Object(5, 7))
cajas.append(Object(5, 10))
cajas.append(Object(15, 10))
cajas.append(Object(17, 15))
cajas.append(Object(10, 5))



data, result = solver.branchAndBound(robots, target, cajas)


print "Iteraciones:", data[4]
print "Maximo tamanyo de la pila:", data[0]
print "Extracciones:", data[3]
print "Estados creados:", data[2]
print "Estados insertados:", data[1]
print "Pasos:", data[5]
print

i = 1
for list in result:
    print "Robot "+str(i)+" ("+str(robots[i-1].x)+", "+str(robots[i-1].y)+")"
    i += 1
    for cosa in list:
        print cosa
