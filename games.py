# python -m SimpleHTTPServer 8080

import os
import xmltodict
import json
import collections

games = {
	'Arcade': '/retropie/roms/arcade/gamelist.xml',
	'Atari 2600': '/retropie/roms/atari2600/gamelist.xml',
	'Atari 7800': '/retropie/roms/atari7800/gamelist.xml',
	'Atari Lynx': '/retropie/roms/atarilynx/gamelist.xml',
	'Sega Gamegear': '/retropie/roms/gamegear/gamelist.xml',
	'Game Boy': '/retropie/roms/gb/gamelist.xml',
	'Game Boy Advance': '/retropie/roms/gba/gamelist.xml',
	'Game Boy Color': '/retropie/roms/gbc/gamelist.xml',
	'Intellivision': '/retropie/roms/intellivision/gamelist.xml',
	'Sega Master System': '/retropie/roms/mastersystem/gamelist.xml',
	'Sega Genesis': '/retropie/roms/megadrive/gamelist.xml',
	'MSX / MSX2': '/retropie/roms/msx/gamelist.xml',
	'Nintendo 64': '/retropie/roms/n64/gamelist.xml',
	'Nintendo Entertainment System': '/retropie/roms/nes/gamelist.xml',
	'Neo Geo Pocket': '/retropie/roms/ngp/gamelist.xml',
	'Neo Geo Pocket (Color)': '/retropie/roms/ngpc/gamelist.xml',
	'TurboGrafx 16': '/retropie/roms/pcengine/gamelist.xml',
	'PlayStation': '/retropie/roms/psx/gamelist.xml',
	'Sega 32X': '/retropie/roms/sega32x/gamelist.xml',
	'Sega CD': '/retropie/roms/segacd/gamelist.xml',
	'Sega SG-1000': '/retropie/roms/sg-1000/gamelist.xml',
	'Super Nintendo': '/retropie/roms/snes/gamelist.xml',
	'Virtual Boy': '/retropie/roms/virtualboy/gamelist.xml',
}

for system, path in games.iteritems():

	gameList = None

	gameNames = []

	if os.path.isfile(path):

		_xml = open(path, 'r').read()

		_dict = xmltodict.parse(_xml)

		gameList = dict(_dict.items())['gameList']

		if gameList is not None:

			gameList = dict(gameList.items())['game']

	for game in gameList or []:

		gameName = dict(game.items())['name']

		gameNames.append(gameName)

	games[system] = gameNames


games = collections.OrderedDict(sorted(games.items()))

_json = json.dumps(games)

# print _json
open('games.json', 'w').write(_json)
