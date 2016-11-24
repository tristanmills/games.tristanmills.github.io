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
			'tested': {
				'pi0': None,
				'pi3': None,
			},
			'multiplayer': {
				'simultaneous-coop': None,
				'alternating-coop': None,
				'simultaneous-vs': None,
				'alternating-vs': None,
			}
		}

		if 'players' in game and game['players'] is not None:

			processedGame['players'] = game['players'].strip('+')
			processedGame['players'] = int(processedGame['players'])

		if 'multiplayer' in game:

			processedGame['multiplayer']['simultaneous-coop'] = str2bool(game['multiplayer']['@simultaneous-coop'])
			processedGame['multiplayer']['alternating-coop'] = str2bool(game['multiplayer']['@alternating-coop'])
			processedGame['multiplayer']['simultaneous-vs'] = str2bool(game['multiplayer']['@simultaneous-vs'])
			processedGame['multiplayer']['alternating-vs'] = str2bool(game['multiplayer']['@alternating-vs'])

		if 'tested' in game:

			if '@pi0' in game['tested']:

				processedGame['tested']['pi0'] = str2bool(game['tested']['@pi0'])

			if '@pi3' in game['tested']:

				processedGame['tested']['pi3'] = str2bool(game['tested']['@pi3'])

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


folder = '/retropie/roms/'
# folder = '//RETROPIE/roms/'

games = getGames(folder)

open('games.json', 'w').write(games)
