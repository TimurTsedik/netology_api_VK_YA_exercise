
from tqdm import tqdm
import json
import tokens
from vk import VKAPIClient
from ya import YaDiscAPIClient

access_token = tokens.vk_access_token
YA_TOKEN = tokens.ya_token
user_id = tokens.user_id


# Define a function to backup photos from VK to Yandex Disk.
def backup_photos_from_vk(number_ph: int):
    """Description: This function performs a backup of photos from a VKontakte (VK)
    account and uploads them to a Yandex Disk folder. It uses the VKAPIClient and YaDiscAPIClient classes.
    Parameters:
    number_ph: The number of photos to be backed up."""
    # Print a message indicating the start of the process.
    print("Finding photos…")
    ph_urls = []
    ph_likes = []
    ph_type = []
    # Initialize lists to store photo URLs, likes, and types.
    vk_client = VKAPIClient(access_token, user_id)
    # Retrieve user's photo albums from VK.
    albums = vk_client.get_albums()
    albums.append('profile')
    # Print a message indicating the start of photo selection.
    print('Starting to select photos…')
    # Loop through each album and retrieve photos.
    for a in albums:
        photos = vk_client.user_photos(a)
        for ph in photos['response']['items']:
            # Extract and store photo details.
            ph_urls.append(ph['sizes'][-1]['url'])
            ph_likes.append(ph['likes']['count'])
            ph_type.append(ph['sizes'][-1]['type'])
    # Combine and sort photos based on likes.
    ph_urls_sorted = list(zip(ph_likes, ph_urls, ph_type))
    ph_urls_sorted = sorted(ph_urls_sorted, reverse=True)
    # Limit the number of photos to be backed up.
    ph_urls_sorted_reduced = ph_urls_sorted[:number_ph]
    # Print a message indicating the completion of photo selection.
    print('Photos selected')
    # Initialize Yandex Disk API client with the specified token.
    folder_path = 'netology_exercise'
    ya_client = YaDiscAPIClient(YA_TOKEN)
    # Create a folder on Yandex Disk for backup.
    response = ya_client.make_folder(folder_path)
    print("Beginning uploading…")
    # Initialize dictionaries and lists to store output data.
    output_dict = {}
    output_list = []
    # Iterate through selected photos and upload them to Yandex Disk.
    for i in tqdm(range(len(ph_urls_sorted_reduced)), desc="Uploading…", ascii=False, ncols=100):
        file_name = str(ph_urls_sorted_reduced[i][0]).zfill(00000000) + '.jpg'
        url = ph_urls_sorted_reduced[i][1]
        # Upload photo to Yandex Disk and store details in output dictionary.
        response = ya_client.upload_file(folder_path, file_name, url)
        output_dict['file_name'] = file_name
        output_dict['size'] = ph_urls_sorted_reduced[i][2]
        output_list.append(output_dict)
    # Write the output data to a JSON file.
    with open("output_data.json", "w") as f:
        json.dump(output_list, f)
    # Print a message indicating the completion of the backup process.
    print("Backup complete")


if __name__ == '__main__':
    backup_photos_from_vk(20)


