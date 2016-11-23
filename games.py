# python -m SimpleHTTPServer 8080

import os
import xmltodict
import json
import collections


def str2bool(string):
	return string.lower() in ('true')


def getFiles(folder):

	files = []

	for dirpath, dirnames, filenames in os.walk(folder):

		for filename in [file for file in filenames if file == 'gamelist.xml']:

			path = os.path.join(dirpath, filename).replace('\\', '/')

			files.append(path)

	return files


def parseFile(file):

	system = 'Unknown'

	games = []

	_xml = open(file, 'r').read()

	_dict = xmltodict.parse(_xml)

	gameList = _dict['gameList']

	if gameList is None:

		gameList = {}

	if '@system' in gameList:

		system = gameList['@system']

	if 'game' in gameList:

		games = gameList['game']

	if isinstance(games, list) is False:

		games = [games]

	return system, games


def processGames(games):

	processedGames = []

	for game in games:

		processedGame = {
			'name': game['name'],
			'players': 1,
			'tested': False,
			'multiplayer': {
				'simultaneous-coop': False,
				'alternating-coop': False,
				'simultaneous-vs': False,
				'alternating-vs': False,
			}
		}

		if 'players' in game and game['players'] is not None:

			processedGame['players'] = game['players'].strip('+')
			processedGame['players'] = int(processedGame['players'])

		if 'multiplayer' in game:

			processedGame['tested'] = True

			processedGame['multiplayer']['simultaneous-coop'] = str2bool(game['multiplayer']['@simultaneous-coop'])
			processedGame['multiplayer']['alternating-coop'] = str2bool(game['multiplayer']['@alternating-coop'])
			processedGame['multiplayer']['simultaneous-vs'] = str2bool(game['multiplayer']['@simultaneous-vs'])
			processedGame['multiplayer']['alternating-vs'] = str2bool(game['multiplayer']['@alternating-vs'])

		processedGames.append(processedGame)

	return processedGames


def getGames(folder):

	games = {}

	files = getFiles(folder)

	for file in files:

		system, unprocessedGames = parseFile(file)

		processedGames = processGames(unprocessedGames)

		if system in games and games[system] != processedGames:

			games[system] = games[system] + processedGames

		else:

			games[system] = processedGames

	games = collections.OrderedDict(sorted(games.items()))

	games = json.dumps(games, indent=4, sort_keys=True)

	return games


games = getGames('//RETROPIE/roms/')

open('games.json', 'w').write(games)
