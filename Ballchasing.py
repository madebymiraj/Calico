import argparse
import sys
from Uploader import Uploader
from pprint import pprint

def main():

	args = parseArguments()
	uploader = Uploader(args)
	uploader.upload()
	

def parseArguments():

	possibleArguments = ['-p', '-v']
	visibilityOptions = ['public', 'private', 'unlisted']
	args = sys.argv[1:]

	# Demo Path
	if '-p' in args:
		nextArg = args[args.index('-p') + 1]
		if nextArg not in possibleArguments:
			demoPath = nextArg
		else:
			demoPath = None
	else:
		demoPath = None

	# Visibility
	if '-v' in args:
		nextArg = args[args.index('-v') + 1]
		if nextArg not in possibleArguments:
			visibility = nextArg
		else:
			visibility = None
	else:
		visibility = None

	if visibility is None: visibility = 'public'

	if visibility not in visibilityOptions:
		sys.exit('Not a valid visibility parameter')

	return [demoPath, visibility]



if __name__ == '__main__':
	main()