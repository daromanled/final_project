import json
import time
import requests
from urllib.parse import urlencode, urlparse

user_id = '406304856'
token_url = 'https://oauth.vk.com/blank.html#access_token=3a70759fbf68a82f62b08fc2d01fd4f0937e81c6d0e6ad43673ca830c00b27a9ba02050360b212ed01380&expires_in=86400&user_id=406304856'
o = urlparse(token_url)
fragments = dict((i.split('=') for i in o.fragment.split('&')))
access_token = fragments['access_token']

params = {'access_token': access_token,
          'v': VERSION,
        }

def get_groups(user_id):
    if user_id:
        params['user_id'] = user_id
    time.sleep(0.5)
    r = requests.get('https://api.vk.com/method/groups.get', params)
    print('*')
    return r.json()

def get_info(group_id):
    if group_id:
        params['group_id'] = group_id
    time.sleep(0.5)
    r = requests.get('https://api.vk.com/method/groups.getById', params)
    print('*')
    return r.json()

def get_friends(user_id):
    if user_id:
        params['user_id'] = user_id
    time.sleep(0.5)
    r = requests.get('https://api.vk.com/method/friends.get', params)
    print('*')
    return r.json()

def write_to_file(group):
    with open('groups.json', 'w') as file:
        json.dump(group, file)

list_of_groups = get_groups(user_id)
my_groups = set(list_of_groups['response']['items'])
friends = get_friends(user_id)
groups_of_friends = []

for id in friends['response']['items']:
    my_groups = my_groups.difference(set(get_groups(id)['response']['items']))
 
result = []
for i in my_groups:
    result.append(get_info(i))
write_to_file(result)
