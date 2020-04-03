import threading
import time
from typing import NamedTuple

class Problem:

    def __init__(self):


        self.boardSize = 8
        self.nSquares = boardSize * boardSize
        self.completeTour = nSquares - 1

        # task input: starting square.  These are 1 based, but otherwise 0 based
        # row and column numbers are used througout the program.
        self.rStart = 2
        self.cStart = 3

        # pheromone representation read by ants


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

class rckt(NamedTuple):
    r: int
    c: int
    k: int
    t: float



def main(self):
    print("Starting square:  row", self.rStart, "column", self.cStart)
    # initialize board
    for r in range(0, self.boardSize):
        for c in range(0, self.boardSize):
            for k in range(0, 8):
                if self.dest(r, c, k):
                    tNet[(r*boardSize+c)*8+k] = 1e-6



    # waitGroups for ant release clockwork

    self.start.Add(1)
    # channel for ants to return tours with pheremone updates
    self.tch =  rckt(NamedTuple)


    # create an ant for each square
    for r in range(0, self.boardSize):
        for c in range(0, self.boardSize):
            ant(r, c, self.start, &reset, tch)
        }
    }

    # accumulator for new pheromone amounts
    tNew := make([]float64, nSquares*8)

    # each iteration is a "cycle" as described in the paper
    for {
        # evaporate pheromones
        for i := range tNet {
            tNet[i] *= .75
        }

        reset.Add(nSquares) // number of ants to release
        start.Done()        // release them
        reset.Wait()        // wait for them to begin searching
        start.Add(1)        // reset start signal for next cycle

        // gather tours from ants
        for i := 0; i < nSquares; i++ {
            tour := <-tch
            // watch for a complete tour from the specified starting square
            if len(tour) == completeTour &&
                tour[0].r == rStart-1 && tour[0].c == cStart-1 {

                // task output:  move sequence in a grid.
                seq := make([]int, nSquares)
                for i, sq := range tour {
                    seq[sq.r*boardSize+sq.c] = i + 1
                }
                last := tour[len(tour)-1]
                r, c, _ := dest(last.r, last.c, last.k)
                seq[r*boardSize+c] = nSquares
                fmt.Println("Move sequence:")
                for r := 0; r < boardSize; r++ {
                    for c := 0; c < boardSize; c++ {
                        fmt.Printf(" %3d", seq[r*boardSize+c])
                    }
                    fmt.Println()
                }
                return // task only requires finding a single tour
            }
            // accumulate pheromone amounts from all ants
            for _, move := range tour {
                tNew[(move.r*boardSize+move.c)*8+move.k] += move.t
            }
        }

        // update pheromone amounts on network, reset accumulator
        for i, tn := range tNew {
            tNet[i] += tn
            tNew[i] = 0
        }
    }
}

type square struct {
    r, c int
}

func ant(r, c int, start, reset *sync.WaitGroup, tourCh chan []rckt) {
    rnd := rand.New(rand.NewSource(time.Now().UnixNano()))
    tabu := make([]square, nSquares)
    moves := make([]rckt, nSquares)
    unexp := make([]rckt, 8)
    tabu[0].r = r
    tabu[0].c = c

    for {
        // cycle initialization
        moves = moves[:0]
        tabu = tabu[:1]
        r := tabu[0].r
        c := tabu[0].c

        // wait for start signal
        start.Wait()
        reset.Done()

        for {
            // choose next move
            unexp = unexp[:0]
            var tSum float64
        findU:
            for k := 0; k < 8; k++ {
                dr, dc, ok := dest(r, c, k)
                if !ok {
                    continue
                }
                for _, t := range tabu {
                    if t.r == dr && t.c == dc {
                        continue findU
                    }
                }
                tk := tNet[(r*boardSize+c)*8+k]
                tSum += tk
                // note:  dest r, c stored here
                unexp = append(unexp, rckt{dr, dc, k, tk})
            }
            if len(unexp) == 0 {
                break // no moves
            }
            rn := rnd.Float64() * tSum
            var move rckt
            for _, move = range unexp {
                if rn <= move.t {
                    break
                }
                rn -= move.t
            }

            // move to new square
            move.r, r = r, move.r
            move.c, c = c, move.c
            tabu = append(tabu, square{r, c})
            moves = append(moves, move)
        }

        // compute pheromone amount to leave
        for i := range moves {
            moves[i].t = float64(len(moves)-i) / float64(completeTour-i)
        }

        // return tour found for this cycle
        tourCh <- moves
    }
}
