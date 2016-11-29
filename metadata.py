import os
import json
import xmltodict


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

	processed_games = []

	xml_ = open(file, 'r').read()

	dict_ = xmltodict.parse(xml_)

	gamelist = dict_['gameList']

	if gamelist is None:

		gamelist = {}

	if '@system' in gamelist:

		system = gamelist['@system']

	if 'game' in gamelist:

		games = gamelist['game']

	if isinstance(games, list) is False:

		games = [games]

	for game in games:

		processed_game = {
			'id': None,
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

		if 'id' in game:

			processed_game['id'] = int(game['id'])

		if 'licensed' in game:

			processed_game['licensed'] = str2bool(game['licensed'])

		if 'releasedate' in game:

			processed_game['releaseDate'] = game['releasedate']

		if 'developer' in game:

			processed_game['developer'] = game['developer']

		if 'publisher' in game:

			processed_game['publisher'] = game['publisher']

		if 'genre' in game:

			processed_game['genre'] = game['genre']

		if 'players' in game and game['players'] is not None:

			processed_game['players'] = game['players'].strip('+')
			processed_game['players'] = int(processed_game['players'])

		if 'multiplayer' in game:

			processed_game['multiplayer']['simultaneous-coop'] = str2bool(game['multiplayer']['@simultaneous-coop'])
			processed_game['multiplayer']['alternating-coop'] = str2bool(game['multiplayer']['@alternating-coop'])
			processed_game['multiplayer']['simultaneous-vs'] = str2bool(game['multiplayer']['@simultaneous-vs'])
			processed_game['multiplayer']['alternating-vs'] = str2bool(game['multiplayer']['@alternating-vs'])

		if 'compatibility' in game:

			if '@pi0' in game['compatibility']:

				processed_game['compatibility']['pi0'] = str2bool(game['compatibility']['@pi0'])

			if '@pi3' in game['compatibility']:

				processed_game['compatibility']['pi3'] = str2bool(game['compatibility']['@pi3'])

		processed_games.append(processed_game)

	return system, processed_games


def convert_metadata_to_systems(metadata):

	systems = {}

	for _system in metadata:

		system = {}

		games = {}

		for game in _system['games']:

			games[game['name']] = game

		systems[_system['name']] = games

	return systems


def merge_systems_into_metadata(systems, metadata):

	for key, system in enumerate(metadata):

		if system['name'] in systems:

			games = systems[system['name']]

			metadata[key]['games'] = sorted(games.values(), key=lambda k: k['name'])

	metadata = sorted(metadata, key=lambda k: k['name'])

	return metadata


def put_metadata(metadata):

	metadata = json.dumps(metadata, indent=4, sort_keys=True, separators=(',', ': '))

	open('metadata.json', 'w').write(metadata)


def put_metadata_partial(metadata):

	for system in metadata:

		for game in system['games']:

			del game['id']
			del game['description']
			del game['image']
			del game['releaseDate']
			del game['developer']
			del game['publisher']
			del game['genre']

	metadata = json.dumps(metadata, indent=4, sort_keys=True, separators=(',', ': '))

	open('partial-metadata.json', 'w').write(metadata)


def update_metadata():

	json_ = open('metadata.json', 'r').read()

	metadata = json.loads(json_)

	systems = convert_metadata_to_systems(metadata)

	gameslists = get_gameslists('/retropie/roms/')
	# gameslists = get_gameslists('//RETROPIE/roms/')

	for system, games in gameslists.iteritems():

		if system not in systems:

			systems[system] = {}

		for game in games:

			if game['name'] not in systems[system]:

				# print game['name']

				systems[system][game['name']] = game

			for key, value in game.iteritems():

				if key not in systems[system][game['name']]:

					systems[system][game['name']][key] = value

	merge_systems_into_metadata(systems, metadata)

	put_metadata(metadata)
	put_metadata_partial(metadata)


update_metadata()
