import requests
from tqdm import tqdm
import json
import tokens

# from urllib.parse import urlencode
#
access_token = tokens.access_token
YA_TOKEN = tokens.YA_TOKEN
user_id = '17'
#
# APP_ID = '51795204'
# OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
# params = {
#     'client_id': APP_ID,
#     'display': 'page',
#     'redirect_uri': 'https://oauth.vk.com/blank.html',
#     'scope': 'status,photos',
#     'response_type': 'token'
# }
# oauth_url = f'{OAUTH_BASE_URL}?{urlencode(params)}'
# print(oauth_url)


class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, access_token, user_id):
        self.token = access_token
        self.user_id = user_id

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.154'
        }

    def _build_url(self, method):
        return f'{self.API_BASE_URL}/{method}'

    # def get_status(self):
    #     params = self.get_common_params()
    #     params.update({'user_id': self.user_id})
    #     response = requests.get(self._build_url('status.get'), params=params)
    #     return response.json().get('response').get('text')

    # def set_status(self, new_status):
    #     params = self.get_common_params()
    #     params.update({'user_id': self.user_id, 'text': new_status})
    #     response = requests.get(self._build_url('status.set'), params=params)
    #     response.raise_for_status()

    # def replace_status(self, target, replace_string):
    #     status = self.get_status()
    #     new_status = status.replace(target, replace_string)
    #     self.set_status(new_status)

    def user_photos(self, album: object) -> object:
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': album, 'extended': 1, 'count': '1000'})
        response = requests.get(self._build_url('photos.get'), params=params)
        return response.json()

    def get_albums(self):
        try:
            output = []
            params = self.get_common_params()
            params.update({'owner_id': self.user_id})
            response = requests.get(self._build_url('photos.getAlbums'), params=params)
            for i in response.json()['response']['items']:
                output.append(i['id'])
            return output

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


class YaDiscAPIClient:
    YA_API_BASE_URL = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.token = token

    def _build_url(self, method):
        return f'{self.YA_API_BASE_URL}/{method}'

    def get_common_headers(self):
        return {
            'Authorization': self.token,
        }

    def upload_file(self, file_path, file_name, file_url):
        params = {'path': file_path + '/' + file_name, 'url': file_url}
        headers = self.get_common_headers()
        response = requests.post(self._build_url('v1/disk/resources/upload'), headers=headers, params=params)
        return response.json()

    def make_folder(self, folder_path):
        params = {'path': '/' + folder_path}
        headers = self.get_common_headers()
        response = requests.put(self._build_url('v1/disk/resources'), headers=headers, params=params)
        return response.json()


def backup_photos_from_vk(number_ph: int):
    print("Finding photos…")
    vk_client = VKAPIClient(access_token, user_id)
    ph_urls = []
    ph_likes = []
    ph_type = []
    albums = vk_client.get_albums()
    albums.append('profile')
    print('Starting to select photos…')
    for a in albums:
        photos = vk_client.user_photos(a)
        for ph in photos['response']['items']:
            ph_urls.append(ph['sizes'][-1]['url'])
            ph_likes.append(ph['likes']['count'])
            ph_type.append(ph['sizes'][-1]['type'])
    # print(len(ph_urls))
    ph_urls_sorted = list(zip(ph_likes, ph_urls, ph_type))
    ph_urls_sorted = sorted(ph_urls_sorted, reverse=True)
    ph_urls_sorted_reduced = ph_urls_sorted[:number_ph]
    print('Photos selected')
    # print(ph_urls_sorted_reduced)
    folder_path = 'netology_exercise'
    ya_client = YaDiscAPIClient(YA_TOKEN)
    response = ya_client.make_folder(folder_path)
    print("Beginning uploading…")
    output_dict = {}
    output_list = []
    for i in tqdm(range(len(ph_urls_sorted_reduced)), desc="Uploading…", ascii=False, ncols=100):
        file_name = str(ph_urls_sorted_reduced[i][0]).zfill(00000000) + '.jpg'
        url = ph_urls_sorted_reduced[i][1]
        response = ya_client.upload_file(folder_path, file_name, url)
        output_dict['file_name'] = file_name
        output_dict['size'] = ph_urls_sorted_reduced[i][2]
        output_list.append(output_dict)
    with open("output_data.json", "w") as f:
        json.dump(output_list, f)
    print("Backup complete")


if __name__ == '__main__':
    backup_photos_from_vk(20)


    # # VKclient = VKAPIClient(access_token, user_id)
    # # print(VKclient.get_albums())

    # for i in range(1000):
    #     try:
    #         VKclient = VKAPIClient(access_token, i)
    #         albums = VKclient.get_albums()
    #         if len(albums)> 0:
    #             f = open('result_scanning.txt', 'a')
    #             f.write(', '.join(str(x) for x in albums) + '\n')
    #             f.write(str(i) + '\n')
    #             f.close()
    #     except Exception as ex:
    #         pass