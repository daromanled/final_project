import json
import time
import requests
from urllib.parse import urlencode, urlparse

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.62'
APP_ID = 5960781

auth_data = {
    'v' : VERSION,
    'client_id' : APP_ID,
    'display' : 'mobile',
    'response_type' : 'token',
}
print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

user_id = '406304856'
token_url = 'https://oauth.vk.com/blank.html#access_token=f65fe16b4cf6f337ca8e8f49bb1e17d5a5427cad8f51f5d8791edca797c894527606e3b352a6e3bac79c6&expires_in=86400&user_id=406304856'
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
        if 'error' in r.json().keys():
            return {}
        return set(r.json()['response']['items'])
    return {}

def get_info(group_id):
    if group_id:
        params['group_id'] = group_id
        time.sleep(0.5)
        r = requests.get('https://api.vk.com/method/groups.getById', params)
        print('*')
        return r.json()
    return {}

def get_friends(user_id):
    if user_id:
        params['user_id'] = user_id
        time.sleep(0.5)
        r = requests.get('https://api.vk.com/method/friends.get', params)
        print('*')
        return r.json()['response']['items']
    return {}

def write_to_file(group):
    with open('groups.json', 'w') as file:
        json.dump(group, file)

list_of_groups = get_groups(user_id) 
friends = get_friends(user_id)

k = 0
for id in friends:
    print('Осталось обработать', len(friends) - k, 'друзей(-га)')
    list_of_groups = list_of_groups.difference(get_groups(id))
    k += 1
 
result = []
k = 0
for i in list_of_groups:
    print('Осталось обработать', len(list_of_groups) - k, 'группу(-ы)')
    result.append(get_info(i))
    k += 1

write_to_file(result)
#не поняла по поводу замечания "Не увидел обработки кодом состояния, когда сервер вк ответил ошибкой Too many requests per second", так как я делаю time.sleep(0.5) после каждого обращения к API
