# Knight's Tour using Warnsdorff's Rule
# http://en.wikipedia.org/wiki/Knight's_tour
# FB - 20121216




from heapq import heappush, heappop # for priority queue
import random
import string
import numpy as np
chessX = 8; chessY = 8 # width and height of the chessboard
chessboard = [[0 for x in range(chessX)] for y in range(chessY)] # chessboard
chessboard = np.zeros((chessY,chessX),dtype=np.int32)


# directions the Knight can move on the chessboard
moveX = [-2, -1, 1, 2, -2, -1, 1, 2]
moveY = [1, 2, 2, 1, -1, -2, -2, -1]
# start the Knight from a random position
initX = random.randint(0, chessX - 1)
initY = random.randint(0, chessY - 1)

print(chessboard)

for step in range(chessX * chessY):
    chessboard[initY][initX] = step + 1
    priorityQueue = [] # priority queue of available neighbors
    for i in range(8):
        newX = initX + moveX[i]
        newY = initY + moveY[i]

        if newX >= 0 and newX < chessX and newY >= 0 and newY < chessY:
            if chessboard[newY][newX] == 0:
                # count the available neighbors of the neighbor
                degreeCount = 0
                for j in range(8):
                    possibleX = newX + moveX[j]
                    possibleY = newY + moveY[j]

                    if possibleX >= 0 and possibleX < chessX and possibleY >= 0 and possibleY < chessY:
                        if chessboard[possibleY][possibleX] == 0:
                            degreeCount += 1
                heappush(priorityQueue, (degreeCount, i))
    # move to the neighbor that has min number of available neighbors
    if len(priorityQueue) > 0:
        (p, m) = heappop(priorityQueue)
        initX += moveX[m]; initY += moveY[m]
    else: break

# print chessboard
for cy in range(chessY):
    for cx in range(chessX):
        print (str.rjust(str(chessboard[cy][cx]), 2),)
    
print(chessboard)


def visualize():
    pass


def isValid(newX,newY,chessboard):
    if newX >= 0 and newY >= 0 and newX < chessX and newY < chessY:
        if chessboard[newY][newX] == 0:
            return True
    return False
    
def getPossibleMoves(newX,newY,chessboard):
    degreeCount = 0
    for j in range(8):
        possibleX = newX + moveX[j]
        possibleY = newY + moveY[j]
        if isValid(possibleX,possibleY,chessboard):
            degreeCount+=1
    return degreeCount
    