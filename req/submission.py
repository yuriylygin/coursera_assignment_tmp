import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode


if __name__ == '__main__':
    host = 'https://datasend.webpython.graders.eldf.ru/'
    path_a = 'submissions/1/'

    response = requests.post(url=host+path_a, auth=HTTPBasicAuth(username='alladin', password='opensesame'))

    path_b = 'submissions/super/duper/secret/'
    response = requests.put(url=host+path_b, auth=HTTPBasicAuth(username='galchonok', password='ktotama'))
    print(response.json())

