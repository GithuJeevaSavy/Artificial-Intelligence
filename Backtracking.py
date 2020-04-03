# Python3 program to solve Knight Tour problem using Backtracking
import datetime

# Chessboard Size
totalRows = 6
totalCols = 6
startRow = 2
startCol = 2
possibleMoves = [[2, 1], [1, 2], [-1, 2],
                 [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]


# Function to validate if next move is possible.
# Verifying new coordinates are not out of bounds and the coordinate is not already visited.
def isValidMove(newRow, newCol, visitedBlocks):
    if newRow > -1 and newRow < totalRows and newCol > -1 and newCol < totalCols and visitedBlocks[newRow][newCol] == 0:
        return True
    return False

# Function to print 2D solution array of size totalRows * totalCols


def printMoves(visitedBlocks):
    print("Solution :::: ")
    for i in range(totalRows):
        row = ""
        for j in range(totalCols):
            row = row + "   " + str(visitedBlocks[i][j])
        print(row)
    print("Program execution finished.")


def findTour(row, col, move, visitedBlocks):
    #  Initial condition to check if starting point is in bounds or not. If not, exit.
    if not (row > -1 and row < totalRows and col > -1 and col < totalCols):
        print("Initial Row Column out of Bounds")
        return False

    # To update 1st move in visitedBlocks in the start.
    if move == 1:
        visitedBlocks[row][col] = move

    # Maximum moves possible to ensure one block is visited once is totalRows * totalCols.
    # If move reaches that value, print the solution generated
    # Else find next move
    if(move == totalCols*totalRows):

        # Function call to print 2D solution array.
        printMoves(visitedBlocks)
        return True
    else:

        # Iterating over possible moves and validating if the move is possible.
        for i in range(len(possibleMoves)):
            newRow = row + possibleMoves[i][0]
            newCol = col + possibleMoves[i][1]

            # If move valid, update move index and visitedBlocks.
            # Find if next move is possible using recursion
            # Else update move to previous value and reset last updated value of visitedblocks
            if(isValidMove(newRow, newCol, visitedBlocks)):
                move += 1
                visitedBlocks[newRow][newCol] = move
                if(findTour(newRow, newCol, move, visitedBlocks)):
                    return True

                move -= 1
                visitedBlocks[newRow][newCol] = 0

        return False


# Driver program to test above function
if __name__ == "__main__":
    # Initialize visitedBlocks array to track moves.
    visitedBlocks = [[0 for x in range(totalRows)] for y in range(totalCols)]
    print("Initiating program execution...")

    # Function call to find tour with starting point as [startRow, startCol]
    if not findTour(startRow, startCol, 1, visitedBlocks):
        print("Solution doesn't exists.")
