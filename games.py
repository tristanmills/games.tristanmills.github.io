# python -m SimpleHTTPServer 8080

import os
import xmltodict
import json
import collections


def str2bool(string):
	return string.lower() in ('true')


def get_gameslists(folder):

	gameslists = {}

	for dirpath, dirnames, filenames in os.walk(folder):

		for filename in [file for file in filenames if file == 'gamelist.xml']:

			path = os.path.join(dirpath, filename).replace('\\', '/')

			system_name, games = parse_gameslist(path)

			gameslists[system_name] = games

	return gameslists


def parse_gameslist(file):

	games = []

	processedGames = []

	xml_ = open(file, 'r').read()

	dict_ = xmltodict.parse(xml_)

	gameList = dict_['gameList']

	if gameList is None:

		gameList = {}

	if '@system' in gameList:

		system = gameList['@system']

	if 'game' in gameList:

		games = gameList['game']

	if isinstance(games, list) is False:

		games = [games]

	for game in games:

		processedGame = {
			'name': game['name'],
			'description': game['desc'],
			'image': game['image'],
			'licensed': None,
			'releaseDate': None,
			'developer': None,
			'publisher': None,
			'genre': None,
			'players': 1,
			'multiplayer': {
				'simultaneous-coop': None,
				'alternating-coop': None,
				'simultaneous-vs': None,
				'alternating-vs': None,
			},
			'compatibility': {
				'pi0': None,
				'pi3': None,
			},
		}

		if 'licensed' in game:

			processedGame['licensed'] = str2bool(game['licensed'])

		if 'releasedate' in game:

			processedGame['releaseDate'] = game['releasedate']

		if 'developer' in game:

			processedGame['developer'] = game['developer']

		if 'publisher' in game:

			processedGame['publisher'] = game['publisher']

		if 'genre' in game:

			processedGame['genre'] = game['genre']

		if 'players' in game and game['players'] is not None:

			processedGame['players'] = game['players'].strip('+')
			processedGame['players'] = int(processedGame['players'])

		if 'multiplayer' in game:

			processedGame['multiplayer']['simultaneous-coop'] = str2bool(game['multiplayer']['@simultaneous-coop'])
			processedGame['multiplayer']['alternating-coop'] = str2bool(game['multiplayer']['@alternating-coop'])
			processedGame['multiplayer']['simultaneous-vs'] = str2bool(game['multiplayer']['@simultaneous-vs'])
			processedGame['multiplayer']['alternating-vs'] = str2bool(game['multiplayer']['@alternating-vs'])

		if 'compatibility' in game:

			if '@pi0' in game['compatibility']:

				processedGame['compatibility']['pi0'] = str2bool(game['compatibility']['@pi0'])

			if '@pi3' in game['compatibility']:

				processedGame['compatibility']['pi3'] = str2bool(game['compatibility']['@pi3'])

		processedGames.append(processedGame)

	return system, processedGames


def get_metadata():

	json_ = open('metadata.json', 'r').read()

	metadata = json.loads(json_)

	return metadata


def convert_metadata_to_systems(metadata):

	systems = {}

	for _system in metadata:

		system = {}

		games = {}

		for game in _system['games']:

			games[game['name']] = game

		system[_system['name']] = games

	return systems


def merge_systems_into_metadata(systems, metadata):

	for key, system in enumerate(metadata):

		if system['name'] in systems:

			games = systems[system['name']]

			metadata[key]['games'] = sorted(games.values(), key=lambda k: k['name'])

	metadata = sorted(metadata.values(), key=lambda k: k['name'])

	return metadata


def put_metadata(metadata):

	metadata = json.dumps(metadata, indent=4, sort_keys=True, separators=(',', ': '))

	open('metadata.json', 'w').write(metadata)


def update_metadata():

	metadata = get_metadata()

	systems = convert_metadata_to_systems(metadata)

	gameslists = get_gameslists('/retropie/roms/')
	# gameslists = get_gameslists('//RETROPIE/roms/')

	for system, games in gameslists.iteritems():

		if system not in systems:

			systems[system] = {}

		for game in games:

			if game['name'] not in systems[system]:

				systems[system][game['name']] = game

			for key, value in game.iteritems():

				if key not in systems[system][game['name']]:

					systems[system][game['name']][key] = value

	put_metadata(metadata)


def update_games():

	json_ = open('metadata.json', 'r').read()

	metadata = json.loads(json_)

	for system in metadata:

		for game in system['games']:

			del game['description']
			del game['image']
			del game['releaseDate']
			del game['developer']
			del game['publisher']
			del game['genre']

	metadata = json.dumps(metadata, indent=4, sort_keys=True, separators=(',', ': '))

	open('games.json', 'w').write(metadata)


update_metadata()
update_games()
