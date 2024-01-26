import requests

api_key = 'PMAK-65a4143e8571590038515335-933806faa8182ee6f8cefd97cb41c909b2'
workspace_id = '0fb6b30e-2dc3-430b-836d-1f2fc9d4af07'

headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}

url = f'https://api.getpostman.com/collections'
response = requests.get(url, headers=headers)

def update_environment():
    environment_id="32112141-e5d02767-f0f1-4d77-aede-144460f42114"
    url_get_environment = f'https://api.getpostman.com/environments/{environment_id}'
    response_get_environment = requests.get(url_get_environment, headers=headers)
    envr= response_get_environment.json()
    check=response_get_environment.json()["environment"]["values"][-1]
    check['value']='test'
    envr["environment"]["values"][-1]=check
    #print(envr)
    url_update_environment = f'https://api.getpostman.com/environments/{environment_id}'
    response_update_environment = requests.put(url_update_environment, headers=headers,json=envr)
    #print(check)
    #.update({'value':'new'})
    
def call_song_request():
    collection_id = "32112141-e5e4c6a5-9932-47c9-8a2f-5885a0da611c"
    request_id = "32112141-b9b45e5a-2f72-4e4a-8148-f455f6aea262"
    url_get_request = f"https://api.getpostman.com/collections/{{collection_id}}/requests/{{request_id}}"
    response_get_song_request = requests.get(url_get_request, headers=headers)

# print(response.json())
call_song_request()
# if response.status_code == 200:
#     collections = response.json().get('collections', [])
#     for collection in collections:
#         print(collection['name'])
# else:
#     print(f"Error: {response.status_code}, {response.text}")