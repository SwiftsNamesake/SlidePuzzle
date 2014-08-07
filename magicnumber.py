#
# Showing Jay how it might be done
#
# Jonatan H Sundqvist
# August 6 2014


from random import randint


def accept(mini, maxi):
	''' Accepts and validates input from the player '''
	guess = input('Guess a number between %d and %d: ' % (mini, maxi))
	while not guess.isdigit():
		guess = input('Sorry, that\'s not a number. Guess again!')
	return int(guess)


def makeGuess(right, guess):
	''' Checks if a guess is correct, returns True if it is '''
	if guess == right:
		print('Hurray, you found it! The answer is \'%d\'!' % right)
		return True
	elif guess > right:
		print('Sorry, too high.')
		return False
	else:
		print('Sorry, too low')
		return False


def playRound():
	''' Plays one round of the game '''
	mini, maxi = 0, 25
	answer = randint(mini, maxi)
	print(answer)
	while not makeGuess(answer, accept(mini, maxi)):
		# Keep guessing while as long as the answer is not correct
		pass


def main():
	''' Plays the game once '''
	#playRound()
	yes, no = (['yes', 'y'], ['No', 'N'])
	while input('Good job! Play again? [Yes/No] ').lower() in yes:
		playRound()
	input()


if __name__ == '__main__':
	main()