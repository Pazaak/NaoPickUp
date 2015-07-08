__author__ = 'Luis Fabregues de los Santos'

import heapq as heap
import copy
import math

infty = float('inf')


def distance_2d(x1, y1, x2, y2):
    x = x1 - x2
    y = y1 - y2
    return math.sqrt(x*x+y*y)


def value(list, robots, target):
    result = 0
    for path in xrange(len(list)):
        for i in xrange(len(list[path])):
            if i == 0:
                result += distance_2d(robots[path].x, robots[path].y, list[path][i].x, list[path][i].y)
                result += distance_2d(target.x, target.y, list[path][i].x, list[path][i].y)
            else:
                result += 2 * distance_2d(target.x, target.y, list[path][i].x, list[path][i].y)
    return result

# Evaluation function 1, min total steps
def branchAndBound1(robots, target, boxes):
    maxLen = 2
    insertions = 2
    creations = 2
    extractions = 0
    boxes = sorted(boxes, key=lambda x: distance_2d(x.x, x.y, target.x, target.y), reverse=True)
    pool = []
    scores = []
    for box in boxes:
        scores.append(distance_2d(box.x, box.y, target.x, target.y) * 2)
    current = []
    for i in xrange(len(robots)):
        current.append([])
    heap.heappush(pool, (sum(scores), range(len(boxes)), current))
    iteraciones = 0
    while len(pool) > 0:
        if len(pool) > maxLen: maxLen = len(pool)
        extractions += 1
        current = heap.heappop(pool)
        # Si la lista de cajas esta vacia
        if not current[1]:
            return [maxLen, insertions, creations, extractions, iteraciones, value(current[2], robots, target), 0], \
                   current[2]
        else:
            # Por cada caja que quede la intentamos asignar a un robot
            for nbox in current[1]:
                for i in xrange(len(robots)):
                    temp = copy.deepcopy(current[2])
                    temp[i].append(boxes[nbox])
                    # Creamos una nueva lista de cajas
                    newboxes = list(current[1])
                    newboxes.remove(nbox)
                    creations += 1
                    plusScore = 0
                    for scbox in newboxes:
                        plusScore += scores[scbox]
                    temp = (value(temp, robots, target) + plusScore, newboxes, temp)
                    heap.heappush(pool, temp)
                    insertions += 1

        iteraciones += 1


def value2(list, robots, target):
    result = []
    for path in xrange(len(list)):
        result.append(0)
        for i in xrange(len(list[path])):
            if i == 0:
                result[path] += distance_2d(robots[path].x, robots[path].y, list[path][i].x, list[path][i].y)
                result[path] += distance_2d(target.x, target.y, list[path][i].x, list[path][i].y)
            else:
                result[path] += 2 * distance_2d(target.x, target.y, list[path][i].x, list[path][i].y)
    return max(result)

# Evaluation function 2, min max robot steps
def branchAndBound2(robots, target, boxes):
    maxLen = 2
    insertions = 2
    creations = 2
    extractions = 0
    boxes = sorted(boxes, key=lambda x: distance_2d(x.x, x.y, target.x, target.y), reverse=True)
    pool = []
    scores = []
    for box in boxes:
        scores.append((distance_2d(box.x, box.y, target.x, target.y) * 2))
    current = []
    for i in xrange(len(robots)):
        current.append([])
    heap.heappush(pool, (sum(scores), range(len(boxes)), current))
    iteraciones = 0
    while len(pool) > 0:
        if len(pool) > maxLen: maxLen = len(pool)
        extractions += 1
        current = heap.heappop(pool)
        # Si la lista de cajas esta vacia
        if not current[1]:
            return [maxLen, insertions, creations, extractions, iteraciones, value(current[2], robots, target), \
                    value2(current[2], robots, target)], current[2]
        else:
            # Por cada caja que quede la intentamos asignar a un robot
            for nbox in current[1]:
                for i in xrange(len(robots)):
                    temp = copy.deepcopy(current[2])
                    temp[i].append(boxes[nbox])
                    # Creamos una nueva lista de cajas
                    newboxes = list(current[1])
                    newboxes.remove(nbox)
                    creations += 1
                    temp = (value2(temp, robots, target), newboxes, temp)
                    heap.heappush(pool, temp)
                    insertions += 1

        iteraciones += 1

# Evaluation function 2, with optimistic score, UNSTABLE
def branchAndBound3(robots, target, boxes):
    maxLen = 2
    insertions = 2
    creations = 2
    extractions = 0
    boxes = sorted(boxes, key=lambda x: distance_2d(x.x, x.y, target.x, target.y), reverse=True)
    pool = []
    scores = []
    for box in boxes:
        scores.append(distance_2d(box.x, box.y, target.x, target.y) * 2)
    current = []
    for i in xrange(len(robots)):
        current.append([])
    heap.heappush(pool, (sum(scores), range(len(boxes)), current))
    iteraciones = 0
    while len(pool) > 0:
        if len(pool) > maxLen: maxLen = len(pool)
        extractions += 1
        current = heap.heappop(pool)
        # Si la lista de cajas esta vacia
        if not current[1]:
            return [maxLen, insertions, creations, extractions, iteraciones, value(current[2], robots, target), \
                    value2(current[2], robots, target)], current[2]
        else:
            # Por cada caja que quede la intentamos asignar a un robot
            for nbox in current[1]:
                for i in xrange(len(robots)):
                    temp = copy.deepcopy(current[2])
                    temp[i].append(boxes[nbox])
                    # Creamos una nueva lista de cajas
                    newboxes = list(current[1])
                    newboxes.remove(nbox)
                    creations += 1
                    temp = (2*value2(temp, robots, target)+len(newboxes), newboxes, temp)
                    heap.heappush(pool, temp)
                    insertions += 1

        iteraciones += 1

# Evaluation function 2, save the better, complete state
def branchAndBound4(robots, target, boxes):
    maxLen = 2
    insertions = 2
    creations = 2
    extractions = 0
    bestYet = infty
    boxes = sorted(boxes, key=lambda x: distance_2d(x.x, x.y, target.x, target.y), reverse=True)
    pool = []
    scores = []
    for box in boxes:
        scores.append((distance_2d(box.x, box.y, target.x, target.y) * 2))
    current = []
    for i in xrange(len(robots)):
        current.append([])
    heap.heappush(pool, (sum(scores), range(len(boxes)), current))
    iteraciones = 0
    while len(pool) > 0:
        if len(pool) > maxLen: maxLen = len(pool)
        extractions += 1
        current = heap.heappop(pool)
        # Si la lista de cajas esta vacia
        if not current[1]:
            return [maxLen, insertions, creations, extractions, iteraciones, value(current[2], robots, target), \
                    value2(current[2], robots, target)], \
                   current[2]
        else:
            # Por cada caja que quede la intentamos asignar a un robot
            for nbox in current[1]:
                for i in xrange(len(robots)):
                    temp = copy.deepcopy(current[2])
                    temp[i].append(boxes[nbox])
                    # Creamos una nueva lista de cajas
                    newboxes = list(current[1])
                    newboxes.remove(nbox)
                    creations += 1
                    temp = (value2(temp, robots, target), newboxes, temp)
                    if temp[0] < bestYet:
                        heap.heappush(pool, temp)
                        insertions += 1
                        if not temp[1]:
                            bestYet = temp[0]

        iteraciones += 1