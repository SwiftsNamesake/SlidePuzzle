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


import logic
import graphics
import interaction


def main():
	# settings = interaction.Settings('C:/Users/Jonatan/Pictures/bild.JPG', 400, 4, 4)
	settings = interaction.askSettings()
	image 	 = interaction.resizeImage(settings.image, settings.size)
	window 	 = interaction.createWindow()
	puzzle 	 = logic.createPuzzle(settings.cols, settings.rows)
	logic.scramblePuzzle(puzzle)
	renderer = graphics.createRenderer(window, puzzle, image)
	for frame in graphics.loopFrames(renderer):
		graphics.bindEvents(frame, renderer)
	window.mainloop()


if __name__ == '__main__':
	main()