def calc_age(uid):
    import requests
    from collections import Counter
    import re
    from datetime import datetime

    ACCESS_TOKEN = '994f2b77994f2b77994f2b77549923276b9994f994f2b77c40a58f91fc51ab0518224f8'

    users_params = dict(user_ids=uid,
                        fields='bdate',
                        access_token=ACCESS_TOKEN,
                        v='5.71')

    vk_user = requests.get('https://api.vk.com/method/users.get', params=users_params)

    friends_params = dict(user_id=vk_user.json()['response'][0]['id'],
                          fields='bdate',
                          access_token=ACCESS_TOKEN,
                          v='5.71')

    vk_user_freinds = requests.get('https://api.vk.com/method/friends.get', params=friends_params)

    now = datetime.now()
    friends_birth_years = []
    for friend in vk_user_freinds.json().get('response').get('items'):
        if 'bdate' in friend and re.match(r"[0-9]+.[0-9]+.[0-9]+", friend['bdate']):
            byear = int(friend.get('bdate').split(sep='.')[2])
            friends_birth_years.append(now.year - byear)

    friends_birth_years.sort()
    years_count = Counter(friends_birth_years)

    return years_count.most_common()


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)