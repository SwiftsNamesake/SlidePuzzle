#
# Slide Puzzle - logic.py
#
# Jonatan H Sundqvist
# August 6 2014
#


# TODO | - Grid utility
#		 -


# SPEC | - 
#		 -


# TODO: Use randint to scramble (?)
from collections import namedtuple
from random import randint, choice


Tile 	= namedtuple('Tile', 'col row')
Puzzle  = namedtuple('Puzzle', 'tiles, cols rows empty')


def createPuzzle(columns, rows):
	''' Creates a 2D array of tiles, each tile storing its original position '''
	return Puzzle([[Tile(col, row) for row in range(rows)] for col in range(columns)], columns, rows, Tile(randint(0, columns-1), randint(0, rows-1)))


def randomPair(puzzle : list) -> Tile:
	fst = randint(0, len(puzzle)-1), randint(0, len(puzzle[0])-1) # Column and row of first tile
	snd = randint(0, len(puzzle)-1), randint(0, len(puzzle[0])-1) # Column and row of second tile
	return Tile(*fst), Tile(*snd)


# Query functions
def chooseTile(puzzle, tile) -> Tile:
	return puzzle.tiles[tile.col][tile.row]


def chooseColumn(puzzle, column):
	return puzzle.tiles[column]


def chooseRow(puzzle, row):
	return [column[row] for column in puzzle.tiles]


def loopTiles(puzzle):
	for nCol, column in enumerate(puzzle.tiles):
		for nRow, tile in enumerate(column):
			yield Tile(nCol, nRow), tile


def swapTiles(puzzle : list, first : Tile, second : Tile):
	''' Swaps to tiles (in-place) in a puzzle '''
	fstTile = chooseTile(puzzle, first)
	sndTile = chooseTile(puzzle, second)
	puzzle.tiles[first.col][first.row], puzzle.tiles[second.col][second.row] = sndTile, fstTile
	return puzzle


def isEmpty(puzzle : list, tile) -> bool:
	return chooseTile(puzzle, tile) == puzzle.empty


# TODO: Allow callbacks (?)
def scramblePuzzle(puzzle):
	for n in range(puzzle.cols*puzzle.rows):
		fst, snd = randomPair(puzzle)
		if fst == snd: continue
		swapTiles(puzzle, fst, snd)
	return puzzle


def withinBounds(puzzle, tile):
	return (0 <= tile.col < puzzle.cols) and (0 <= tile.row < puzzle.rows)


def move(puzzle, tile):
	# TODO: Additional information (eg. reason for not moving) (✓)
	for c, r in ((0,1), (0,-1), (1,0), (-1,0)):
		adjacent = Tile(c+tile.col, r+tile.row)
		if withinBounds(puzzle, adjacent) and isEmpty(puzzle, adjacent):
			swapTiles(puzzle, tile, adjacent)
			return True, adjacent, checkVictory(puzzle)
	return False, None, False


# Game play
def checkVictory(puzzle):
	return all(actual == correct for actual, correct in loopTiles(puzzle))


# Debugging
def renderRow(puzzle, row):
	return '[%s]' % ' '.join('(%d, %d)' % tile for tile in chooseRow(puzzle, row))


def renderGrid(puzzle):
	''' Outputs a prettified rendition to the console '''
	print('\n'.join(renderRow(puzzle, row) for row in range(puzzle.rows)))


# Test suite
def main():
	puzzle = createPuzzle(5,5)
	renderGrid(puzzle)
	print('\n')

	puzzle = scramblePuzzle(puzzle)
	renderGrid(puzzle)


if __name__ == '__main__':
	main()