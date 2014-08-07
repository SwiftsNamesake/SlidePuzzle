#
# Slide Puzzle - main.py
#
# Jonatan H Sundqvist
# August 6 2014
#


# TODO | - Grid utility
#		 -


# SPEC | - 
#		 -


import tkinter as tk

from tkinter import filedialog
from PIL.ImageTk import PhotoImage, Image
from random import randint, choice
from collections import namedtuple


import logic
import graphics
import interaction


tile = namedtuple('tile', 'tkPhoto pos photo isEmpty') # TODO: Separate row and col (?)
puzzle = {}

def loadImageTiles(fn):
	''' '''
	pass


def handleMove(col, row, puzzle):
	''' '''

	#print(puzzle['tiles'][col][row])

	if puzzle['tiles'][col][row].isEmpty:
		# Empty tile
		#print('Can\'t move an empty tile')
		return False, False # Did not move, Did not win

	for c, r in ((0,1), (0,-1), (1,0), (-1,0)):
		cAdj,rAdj  = col+c, row+r # Adjacent column and row
		#print(cAdj, rAdj)
		if (0 <= cAdj < puzzle['nCols']) and (0 <= rAdj < puzzle['nRows']) and puzzle['tiles'][cAdj][rAdj].isEmpty:
			# Adjacent tile is empty
			#print('Moving tile')
			#print((col, row), (cAdj, rAdj))
			updateTiles(puzzle, (col, row), (cAdj, rAdj))
			return True, checkVictory(puzzle)
	else:
		#print('Can\'t move, no adjacent empty tiles')
		pass


#def onClick(event):
#	''' '''
#	pass


def bindEvents(widget):
	''' Binds mouse behaviour to widget '''
	def onEnter(event):
		#frame[0].config(bd=0)
		pass

	def onLeave(event):
		#frame[0].config(bd=0)
		pass

	def onClick(event):
		#print('Handling move')
		print('Col', widget[1], 'Row', widget[2])
		handleMove(widget[1], widget[2], puzzle)

	widget[0].bind('<Enter>', onEnter)
	widget[0].bind('<Leave>', onLeave)
	widget[0].bind('<Button-1>', onClick)

	return onEnter, onLeave, onClick


def createTile(image, column, row, width, height, isEmpty):
	''' '''
	if not isEmpty:
		photo = image.crop((column*width, row*height, (column+1)*width, (row+1)*height))
	else:
		photo = Image.new('RGB', (width, height), 'white') # Create white tile
	return tile(PhotoImage(photo), (column, row), photo, isEmpty) # TODO: Remove photo (?)


def createFrame(tile, width, height):

	''' '''
	# TODO: Attach image to frame (?)
	frame = tk.Label(width=width, height=height, anchor=tk.NW, image=tile[0], bd=5, cursor='hand2')
	frame.grid(column=tile.pos[0], row=tile.pos[1])

	frameTile = (frame, tile.pos[0], tile.pos[1]) 
	bindEvents(frameTile)

	return frameTile


def scramblePuzzle(puzzle):
	''' '''
	pass


def createPuzzle(fn : str, rows : int, columns : int, size : tuple, title : str):

	''' '''

	# TODO: Separate rendering from logic
	# TODO: Find an elegant way of coupling tiles to frames and keeping them in sync
	# TODO: Should tiles be in a constant order, seperate index array (?)
	# TODO: CLean up e
	# TODO: Formatting options

	# Initialize properties
	image = Image.open(fn)
	width, height 	= image.size[0]//columns, image.size[1]//rows 	# Width and height of each tile
	blankCol, blankRow 	= randint(0, columns-1), randint(0, rows-1) # Choose an empty tile randomly
	
	# Create and configure window
	window = tk.Tk()
	window.resizable(width=False, height=False)
	#window.geometry('%dx%d' % (image.size[0], image.size[1]))
	window.title(title)
	
	# Create image tiles
	tiles = [ [createTile(image, column, row, width, height, (row, column) == (blankCol, blankRow)) for row in range(rows)] for column in range(columns)]
	frames = [ [createFrame(tile, width, height) for tile in column] for column in tiles ]

	return {
		'window': window,
		'title': title,
		'size': size,
		'image': image,
		'tiles': tiles,
		'frames': frames,
		'nRows': rows,
		'nCols': columns,
		'width': width,
		'height': height
	}


def swap(first, second):
	return second, first


def updateTiles(puzzle : dict, first : tuple, second : tuple):
	''' Swaps two tiles in the puzzle '''

	#print('Updating tiles')
	tileOne = puzzle['tiles'][first[0]][first[1]]
	tileTwo = puzzle['tiles'][second[0]][second[1]]

	puzzle['tiles'][first[0]][first[1]], puzzle['tiles'][second[0]][second[1]] = tileTwo, tileOne

	puzzle['frames'][first[0]][first[1]][0].config(image=tileTwo.tkPhoto)
	puzzle['frames'][first[0]][first[1]] = puzzle['frames'][first[0]][first[1]][0], tileTwo.pos[0], tileTwo.pos[1]

	puzzle['frames'][second[0]][second[1]][0].config(image=tileOne.tkPhoto)
	puzzle['frames'][second[0]][second[1]] = puzzle['frames'][second[0]][second[1]][0], tileOne.pos[0], tileOne.pos[1]


def checkVictory(puzzle):
	''' '''
	win = all(tile.pos == (nRow, nCol) for nCol, col in enumerate(puzzle['tiles']) for nRow, tile in enumerate(col) )
	return win


def main():
	''' '''
	global puzzle
	#puzzle = createPuzzle('C:/Users/Jonatan/Desktop/Python/resources/euler.jpeg', 5, 5, (400, 400), 'Save Euler')
	puzzle = createPuzzle(filedialog.askopenfilename(), int(input('How many columns?')), int(input('How many rows?')), (400, 400), 'Save Euler')
	puzzle['window'].mainloop()


def refactored():
	#settings = interaction.askSettings()
	#namedtuple('Settings', 'image size cols rows')
	settings = interaction.Settings('C:/Users/Jonatan/Pictures/bild.JPG', 400, 4, 4)
	image 	 = interaction.resizeImage(settings.image, settings.size)
	window 	 = tk.Tk()
	window.title('Solve the Puzzle')
	window.resizable(width=False, height=False)
	puzzle 	 = logic.createPuzzle(settings.cols, settings.rows)
	logic.scramblePuzzle(puzzle)
	renderer = graphics.createRenderer(window, puzzle, image)
	for frame in graphics.loopFrames(renderer):
		graphics.bindEvents(frame, renderer)
	window.mainloop()


if __name__ == '__main__':
	modular = True
	if modular:
		refactored()
	else:
		main()