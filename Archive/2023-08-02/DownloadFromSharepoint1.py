import os
import requests
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version

# Replace with your credentials and target folder details
sharepoint_username = "p280492@sggw.edu.pl"
sharepoint_password = ""
sharepoint_site_url = "https://siseth.sharepoint.com/:f:/r/sites/ProjektEOSC"
sharepoint_folder_path = "/Shared Documents/General/Photos"
download_directory = "local_download_directory"

# Authenticate
authcookie = Office365(sharepoint_site_url, username=sharepoint_username, password=sharepoint_password).GetCookies()
site = Site(sharepoint_site_url, version=Version.v2016, authcookie=authcookie)
folder = site.Folder(sharepoint_folder_path)

# Get folder contents
folder_files = folder.get_items()

# Download files
for file in folder_files:
    file_name = file['Name']
    file_url = folder.url + "/" + file_name
    download_path = os.path.join(download_directory, file_name)

    print(f"Downloading {file_name}...")
    response = requests.get(file_url, cookies=authcookie, allow_redirects=True)

    with open(download_path, "wb") as f:
        f.write(response.content)

print("All files downloaded successfully.")
