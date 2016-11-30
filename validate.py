import json
import xmltodict
import urllib
import requests
import datetime


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

		game['releaseDate'] = processed_game['releaseDate'] = datetime.datetime.strptime(data['Game']['ReleaseDate'], '%m/%d/%Y').strftime('%Y-%m-%d')

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

	for system in metadata:

		base_url = 'http://thegamesdb.net/api/GetGame.php?platform=' + urllib.quote(system['name'].encode('utf8')) + '&exactname='

		for game in system['games']:

			url = base_url + urllib.quote(game['name'].encode('utf8'))

			response = requests.get(url)

			if response.status_code == 200:

				data = xmltodict.parse(response.text)['Data']

				if 'Game' in data:

					_game = parse_data(data)

					if game['releaseDate'] != _game['releaseDate']:

						print system['name'] + ' - ' + game['name'] + ' - Wrong releaseDate\n'

					if game['developer'] != _game['developer']:

						print system['name'] + ' - ' + game['name'] + ' - Wrong developer\n'

					if game['publisher'] != _game['publisher']:

						print system['name'] + ' - ' + game['name'] + ' - Wrong publisher\n'

					if game['players'] != _game['players']:

						print system['name'] + ' - ' + game['name'] + ' - Wrong players\n'

					if game['genre'] not in _game['genre']:

						print system['name'] + ' - ' + game['name'] + ' - Wrong genre\n'

				else:

					print system['name'] + ' - ' + game['name'] + ' - Wrong Name\n'

			else:

				print system['name'] + ' - ' + game['name'] + ' - Failed\n'


validate_metadata()
