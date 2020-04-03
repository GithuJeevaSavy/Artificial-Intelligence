package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const boardSize = 8
const nSquares = boardSize * boardSize
const completeTour = nSquares - 1

// task input: starting square.  These are 1 based, but otherwise 0 based
// row and column numbers are used througout the program.
const rStart = 1
const cStart = 1

// pheromone representation read by ants
var tNet = make([]float64, nSquares*8)

// row, col deltas of legal moves
var drc = [][]int{{1, 2}, {2, 1}, {2, -1}, {1, -2},
	{-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}}

// get square reached by following edge k from square (r, c)
func dest(r, c, k int) (int, int, bool) {
	r += drc[k][0]
	c += drc[k][1]
	return r, c, r >= 0 && r < boardSize && c >= 0 && c < boardSize
}

// struct represents a pheromone amount associated with a move
type rckt struct {
	r, c, k int
	t       float64
}

func main() {
	fmt.Println("Starting square:  row", rStart, "column", cStart)
	// initialize board
	for r := 0; r < boardSize; r++ {
		for c := 0; c < boardSize; c++ {
			for k := 0; k < 8; k++ {
				if _, _, ok := dest(r, c, k); ok {
					tNet[(r*boardSize+c)*8+k] = 1e-6
				}
			}
		}
	}
