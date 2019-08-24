def calc_age(uid):
    import requests

    access_token = '994f2b77994f2b77994f2b77549923276b9994f994f2b77c40a58f91fc51ab0518224f8'

    users_params = dict(user_ids=uid,
                        fields='bdate',
                        access_token=access_token,
                        v='5.71')

    vk_user = requests.get('https://api.vk.com/method/users.get', params=users_params)

    friends_params = dict(user_id=vk_user.json()['response'][0]['id'],
                          fields='bdate',
                          access_token=access_token,
                          v='5.71')

    vk_user_freinds = requests.get('https://api.vk.com/method/friends.get', params=friends_params)

    import re
    from datetime import datetime
    import numpy as np

    now = datetime.now()
    friends_birth_years = []
    for friend in vk_user_freinds.json()['response']['items']:
        if 'bdate' in friend and re.match(r"[0-9]+.[0-9]+.[0-9]+", friend['bdate']):
            byear = int(friend['bdate'].split(sep='.')[2])
            friends_birth_years.append(now.year - byear)

    years, count = np.unique(np.array(friends_birth_years),
                             return_counts=True)

    years_count = list(zip(years, count))
    years_count.sort(key=lambda x: x[1], reverse=True)

    return years_count


if __name__ == '__main__':
    res = calc_age('reigning')
    # res = calc_age('id11613')
    print(res)
