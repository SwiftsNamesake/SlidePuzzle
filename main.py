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
	# settings = interaction.Settings('C:/Users/Jonatan/Pictures/2013-10-27/IMG_0017.JPG', 400, 4, 4)
	settings = interaction.askSettings()								# Prompt user for settings (console)
	image 	 = interaction.resizeImage(settings.image, settings.size)	# Resize window based on settings, if necessary
	window 	 = interaction.createWindow()								# Create and configure window
	puzzle 	 = logic.createPuzzle(settings.cols, settings.rows)			# Create a new puzzle, with the desired settings
	logic.scramblePuzzle(puzzle)										# Scramble it
	renderer = graphics.createRenderer(window, puzzle, image)			# Renders puzzle tiles with the selected image
	graphics.bindEvents(renderer)										# Attach click event handlers
	window.mainloop()													# Enter main loop (start the game)


if __name__ == '__main__':
	main()
