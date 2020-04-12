package main

import (
    "fmt"
    "math/rand"
    "sync"
    "time"
)

const size = 8
const squares = size * size
const hamiltonianPath = squares - 1
const rowStart = 5
const colStart = 3

var pheroSquares = make([]float64, squares*8)

var validMoves = [][]int{{1, 2}, {2, 1}, {2, -1}, {1, -2},
    {-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}}

func validEdge(r, c, k int) (int, int, bool) {
    r += validMoves[k][0]
    c += validMoves[k][1]
    return r, c, r >= 0 && r < size && c >= 0 && c < size
}

type rckPheromone struct {
    r, c, k int
    t       float64
}

func main() {
    startT := time.Now()
    startTime := time.Now().UnixNano()
    fmt.Println(startTime)
    fmt.Println("Starting row: ", rowStart, "| Starting column: ", colStart)

    for r := 0; r < size; r++ {
        for c := 0; c < size; c++ {
            for k := 0; k < 8; k++ {
                if _, _, ok := validEdge(r, c, k); ok {
                    pheroSquares[(r*size+c)*8+k] = 1e-6
                }
            }
        }
    }

    var start, reset sync.WaitGroup
    start.Add(1)
    rckpObj := make(chan []rckPheromone)

    for r := 0; r < size; r++ {
        for c := 0; c < size; c++ {
            go ant(r, c, &start, &reset, rckpObj)
        }
    }

    pheroList := make([]float64, squares*8)

    for {
        for i := range pheroSquares {
            pheroSquares[i] *= .75
        }

        reset.Add(squares)
        start.Done()
        reset.Wait()
        start.Add(1)

        for i := 0; i < squares; i++ {
            tour := <-rckpObj
            if len(tour) == hamiltonianPath &&
                tour[0].r == rowStart-1 && tour[0].c == colStart-1 {

                seq := make([]int, squares)
                for i, sq := range tour {
                    seq[sq.r*size+sq.c] = i + 1
                }
                last := tour[len(tour)-1]
                r, c, _ := validEdge(last.r, last.c, last.k)
                seq[r*size+c] = squares
                fmt.Println("Move sequence:")
                for r := 0; r < size; r++ {
                    for c := 0; c < size; c++ {
                        fmt.Printf(" %3d", seq[r*size+c])
                    }
                    fmt.Println()
                }
                fmt.Println(time.Now().UnixNano())
                var duration = time.Now().UnixNano() - startTime
                elapsed := time.Since(startT)

                fmt.Println(duration)
                fmt.Println("ACO took %s", elapsed)
                return
            }
            for _, move := range tour {
                pheroList[(move.r*size+move.c)*8+move.k] += move.t
            }
        }

        for i, tn := range pheroList {
            pheroSquares[i] += tn
            pheroList[i] = 0
        }
    }
}

type square struct {
    r, c int
}

func ant(r, c int, start, reset *sync.WaitGroup, tourCh chan []rckPheromone) {
    rnd := rand.New(rand.NewSource(time.Now().UnixNano()))
    pathList := make([]square, squares)
    moves := make([]rckPheromone, squares)
    unExplored := make([]rckPheromone, 8)
    pathList[0].r = r
    pathList[0].c = c

    for {
        moves = moves[:0]
        pathList = pathList[:1]
        r := pathList[0].r
        c := pathList[0].c

        start.Wait()
        reset.Done()

        for {
            unExplored = unExplored[:0]
            var tSum float64
        findU:
            for k := 0; k < 8; k++ {
                dr, dc, ok := validEdge(r, c, k)
                if !ok {
                    continue
                }
                for _, t := range pathList {
                    if t.r == dr && t.c == dc {
                        continue findU
                    }
                }
                tk := pheroSquares[(r*size+c)*8+k]
                tSum += tk
                unExplored = append(unExplored, rckPheromone{dr, dc, k, tk})
            }
            if len(unExplored) == 0 {
                break
            }
            rn := rnd.Float64() * tSum
            var move rckPheromone
            for _, move = range unExplored {
                if rn <= move.t {
                    break
                }
                rn -= move.t
            }

            move.r, r = r, move.r
            move.c, c = c, move.c
            pathList = append(pathList, square{r, c})
            moves = append(moves, move)
        }

        for i := range moves {
            moves[i].t = float64(len(moves)-i) / float64(hamiltonianPath-i)
        }

        tourCh <- moves
    }
}
