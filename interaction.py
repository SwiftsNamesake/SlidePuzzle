#
# Slide Puzzle - interaction.py
#
# Jonatan H Sundqvist
# August 7 2014
#


# TODO | - 
#		 - 


# SPEC | - 
#		 -


import tkinter as tk

from os import path
from collections import namedtuple
from PIL import Image, ImageTk


Settings = namedtuple('Settings', 'image size cols rows')


def askUntil(condition : 'function', query : str, followup : 'function') -> str:
	''' Asks for input until condition is met. Allows tailored responses by passing reply into followup callback '''
	# TODO: Added number of times asked as argument to callback
	# TODO: Allow break-out conditions
	reply = input(query)
	while not condition(reply):
		reply = input(followup(reply))
	return reply


def makePathValidator(supported):
	def isValidPath(reply):
		exists 	 = path.isfile(reply)
		validExt = path.splitext(reply)[-1][1:].lower() in supported # Make sure the file type (lowercase, dot removed) is supported
		return exists and validExt
	return isValidPath


def makeSizeCallbacks(mini, maxi):
	
	def isValidSize(reply):
		return (reply == 'no') or (reply.isdigit() and (mini <= int(reply) <= maxi))
	
	def sizeFollowup(reply):
		return 'The size must be between %d and %d px. Choose another size... ' % (mini, maxi)
	
	return isValidSize, sizeFollowup


def makeGridCallbacks(mini, maxi):

	def isValidGrid(reply):
		return reply.isdigit() and (mini <= int(reply) <= maxi)

	def gridFollowUp(reply):
		return 'Sorry, that is not a valid reply. Make sure your reply is within range and only contains digits... '

	return isValidGrid, gridFollowUp


def askImage(supported=['png', 'jpg', 'jpeg', 'gif', 'bmp']):
	# TODO: Make sure the list of supported file formats is exhaustive
	fn = askUntil(makePathValidator(supported), 'Choose a file... ', lambda reply: 'I am sorry, that is not a valid path.\nChoose another one... ')
	return fn


def askSize():
	''' '''
	# TODO: Adapt to screen, etc.
	mini, maxi 	 = (100, 500) # Valid range for size
	cond, follow = makeSizeCallbacks(mini, maxi)
	query = 'Scale the image? Put down the maximum (pixels) or reply no to skip... '
	size = askUntil(cond, query, follow)
	return None if size == 'no' else int(size)


def askColumnsRows():
	''' '''
	mini, maxi = (2, 10)
	isValidGrid, followup = makeGridCallbacks(mini, maxi)
	cols = askUntil(isValidGrid, 'How many columns [%d-%d]? ' % (mini, maxi), followup)
	rows = askUntil(isValidGrid, 'How many rows [%d-%d]? ' % (mini, maxi), followup)
	return int(cols), int(rows)


def resizeImage(fn, maxi):
	''' Creates and (optionally) resizes an image based on the maximum length for either side '''
	# TODO: Implement minium values and percentage scaling
	image = Image.open(fn)
	if maxi is not None:
		ratio = maxi/max(*image.size)
		image.thumbnail((int(image.size[0]*ratio), int(image.size[1]*ratio)), Image.ANTIALIAS)
	return image


def askSettings():
	''' '''
	return Settings(askImage(), askSize(), *askColumnsRows())


def createWindow():
	window 	 = tk.Tk()
	window.title('Solve the Puzzle')
	window.resizable(width=False, height=False)
	window.call('wm', 'iconphoto', window._w, ImageTk.PhotoImage(Image.open('icon.png')))
	return window


def bindEvents():
	pass


# Test suite
def main():
	print(askSettings())


if __name__ == '__main__':
	main()