#
# Slide Puzzle - logic.py
#
# Jonatan H Sundqvist
# August 6 2014
#


# TODO | - Grid utility
#		 - Clarify Tile nomenclature (position tile and logical tile)


# SPEC | - 
#		 -


# TODO: Use randint to scramble (?)
from collections import namedtuple
from random import randint, choice


Tile 	= namedtuple('Tile', 'col row')
Puzzle  = namedtuple('Puzzle', 'tiles, cols rows empty')


def createPuzzle(columns : int, rows : int) -> Puzzle:
	''' Creates a 2D array of tiles, each tile storing its original position and returns it alongside related data '''
	return Puzzle([[Tile(col, row) for row in range(rows)] for col in range(columns)], columns, rows, Tile(randint(0, columns-1), randint(0, rows-1)))


def randomPair(puzzle : Puzzle) -> Tile:
	''' Selects a random pair of tiles '''
	fst = randint(0, puzzle.cols-1), randint(0, puzzle.rows-1) # Column and row of first tile
	snd = randint(0, puzzle.cols-1), randint(0, puzzle.rows-1) # Column and row of second tile
	return Tile(*fst), Tile(*snd)


# Query functions
def chooseTile(puzzle : Puzzle, tile : Tile) -> Tile:
	return puzzle.tiles[tile.col][tile.row]


def chooseColumn(puzzle : Puzzle, column : int):
	return puzzle.tiles[column]


def chooseRow(puzzle : Puzzle, row : int):
	return [column[row] for column in puzzle.tiles]


def loopTiles(puzzle : Puzzle):
	''' Iterates all tiles, yielding its current and proper position as a tuple of Tiles '''
	for nCol, column in enumerate(puzzle.tiles):
		for nRow, tile in enumerate(column):
			yield Tile(nCol, nRow), tile


def loopAdjacent(puzzle, tile):
	''' Iterates adjacent tiles '''
	for c, r in ((0,1), (0,-1), (1,0), (-1,0)):
		adjacent = Tile(c+tile.col, r+tile.row)
		if withinBounds(puzzle, adjacent):
			yield adjacent
		else:
			continue


#def findEmpty(puzzle):
#	pass


def swapTiles(puzzle : Puzzle, first : Tile, second : Tile) -> Puzzle:
	''' Swaps two tiles (in-place) in a puzzle '''
	fstTile = chooseTile(puzzle, first)
	sndTile = chooseTile(puzzle, second)
	puzzle.tiles[first.col][first.row], puzzle.tiles[second.col][second.row] = sndTile, fstTile
	return puzzle


def isEmpty(puzzle : Puzzle, tile : Tile) -> bool:
	''' Determines if the tile at the specified position is empty '''
	return chooseTile(puzzle, tile) == puzzle.empty


# TODO: Allow callbacks (?)
def scramblePuzzle(puzzle : Puzzle) -> Puzzle:
	''' Scrambles the puzzle by making a series of random moves '''
	# TODO: Make sure this never results in impossible puzzles (✓)
	# TODO: 
	# TODO: Specify degree of randomness
	# Python findIf (?)
	empty = [pos for pos, tile in loopTiles(puzzle) if isEmpty(puzzle, pos)][0]

	# Swaps empty tile with one of its adjacents for as many times as there are tiles
	# This algorithm is not ideal and sometimes produces very orderly puzzles
	# A simple solution would be to increase the number of iterations
	for n in range(puzzle.cols*puzzle.rows):
		#fst, snd = randomPair(puzzle)
		adjacent = choice([adj for adj in loopAdjacent(puzzle, empty)])
		swapTiles(puzzle, empty, adjacent)
		empty = adjacent
	return puzzle


def withinBounds(puzzle : Puzzle, tile : Tile) -> bool:
	return (0 <= tile.col < puzzle.cols) and (0 <= tile.row < puzzle.rows)


def move(puzzle : Puzzle, tile : Tile) -> '(didMove, tile, didWin)':
	''' Attempts to move the chosen tile, returns the outcome '''
	# TODO: Additional information (eg. reason for not moving) (✓)
	for c, r in ((0,1), (0,-1), (1,0), (-1,0)):
		adjacent = Tile(c+tile.col, r+tile.row)
		if withinBounds(puzzle, adjacent) and isEmpty(puzzle, adjacent):
			swapTiles(puzzle, tile, adjacent)
			return True, adjacent, checkVictory(puzzle)
	return False, None, False


# Game play
def checkVictory(puzzle : Puzzle) -> bool:
	return all(actual == correct for actual, correct in loopTiles(puzzle))


# Debugging
def renderRow(puzzle : Puzzle, row : int) -> str:
	return '[%s]' % ' '.join('(%d, %d)' % tile for tile in chooseRow(puzzle, row))


def renderGrid(puzzle : Puzzle):
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