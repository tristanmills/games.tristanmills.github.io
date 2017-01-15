import os
import json
import xmltodict
import datetime
import urllib
import requests


class Utilities(object):

	def __init__(self):
		self.roms_path = '/retropie/roms/'
		self.metadata_path = '../data/metadata.json'
		self.partial_metadata_path = '../data/partial-metadata.json'

	def str2bool(self, string):
		return string.lower() in ('true')

	def get_gameslists(self, folder):

		gameslists = {}

		for dirpath, dirnames, filenames in os.walk(folder):

			for filename in [file for file in filenames if file == 'gamelist.xml']:

				path = os.path.join(dirpath, filename).replace('\\', '/')

				system_name, games = self.parse_gameslist(path)

				gameslists[system_name] = games

		return gameslists

	def parse_gameslist(self, file):

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
				# 'image': game['image'],
				'released': None,
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

			if 'released' in game:

				processed_game['released'] = self.str2bool(game['released'])

			if 'releasedate' in game:

				processed_game['releaseDate'] = datetime.datetime.strptime(game['releasedate'], '%Y%m%dT000000').strftime('%Y-%m-%d')

			if 'developer' in game:

				processed_game['developer'] = game['developer']

			if 'publisher' in game:

				processed_game['publisher'] = game['publisher']

			if 'genre' in game:

				processed_game['genre'] = game['genre']

			if 'players' in game and game['players'] is not None:

				processed_game['players'] = int(game['players'].strip('+'))

			if 'multiplayer' in game:

				processed_game['multiplayer']['simultaneous-coop'] = self.str2bool(game['multiplayer']['@simultaneous-coop'])
				processed_game['multiplayer']['alternating-coop'] = self.str2bool(game['multiplayer']['@alternating-coop'])
				processed_game['multiplayer']['simultaneous-vs'] = self.str2bool(game['multiplayer']['@simultaneous-vs'])
				processed_game['multiplayer']['alternating-vs'] = self.str2bool(game['multiplayer']['@alternating-vs'])

			if 'compatibility' in game:

				if '@pi0' in game['compatibility']:

					processed_game['compatibility']['pi0'] = self.str2bool(game['compatibility']['@pi0'])

				if '@pi3' in game['compatibility']:

					processed_game['compatibility']['pi3'] = self.str2bool(game['compatibility']['@pi3'])

			processed_games.append(processed_game)

		return system, processed_games

	def convert_metadata_to_systems(self, metadata):

		systems = {}

		for _system in metadata:

			system = {}

			games = {}

			for game in _system['games']:

				games[game['name']] = game

			systems[_system['name']] = games

		return systems

	def merge_systems_into_metadata(self, systems, metadata):

		for key, system in enumerate(metadata):

			if system['name'] in systems:

				games = systems[system['name']]

				released = 0

				for game in games.values():

					if game['released']:

						released += 1

				if metadata[key]['released'] == 'Unknown':

					metadata[key]['collection'] = 'Unknown'

				else:

					collection = 100 * float(released) / float(metadata[key]['released'])

					metadata[key]['collection'] = format(collection, '.2f') + '%'

				metadata[key]['games'] = sorted(games.values(), key=lambda k: k['name'])

		metadata = sorted(metadata, key=lambda k: k['name'])

		return metadata

	def get_metadata(self):

		json_ = open(self.metadata_path, 'r').read()

		metadata = json.loads(json_)

		return metadata

	def put_metadata(self, metadata):

		metadata = json.dumps(metadata, indent=4, sort_keys=True, separators=(',', ': '))

		open(self.metadata_path, 'w').write(metadata)

	def put_partial_metadata(self, metadata):

		for system in metadata:

			for game in system['games']:

				del game['id']
				del game['description']
				# del game['image']
				del game['releaseDate']
				del game['developer']
				del game['publisher']
				del game['genre']

		metadata = json.dumps(metadata, indent=4, sort_keys=True, separators=(',', ': '))

		open(self.partial_metadata_path, 'w').write(metadata)

	def update_metadata(self):

		metadata = self.get_metadata()

		systems = self.convert_metadata_to_systems(metadata)

		gameslists = self.get_gameslists(self.roms_path)

		for system, games in gameslists.iteritems():

			if system not in systems:

				systems[system] = {}

			for game in games:

				if game['name'] not in systems[system]:

					systems[system][game['name']] = game

				for key, value in game.iteritems():

					if key not in systems[system][game['name']]:

						systems[system][game['name']][key] = value

		self.merge_systems_into_metadata(systems, metadata)

		self.put_metadata(metadata)
		self.put_partial_metadata(metadata)

	def update_ids(self):

		metadata = self.get_metadata()

		for system_index, system in enumerate(metadata):

			base_url = 'http://thegamesdb.net/api/GetGame.php?platform=' + urllib.quote(system['name'].encode('utf8')) + '&exactname='

			for game_index, game in enumerate(system['games']):

				if game['id'] is None:

					url = base_url + urllib.quote(game['name'].encode('utf8'))

					response = requests.get(url)

					if response.status_code == 200:

						data = xmltodict.parse(response.text)['Data']

						if 'Game' in data:

							metadata[system_index]['games'][game_index]['id'] = data['Game']['id']

					else:

						print system['name'] + ' - ' + game['name'] + ' - Failed'

		self.put_metadata(metadata)

	def parse_api_metadata(self, metadata):

		game = {
			'name': metadata['Game']['GameTitle'],
			'description': metadata['Game']['Overview'],
			'releaseDate': None,
			'developer': None,
			'publisher': None,
			'genre': [],
			'players': None,
		}

		if 'ReleaseDate' in metadata['Game']:

			pass
			# game['releaseDate'] = datetime.datetime.strptime(metadata['Game']['ReleaseDate'], '%m/%d/%Y').strftime('%Y-%m-%d')

		if 'Developer' in metadata['Game']:

			game['developer'] = metadata['Game']['Developer']

		if 'Publisher' in metadata['Game']:

			game['publisher'] = metadata['Game']['Publisher']

		if 'Genres' in metadata['Game']:

			game['genre'] = metadata['Game']['Genres']['genre']

		if 'Players' in metadata['Game']:

			game['players'] = int(metadata['Game']['Players'].strip('+'))

		return game

	def validate_metadata(self):

		metadata = self.get_metadata()

		for system_index, system in enumerate(metadata):

			base_url = 'http://thegamesdb.net/api/GetGame.php?id='

			for game_index, game in enumerate(system['games']):

				if game['id'] is not None:

					url = base_url + str(game['id'])

					response = requests.get(url)

					if response.status_code == 200:

						api_metadata = xmltodict.parse(response.text)['Data']

						if 'Game' in api_metadata:

							api_metadata = self.parse_api_metadata(api_metadata)

							if game['releaseDate'] != api_metadata['releaseDate']:

								pass
								# print system['name'] + ' - ' + game['name'] + ' - Wrong releaseDate'

							if game['developer'] != api_metadata['developer']:

								print system['name'] + ' - ' + game['name'] + ' - Wrong developer'

							if game['publisher'] != api_metadata['publisher']:

								print system['name'] + ' - ' + game['name'] + ' - Wrong publisher'

							if game['players'] != api_metadata['players']:

								print system['name'] + ' - ' + game['name'] + ' - Wrong players'

							if game['genre'] not in api_metadata['genre']:

								print system['name'] + ' - ' + game['name'] + ' - Wrong genre'

						else:

							print system['name'] + ' - ' + game['name'] + ' - Wrong Name'

					else:

						print system['name'] + ' - ' + game['name'] + ' - Failed'

				else:

						print system['name'] + ' - ' + game['name'] + ' - Missing ID'
