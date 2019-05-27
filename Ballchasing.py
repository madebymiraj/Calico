import argparse
import sys
import asyncio
import time
from Uploader import Uploader
from pprint import pprint

def main():

	args = parseArguments()
	uploader = Uploader(args)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(uploader.asyncUpload())
	uploader.logResponses(uploader.asyncPayloads)	

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

	if demoPath is not None:
		if (demoPath[-1] is not '/'):
			demoPath = demoPath + '/'
		elif (demoPath[-1] is not '\\'):
			demoPath = demoPath + '\\\\'

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