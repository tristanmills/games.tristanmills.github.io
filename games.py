# python -m SimpleHTTPServer 8080

import xmltodict
import json
import collections

games = {
	'Arcade': '/retropie/roms/arcade/gamelist.xml',
	'Atari 2600': '/retropie/roms/atari2600/gamelist.xml',
}

for system, path in games.iteritems():

	_xml = open(path, 'r').read()

	_dict = xmltodict.parse(_xml)

	gameList = dict(_dict.items())['gameList']

	if gameList is not None:

		gameList = dict(gameList.items())['game']

	gameNames = []

	for game in gameList or []:

		gameName = dict(game.items())['name']

		gameNames.append(gameName)

	games[system] = gameNames


collections.OrderedDict(sorted(games.items()))

_json = json.dumps(games)

# print _json
open('games.json', 'w').write(_json)
