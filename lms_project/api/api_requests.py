import requests


data = {
    "email": "test_frame@example.com",
    "birthday": "2023-11-10",
    "description": "a",
    #"avatar": "/home/max/Загрузки/ava.png",
    "name": "Анна Павлова",
    "password": "password012201"
}

response = requests.post(url='http://127.0.0.1:8000/api/users/', data=data,
                         files={'avatar': open('/home/max/Загрузки/ava.png', 'rb')})
print(response.text, response.status_code)