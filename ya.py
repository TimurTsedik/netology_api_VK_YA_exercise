import requests

class YaDiscAPIClient:
    """Description: This class represents a client for interacting with the Yandex Disk API.
    It provides methods for uploading files and creating folders on Yandex Disk.
    Attributes:
    YA_API_BASE_URL: A class variable representing the base URL for Yandex Disk API methods.
    Methods:
    __init__(self, token): Initializes the YaDiscAPIClient with the provided access token.
    _build_url(self, method): Private method to construct the complete URL for a given API method.
    get_common_headers(self): Returns common headers required for Yandex Disk API requests.
    upload_file(self, file_path, file_name, file_url): Uploads a file to Yandex Disk from a specified URL.
    make_folder(self, folder_path): Creates a folder on Yandex Disk with the specified path."""
    # Base URL for Yandex Disk API.
    YA_API_BASE_URL = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        # Initialize YaDiscAPIClient with Yandex Disk token.
        self.token = token

    def _build_url(self, method):
        # Build complete URL for a Yandex Disk API method.
        return f'{self.YA_API_BASE_URL}/{method}'

    def get_common_headers(self):
        # Common headers required for Yandex Disk API requests.
        return {
            'Authorization': self.token,
        }

    def upload_file(self, file_path, file_name, file_url):
        # Upload a file to Yandex Disk.
        params = {'path': file_path + '/' + file_name, 'url': file_url}
        headers = self.get_common_headers()
        response = requests.post(self._build_url('v1/disk/resources/upload'), headers=headers, params=params)
        return response.json()

    def make_folder(self, folder_path):
        # Create a folder on Yandex Disk.
        params = {'path': '/' + folder_path}
        headers = self.get_common_headers()
        response = requests.put(self._build_url('v1/disk/resources'), headers=headers, params=params)
        return response.json()
