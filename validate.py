import json
import requests

json_ = open('metadata.json', 'r').read()

metadata = json.loads(json_)

for system in metadata:

	base_url = 'http://thegamesdb.net/api/GetGame.php?platform=' + system['name'] + '&exactname='

	for game in system['games']:

		url = base_url + game['name']

		print url

		# r = requests.get(url)
