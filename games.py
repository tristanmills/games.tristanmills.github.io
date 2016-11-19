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

	system = ''
	games = []

	_games = []

	if os.path.isfile(file):

		_xml = open(file, 'r').read()

		_dict = xmltodict.parse(_xml)

		gameList = dict(_dict.items())['gameList']

		gameList = dict(gameList.items())

		system = gameList['@system']

		if 'game' in gameList:

			_games = gameList['game']

	for _game in _games:

		_game = dict(_game.items())

		game = {
			'name': _game['name'],
			'players': 1,
			'tested': False,
			'multiplayer': {
				'simultaneous-coop': False,
				'alternating-coop': False,
				'simultaneous-vs': False,
				'alternating-vs': False,
			}
		}

		if 'players' in _game and _game['players'] > 1:

			game['players'] = int(_game['players'])

		if 'multiplayer' in _game:

			_multiplayer = dict(_game['multiplayer'])

			game['tested'] = True

			game['multiplayer']['simultaneous-coop'] = str2bool(_multiplayer['@simultaneous-coop'])
			game['multiplayer']['alternating-coop'] = str2bool(_multiplayer['@alternating-coop'])
			game['multiplayer']['simultaneous-vs'] = str2bool(_multiplayer['@simultaneous-vs'])
			game['multiplayer']['alternating-vs'] = str2bool(_multiplayer['@alternating-vs'])

		games.append(game)

	return system, games


def getGames(folder):

	games = {}

	files = getFiles(folder)

	for file in files:

		system, _games = parseFile(file)

		games[system] = _games

	games = collections.OrderedDict(sorted(games.items()))

	games = json.dumps(games, indent=4, sort_keys=True)

	return games


games = getGames('/retropie/roms/')

# print games
open('games.json', 'w').write(games)
