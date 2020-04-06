import threading
import time
from typing import NamedTuple
import math
import random

import threading

class WaitGroup(object):

    def __init__(self):
        self.count = 0
        self.cv = threading.Condition()

    def add(self, n):
        self.cv.acquire()
        self.count += n
        self.cv.release()

    def done(self):
        self.cv.acquire()
        self.count -= 1
        if self.count == 0:
            self.cv.notify_all()
        self.cv.release()

    def wait(self):
        self.cv.acquire()
        while self.count > 0:
            self.cv.wait()
        self.cv.release()

class rckt(NamedTuple):
    r: int
    c: int
    k: int
    t: float

class Problem:
    boardSize=0
    nSquares = 0
    completeTour = 0
    rstart = 2
    cstart = 3
    tNet = []
    drc = [[]]
    def __init__(self):


        self.boardSize = 8
        self.nSquares = boardSize * boardSize
        self.completeTour = nSquares - 1

        # task input: starting square.  These are 1 based, but otherwise 0 based
        # row and column numbers are used througout the program.
        self.rStart = 2
        self.cStart = 3

        # pheromone representation read by ants
        self.tNet = [self.nSquares*8]

        # row, col deltas of legal moves
        self.drc = [[-2, 1], [-2, -1], [-1, 2], [1, 2],
                            [2, 1], [2, -1], [1, -2], [-1, -2]]

# get square reached by following edge k from square (r, c)
    def dest(self,r, c, k ):
        r += self.drc[k][0]
        c += drc[k][1]
        if (r >= 0 and r < self.boardSize and c >= 0 and c < self.boardSize):
            return (r, c)


# struct represents a pheromone amount associated with a move

class square(NamedTuple):
    r: int
    c: int


def ant(self, r, c , start, reset , tourCh):

    self.tabu = [square]
    self.moves = [rckt]
    self.unexp = [rckt]
    self.tabu[0].r = r
    self.tabu[0].c = c

    while True:
        # cycle initialization


        r = self.tabu[0].r
        c = self.tabu[0].c

        # wait for start signal
        start.wait()
        reset.done()

        while True:
            # choose next move
            for k in range(0, 8):
                dr, dc, ok = self.dest(r, c, k)
                if not ok:
                    continue

                for t in self.tabu:
                    if t.r == dr and t.c == dc:
                        break


                tk = self.tNet[(r*self.boardSize+c)*8+k]
                self.tSum += tk
                # note:  dest r, c stored here
                self.unexp.append(rckt[dr, dc, k, tk])

            if len(self.unexp) == 0:
                break # no moves

            rn = random.random() * self.tSum

            for move in self.unexp:
                if rn <= move.t:
                    break
                rn -= move.t

            # move to new square
            move.r, r = r, move.r
            move.c, c = c, move.c
            self.tabu.append(square[r, c])
            self.moves.append( move)


        # compute pheromone amount to leave
        for i in self.moves:
            moves[i].t = (len(self.moves)-i) / (self.completeTour-i)

        # return tour found for this cycle
        tourCh <- self.moves


def main():
    pObj = Problem
    wObj = WaitGroup()

    print("Starting square:  row", pObj.rstart, "column", pObj.cstart)
    # initialize board
    for r in range(0, pObj.boardSize):
        for c in range(0, pObj.boardSize):
            for k in range(0, 8):
                if pObj.dest(r, c, k):
                    tNet[(r*pObj.boardSize+c)*8+k] = math.e-6



    # waitGroups for ant release clockwork
    start = WaitGroup
    start.__init__(WaitGroup)
    reset = WaitGroup
    reset.__init__(WaitGroup)
    start.add(start, n=1)
    r=0
    c=0
    k=0
    t=0
    # channel for ants to return tours with pheremone updates
    tch= [rckt(r,c,k,t)]


    # create an ant for each square
    for r in range(0, pObj.boardSize):
        for c in range(0, pObj.boardSize):
            ant(r, c, start, reset.wait(), tch)



    # accumulator for new pheromone amounts
    tNew = [pObj.nSquares*8]

    # each iteration is a "cycle" as described in the paper
    while True:
        # evaporate pheromones
        for i in range(0,len(pObj.tNet)):
            pObj.tNet[i] *= .75


        reset.add(reset,n=pObj.nSquares) #number of ants to release
        start.done(start)        #release them
        reset.wait(reset)        #wait for them to begin searching
        start.add(start, n=1)        #reset start signal for next cycle

        # gather tours from ants
        for r in range(0, pObj.nSquares):
            tour = pObj.tch
            # watch for a pObj tour from the specified starting square
            if len(tour) == pObj.completeTour and tour[0].r == pObj.rStart-1 and tour[0].c == pObj.cStart-1:

                # task output:  move sequence in a grid.
                seq = [pObj.nSquares]
                for i in  range(tour):
                    seq[tour[i].r*pObj.boardSize+tour[i].c] = i + 1

                last = tour[len(tour)-1]
                r, c, temp= pObj.dest(last.r, last.c, last.k)
                seq[r*pObj.boardSize+c] = pObj.nSquares
                print("Move sequence:")
                for r in range(0, pObj.boardSize):
                    for c in range(0, pObj.boardSize):
                        print(seq[r * pObj.boardSize + c])

                    print("\n")

                return # task only requires finding a single tour

            # accumulate pheromone amounts from all ants
            for i in range(tour):
                tNew[(tour[i].r*pObj.boardSize+tour[i].c)*8+tour[i].k] += tour[i].t



        # update pheromone amounts on network, reset accumulator
        for i in range(0,len(tNew)):
            pObj.tNet[i] += tNew[i]
            tNew[i] = 0


if __name__ == "__main__":
    main()

