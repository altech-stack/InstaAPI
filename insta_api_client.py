import requests
import json
from pymongo import MongoClient
import time
headers = {'Content-Type': 'application/json'}
api_endpoint='http://localhost:5000/api/v1.0'

def api_post(endpoint,payload=None):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('{}{}'.format(api_endpoint, endpoint), data=json.dumps(payload),headers=headers)
    return response

def api_get(endpoint, params=None):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get('{}{}'.format(api_endpoint, endpoint), params=params,headers=headers)
    return response


def test_instapi_api(user):

    response = api_get('/instapi/'+user)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None

def test_getter(j_id):
    response = api_get('/instapi/'+str(j_id))
    return response.content

def main():
    job_id = test_instapi_api(str('shannoncakes_'))
    print job_id




if __name__ == '__main__':
    main()