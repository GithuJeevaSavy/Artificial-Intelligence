	import argparse
import cv2
from heapq import heappush, heappop
import random
import numpy as np

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
	


aparser = argparse.ArgumentParser(description="Warnsdorff Rule")
aparser.add_argument('--rows', type=int, default=8, 
	help="rows in a chessboard")
aparser.add_argument('--cols', type=int, default=8, 
	help="columns in a chessboard")
args = vars(aparser.parse_args())

chessX = args["cols"]	# X
chessY = args["rows"]	# Y

# init a chessboard with zeros
chessboard = np.zeros((chessY,chessX),dtype=np.int32)

#mocve pattern of the knight
moveX = [-2, -1, 1, 2, -2, -1, 1, 2]
moveY = [1, 2, 2, 1, -1, -2, -2, -1]

# init position of the knight
initX = random.randint(0,chessX-1)
initY = random.randint(0,chessY-1)

for step in range(chessX*chessY):
	# print("step",step)
	chessboard[initY][initX] = step+1
	priorityQueue = []

	for i in range(8):
		newX = initX + moveX[i]
		newY = initY + moveY[i]


		if isValid(newX,newY,chessboard):
			degreeCount = getPossibleMoves(newX,newY,chessboard)
			heappush(priorityQueue,(degreeCount,i))

	# pop the smallest element from the priority queue
	if len(priorityQueue) > 0:
		(degree,moveNumber) = heappop(priorityQueue)
		initX = initX + moveX[moveNumber]
		initY = initY + moveY[moveNumber]
	else: 
		print("queue was empty")
		break


print(priorityQueue)
print(chessboard)
