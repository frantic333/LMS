import requests


data = {
    "email": "test_frame@example.com",
    "birthday": "2023-11-10",
    "description": "a",
    #"avatar": "/home/max/Загрузки/ava.png",
    "name": "Анна Павлова",
    "password": "password012201"
}

auth_data = dict(
    username='test@gmail.com',
    password='1'
)
import base64
from requests.auth import HTTPBasicAuth
#userpass = "{0}:{1}".format(auth_data['username'], auth_data['password'])
#userpass_encoded = base64.b64encode(userpass.encode()).decode()
#print(userpass_encoded)
#response = requests.get(url='http://127.0.0.1:8000/api/courses/', headers={
#    'Authorization': "Token f2dd1ecf9c4c49f6bc727761b7e277a6cb51ecbd"
#})
response = requests.post(url='http://127.0.0.1:8000/api/generate-token/', data=auth_data)
print(response.text, response.status_code)