# python -m SimpleHTTPServer 8080

import os
import xmltodict
import json
import collections


def str2bool(string):
	return string.lower() in ('true')


def get_system_folders(folder):

	system_folders = []

	for dirpath, dirnames, filenames in os.walk(folder):

		for filename in [file for file in filenames if file == 'gamelist.xml']:

			system_folders.append(dirpath + '/')

	return system_folders


def get_games(file):

	games = []

	processedGames = []

	xml_ = open(file, 'r').read()

	dict_ = xmltodict.parse(xml_)

	gameList = dict_['gameList']

	if gameList is None:

		gameList = {}

	if 'game' in gameList:

		games = gameList['game']

	if isinstance(games, list) is False:

		games = [games]

	for game in games:

		processedGame = {
			'name': game['name'],
			'description': game['desc'],
			'image': game['image'],
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

	return processedGames


def get_metadata(file):

	json_ = open(file, 'r').read()

	metadata = json.loads(json_)

	system = metadata.keys()[0]

	games2 = metadata.values()[0]

	games = {}

	for game in games2:

		games[game['name']] = game

	metadata['system'] = system

	metadata['games'] = games

	return metadata


def put_metadata(file, metadata):

	metadata = {metadata['system']: metadata['games'].values()}

	metadata = json.dumps(metadata, indent=4, sort_keys=True)

	open(file, 'w').write(metadata)


def update_metadata(system_folders):

	for system_folder in system_folders:

		games_file = system_folder + 'gamelist.xml'

		metadata_file = system_folder + 'games.json'

		games = get_games(games_file)

		metadata = get_metadata(metadata_file)

		for game in games:

			if game['name'] not in metadata['games']:

				metadata['games'][game['name']] = game

		put_metadata(metadata_file, metadata)


def combine_metadata(system_folders):

	collection = {}

	for system_folder in system_folders:

		metadata_file = system_folder + 'games.json'

		metadata = get_metadata(metadata_file)

		system = metadata['system']

		games = metadata['games'].values()

		if system in collection and collection[system] != games:

			collection[system] = collection[system] + games

		else:

			collection[system] = games

	collection = collections.OrderedDict(sorted(collection.items()))

	collection = json.dumps(collection, indent=4, sort_keys=True)

	open('games.json', 'w').write(collection)


system_folders = get_system_folders('/retropie/roms/')
# system_folders = get_system_folders('//RETROPIE/roms/')

update_metadata(system_folders)
combine_metadata(system_folders)
