import json
import os
import requests
from datetime import datetime

def get_data(url,params={}):
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + os.environ['TOKEN']
    }
    return requests.get(url,params=params,headers=headers)
#end 

def get_groups():
    print('Groups')
    r = get_data("https://api.gitter.im/v1/groups")
    groups = r.json()
    for g in groups:
        print("{0} {1}".format(g['id'], g['name']))
    #end
#end

def get_rooms():
    print('Rooms')
    r = get_data("https://api.gitter.im/v1/rooms")
    rooms = r.json();
    for r in rooms:
        print("{0} {1}".format(r['id'],r['name']))
    #end
#end

def get_messages(room_id):

    before_id = None
    min_sent = None
    f = open('{0}-messages.txt'.format(room_id),'w+')
    try:
        while True:
            params = {
                'beforeId': before_id,
                'limit': 100
            }
            r = get_data('https://api.gitter.im/v1/rooms/{0}/chatMessages'.format(room_id),params=params)
            if r.status_code == 200:
                messages = r.json();
                for m in messages:
                    sent = datetime.strptime(m['sent'],'%Y-%m-%dT%H:%M:%S.%fZ')
                    if min_sent == None or sent < min_sent:
                        min_sent = sent
                        before_id = m['id']
                    #end
                    f.write(json.dumps(m,sort_keys=True) + '\n')
                #end
                print(before_id)
            else:
                print(r.reason)
                print("Run again in " + r.headers['X-RateLimit-Reset'] + "seconds")
                break
            #end
        #end
    finally:
        f.close()
    #end
#end

# get_rooms()
# ethereum research
# messages = get_messages('55fe873b0fc9f982beb13b83')
to_csv('55fe873b0fc9f982beb13b83-messages.txt')
