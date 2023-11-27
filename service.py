from urllib.parse import urlencode

def get vk_token():
    APP_ID = '51795204'
    OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': APP_ID,
        'display': 'page',
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'scope': 'status,photos',
        'response_type': 'token'
    }
    oauth_url = f'{OAUTH_BASE_URL}?{urlencode(params)}'
    print(oauth_url)

def get_interesting_users():
    for i in range(1000):
        try:
            VKclient = VKAPIClient(access_token, i)
            albums = VKclient.get_albums()
            if len(albums)> 0:
                f = open('result_scanning.txt', 'a')
                f.write(', '.join(str(x) for x in albums) + '\n')
                f.write(str(i) + '\n')
                f.close()
        except Exception as ex:
            pass