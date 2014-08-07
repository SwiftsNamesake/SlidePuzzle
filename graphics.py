#
# Slide Puzzle - graphics.py
#
# Jonatan H Sundqvist
# August 6 2014
#


# TODO | - Grid utility
#		 - Better names, consistent nomenclature
#		 - Use tiles (?)


# SPEC | - 
#		 -


import tkinter as tk
import logic

from collections import namedtuple
from PIL.ImageTk import Image, PhotoImage


Renderer = namedtuple('Renderer', 'frames pictures image puzzle cols rows empty')
Frame 	 = namedtuple('Frame', 'label tile')
Tile 	 = logic.Tile


# Image tiles
def createSection(image, width, height, column, row):
	return PhotoImage(image.crop((column*width, row*height, (column+1)*width, (row+1)*height)))


def createEmpty(width, height, colour='white'):
	return PhotoImage(Image.new('RGB', (width, height), colour)) # Create white tile


def createImageGrid(image, width, height, columns, rows, empty):
	# TODO: Scaling
	return [ [createSection(image, width, height, col, row) if (col, row) != empty else createEmpty(width, height) for row in range(rows)] for col in range(columns) ]


# Labels
def createFrame(col, row, image):
	label = tk.Label(image=image, anchor=tk.NW, bd=0, cursor='hand2')
	label.grid(column=col, row=row)
	return Frame(label, Tile(col, row))


def createFrameGrid(tiles, pictures):
	return [[createFrame(nCol, nRow, pictures[tile.col][tile.row]) for nRow, tile in enumerate(column)] for nCol, column in enumerate(tiles)]


# Queries
def loopFrames(renderer):
	for column in renderer.frames:
		for frame in column:
			yield frame


def loopImages(renderer):
	for nCol, column in enumerate(renderer.frames):
		for nRow, image in enumerate(column):
			yield Tile(nCol, nRow), frame


# Renderer
def createRenderer(window, puzzle, image) -> Renderer:
	pictures = createImageGrid(image, image.size[0]//puzzle.cols, image.size[1]//puzzle.rows, puzzle.cols, puzzle.rows, puzzle.empty)
	return Renderer(createFrameGrid(puzzle.tiles, pictures), pictures, image, puzzle, puzzle.cols, puzzle.rows, puzzle.empty)


def swapFrames(renderer, first, second):
	''' Updates frames after two tiles have been swapped '''
	fstTile = renderer.puzzle.tiles[first.col][first.row]
	sndTile = renderer.puzzle.tiles[second.col][second.row]
	renderer.frames[first.col][first.row].label.config(image=renderer.pictures[fstTile.col][fstTile.row])
	renderer.frames[second.col][second.row].label.config(image=renderer.pictures[sndTile.col][sndTile.row])


# TODO: Graphics module should probably not implement event handlers...
def bindEvents(frame, renderer):
	
	def onClick(event):
		moved, tile, victory = logic.move(renderer.puzzle, frame.tile)
		if moved:
			swapFrames(renderer, tile, frame.tile)
		if victory:
			print('Hurray!')

	frame.label.bind('<Button-1>', onClick)


def main():
	window = tk.Tk()
	puzzle = logic.createPuzzle(5, 5)
	logic.scramblePuzzle(puzzle)
	renderer = createRenderer(window, puzzle, Image.open('C:/Users/Jonatan/Pictures/2013-10-27/IMG_0017.JPG'))
	for frame in loopFrames(renderer):
		bindEvents(frame, renderer)
	window.mainloop()


if __name__ == '__main__':
	main()