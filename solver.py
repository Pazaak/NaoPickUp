__author__ = 'Luis Fabregues de los Santos'

import heapq as heap
from copy import deepcopy
infty = float('inf')


def distance_2d(x1, y1, x2, y2):
    return abs(x1-x2)+abs(y1-y2)


def value(list, robots, target):
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

def end_value(list, robots, target):
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

def branchAndBound(robots, target, boxes):

    maxLen = 2
    insertions = 2
    creations = 2
    extractions = 0
    boxes = sorted(boxes, key=lambda x: distance_2d(x.x, x.y, target.x, target.y), reverse=False)
    pool = []
    current = []
    scores = []
    for box in boxes:
        scores.append(distance_2d(box.x, box.y, target.x, target.y))
    ratio = len(boxes)/len(robots)
    if ratio == 0:
        for i in xrange(len(boxes)):
            current.append(boxes[i])
    else:
        for i in xrange(len(robots)):
            if i+1 != len(robots):
                current.append(boxes[i*ratio:(i+1)*ratio])
            else:
                current.append(boxes[i*ratio:])
    current = (value(current, robots, target), [], current)
    heap.heappush(pool, current)
    best_yet = current[0]
    current = []
    for i in xrange(len(robots)):
        current.append([])
    heap.heappush(pool, (sum(scores)/len(robots), range(len(boxes)), current))
    iteraciones = 0
    while len(pool) > 0:
        if len(pool) > maxLen: maxLen = len(pool)
        extractions += 1
        current = heap.heappop(pool)
        # Si la lista de cajas esta vacia
        if not current[1]:
            return [maxLen, insertions, creations, extractions, iteraciones, end_value(current[2], robots, target)], current[2]
        else:
            # Por cada caja que quede la intentamos asignar a un robot
            for nbox in current[1]:
                for i in xrange(len(robots)):
                    temp = deepcopy(current[2])
                    temp[i].append(boxes[nbox])
                    # Creamos una nueva lista de cajas
                    newboxes = deepcopy(current[1])
                    newboxes.remove(nbox)
                    creations += 1
                    plusScore = 0
                    for scbox in newboxes:
                        plusScore += scores[scbox]
                    temp = (value(temp, robots, target)+plusScore/len(robots), newboxes, temp)
                    if best_yet > temp[0]:
                        heap.heappush(pool, temp)
                        insertions += 1
                        if temp[1] == len(boxes):
                            best_yet = temp[0]
        iteraciones += 1