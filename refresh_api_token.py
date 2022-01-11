import json
import requests

url = 'https://id.twitch.tv/oauth2/token'
payload = {}
json_dict = {}

with open('settings.json', mode='r') as f:
    json_dict = json.load(f)
with open('settings.json', mode='w') as f:
    payload = {'client_id' : json_dict['TwitchClientId'], 'client_secret':json_dict['TwitchClinetSecret'], 'grant_type':'client_credentials'}
    data = json.loads(requests.post(url, params=payload).text)
    json_dict['TwitchAuthorization'] = "Bearer " + data['access_token']
    json.dump(json_dict, f, indent=4)
    print(data)