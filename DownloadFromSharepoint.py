import os
import sharepy
import requests
from io import BytesIO

def save_file(file_url, local_folder):
    response = s.get(file_url, stream=True)
    with BytesIO(response.content) as b:
        with open(os.path.join(local_folder, file_url.split('/')[-1]), 'wb') as f:
            f.write(b.read())
def download_sharepoint_folder(site_url, folder_url, username, password, local_folder):
    s = sharepy.connect(site_url, username, password)

    # Ensure local folder exists
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    # Get folder contents
    response = s.get(f"{site_url}/_api/web/GetFolderByServerRelativeUrl('{folder_url}')/Files")
    files = response.json()['value']

    # Download files
    for file in files:
        file_url = file['ServerRelativeUrl']
        save_file(file_url, local_folder)


if __name__ == "__main__":
    site_url = "https://siseth.sharepoint.com/:f:/r/sites/ProjektEOSC"  # Replace with your SharePoint site URL
    #site_url = "https://siseth.sharepoint.com"  # Replace with your SharePoint site URL
    folder_url = "/Shared%20Documents/General/Photos"  # Replace with the server relative URL of the folder
    username = "p280492@sggw.edu.pl"  # Replace with your username
    password = ""  # Replace with your password
    local_folder = "downloads"

#https://siseth.sharepoint.com/:f:/r/sites/ProjektEOSC/Shared%20Documents/General/Photos?csf=1&web=1&e=sAdNCq

    download_sharepoint_folder(site_url, folder_url, username, password, local_folder)