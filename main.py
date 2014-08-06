#
# Slide Puzzle - main.py
#
# Jonatan H Sundqvist
# August 6 2014
#


import tkinter
from PIL.ImageTk import PhotoImage, Image
from random import randint


def loadImageTiles(fn):
	''' '''
	pass


def handleMove(x, y, puzzle):
	''' '''
	pass


def onClick(event):
	''' '''
	pass


def createPuzzle(fn, rows, columns):

	''' '''

	image = Image.open(fn)
	width, height 	= image.size[0]//columns, image.size[1]//rows 	# Width and height of each tile
	blankX, blankY 	= randint(rows), randint(columns) 				# Choose an empty tile randomly
	
	puzzle = [ [PhotoImage(image.crop((column*width, row*height, (column+1)*width, (row+1)*height))) for row in range(rows)] for column in range(columns)]
	puzzle[blankX][blankY] = None

	return puzzle


def updateTiles(puzzle):
	''' '''
	pass


def main():
	''' '''
	pass

if __name__ == '__main__':
	main()