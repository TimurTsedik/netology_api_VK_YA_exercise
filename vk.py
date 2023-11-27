import requests

class VKAPIClient:
    """Description: This class represents a client for interacting with the VK (Vkontakte) API.
    It provides methods to retrieve user photos and albums from VK.
    Attributes:
    API_BASE_URL: A class variable representing the base URL for VK API methods.
    Methods:
    __init__(self, access_token, user_id): Initializes the VKAPIClient with the provided access token and user ID.
    get_common_params(self): Returns common parameters required for VK API requests,
    such as the access token and API version.
    _build_url(self, method): Private method to construct the complete URL for a given API method.
    user_photos(self, album): Retrieves user photos from a specified album.
    get_albums(self): Retrieves a list of album IDs for the user."""
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, access_token, user_id):
        # Initialize VKAPIClient with access token and user ID.
        self.token = access_token
        self.user_id = user_id

    def get_common_params(self):
        # Common parameters required for VK API requests.
        return {
            'access_token': self.token,
            'v': '5.154'
        }

    def _build_url(self, method):
        # Build complete URL for a VK API method.
        return f'{self.API_BASE_URL}/{method}'

    def user_photos(self, album: object) -> object:
        # Retrieve user photos from a specified album.
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': album, 'extended': 1, 'count': '1000'})
        response = requests.get(self._build_url('photos.get'), params=params)
        return response.json()

    def get_albums(self):
        # Retrieve user's photo albums.
        try:
            output = []
            params = self.get_common_params()
            params.update({'owner_id': self.user_id})
            response = requests.get(self._build_url('photos.getAlbums'), params=params)
            for i in response.json()['response']['items']:
                output.append(i['id'])
            return output

        except Exception as ex:
            # Handle exceptions, print an informative message.
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)