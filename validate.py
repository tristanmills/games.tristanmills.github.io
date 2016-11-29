import json
import xmltodict
import urllib
import requests


json_ = open('metadata.json', 'r').read()

metadata = json.loads(json_)

for system in metadata:

	base_url = 'http://thegamesdb.net/api/GetGame.php?platform=' + urllib.quote(system['name'].encode('utf8')) + '&exactname='

	for game in system['games']:

		url = base_url + urllib.quote(game['name'].encode('utf8'))

		response = requests.get(url)

		if response.status_code == 200:

			dict_ = xmltodict.parse(response.text)['Data']['Game']

			_game = {
				'name': dict_['GameTitle'],
				'description': dict_['Overview'],
				'releaseDate': None,
				'developer': None,
				'publisher': None,
				'genre': [],
				'players': None,
			}

			if 'ReleaseDate' in dict_:

				_game['releaseDate'] = dict_['ReleaseDate']

			if 'Developer' in dict_:

				_game['developer'] = dict_['Developer']

			if 'Publisher' in dict_:

				_game['publisher'] = dict_['Publisher']

			if 'Genres' in dict_:

				_game['genre'] = dict_['Genres']

			if 'Players' in dict_:

				_game['players'] = dict_['Players']

			print _game

		else:

			print system['name'] + ' - ' + game['name']
