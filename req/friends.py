def calc_age(uid):
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

    print(vk_user.json(), '\n')
    # print(vk_user.json()['response'], '\n')
    print(vk_user_freinds.json(), '\n')
    items = vk_user_freinds['response']['items']
    print(items)


if __name__ == '__main__':
    import requests
    # res = calc_age('reigning')
    res = calc_age('id11613')
    print(res)
