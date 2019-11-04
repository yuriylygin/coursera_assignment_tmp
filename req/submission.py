import requests
from requests.auth import HTTPBasicAuth


if __name__ == '__main__':
    url = 'http://79.137.175.13/submissions/1/'

    try:
        response = requests.post(url, auth=HTTPBasicAuth('alladin', 'opensesame'))
    finally:
        print(response.text)
