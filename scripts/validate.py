import json
import xmltodict
import urllib
import requests
import datetime


def put_metadata(metadata):

	metadata = json.dumps(metadata, indent=4, sort_keys=True, separators=(',', ': '))

	open('metadata2.json', 'w').write(metadata)


def parse_data(data):

	game = {
		'name': data['Game']['GameTitle'],
		'description': data['Game']['Overview'],
		'releaseDate': None,
		'developer': None,
		'publisher': None,
		'genre': [],
		'players': None,
	}

	if 'ReleaseDate' in data['Game']:

		pass
		# game['releaseDate'] = datetime.datetime.strptime(data['Game']['ReleaseDate'], '%m/%d/%Y').strftime('%Y-%m-%d')

	if 'Developer' in data['Game']:

		game['developer'] = data['Game']['Developer']

	if 'Publisher' in data['Game']:

		game['publisher'] = data['Game']['Publisher']

	if 'Genres' in data['Game']:

		game['genre'] = data['Game']['Genres']['genre']

	if 'Players' in data['Game']:

		game['players'] = int(data['Game']['Players'].strip('+'))

	return game


def validate_metadata():

	json_ = open('metadata.json', 'r').read()

	metadata = json.loads(json_)

	for system_index, system in enumerate(metadata):

		name_url = 'http://thegamesdb.net/api/GetGame.php?platform=' + urllib.quote(system['name'].encode('utf8')) + '&exactname='

		id_url = 'http://thegamesdb.net/api/GetGame.php?id='

		for game_index, game in enumerate(system['games']):

			if game['id'] is not None:

				url = id_url + game['id']

				if response.status_code == 200:

					data = xmltodict.parse(response.text)['Data']

					if 'Game' in data:

						_game = parse_data(data)

						if game['releaseDate'] != _game['releaseDate']:

							pass
							# print system['name'] + ' - ' + game['name'] + ' - Wrong releaseDate'

						if game['developer'] != _game['developer']:

							print system['name'] + ' - ' + game['name'] + ' - Wrong developer'

						if game['publisher'] != _game['publisher']:

							print system['name'] + ' - ' + game['name'] + ' - Wrong publisher'

						if game['players'] != _game['players']:

							print system['name'] + ' - ' + game['name'] + ' - Wrong players'

						if game['genre'] not in _game['genre']:

							print system['name'] + ' - ' + game['name'] + ' - Wrong genre'

					else:

						print system['name'] + ' - ' + game['name'] + ' - Wrong Name'

				else:

					print system['name'] + ' - ' + game['name'] + ' - Failed'

			else:

				url = name_url + urllib.quote(game['name'].encode('utf8'))

				response = requests.get(url)

				if response.status_code == 200:

					data = xmltodict.parse(response.text)['Data']

					if 'Game' in data:

						metadata[system_index]['games'][game_index]['id'] = data['Game']['id']

				else:

					print system['name'] + ' - ' + game['name'] + ' - Failed'

	put_metadata(metadata)


validate_metadata()
