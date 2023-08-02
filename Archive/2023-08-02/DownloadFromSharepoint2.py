from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
import os

# Replace these variables with your own credentials and folder information
sharepoint_url = 'https://siseth.sharepoint.com/:f:/r/sites/ProjektEOSC'
client_id = 'p280492@sggw.edu.pl'
client_secret = ''
site_url = 'https://your_domain.sharepoint.com/sites/your_site'
folder_url = '/Shared Documents/General/Photos'
local_download_path = 'your_local_download_path'

# Authenticate with SharePoint
auth_ctx = AuthenticationContext(sharepoint_url)
auth_ctx.acquire_token_for_app(client_id, client_secret)
ctx = ClientContext(site_url, auth_ctx)

# Get folder
folder = ctx.web.get_folder_by_server_relative_url(folder_url)
ctx.load(folder)
ctx.execute_query()

# Download files
def download_files(folder, download_path):
    files = folder.files
    ctx.load(files)
    ctx.execute_query()

    for file in files:
        file_name = os.path.join(download_path, file.properties['Name'])
        with open(file_name, 'wb') as local_file:
            file.download(local_file, ctx)
            ctx.execute_query()
        print(f"Downloaded file: {file_name}")

    # Process subfolders
    folders = folder.folders
    ctx.load(folders)
    ctx.execute_query()

    for subfolder in folders:
        subfolder_path = os.path.join(download_path, subfolder.properties['Name'])
        os.makedirs(subfolder_path, exist_ok=True)
        download_files(subfolder, subfolder_path)

download_files(folder, local_download_path)
