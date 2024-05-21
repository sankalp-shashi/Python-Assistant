import os
import google.auth
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload





# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
courseTitles = ["'CS303'","'HS104'","'GE111'","'HS202'"]
creds = None
folderType = "application/vnd.google-apps.folder"
root = "/home/sankalp/Desktop/SM/courses/"
failedDownloadID = []


def download_file(real_file_id, real_file_name, address):
  """Downloads a file
  Args:
      real_file_id: ID of the file to download

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)

    file_id = real_file_id

    # pylint: disable=maybe-no-member
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
#      print(f"Downloading {real_file_name}: {int(status.progress() * 100)}%...")
    file.seek(0);
	
    with open(os.path.join(address,real_file_name), "wb") as localFile:
  	  localFile.write(file.read())
    localFile.close()
    print(f"Downloaded {real_file_name} successfully.")
  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None
    print(f"Failed to download the file {real_file_name}.")
    print("Proceeding to next file...")
    failedDownloadID.append({real_file_id,real_file_name})
  return




def copy_folder(folderId, folderName, address):
	files = []
	subfolders = []
	address = os.path.join(address, folderName)
	if not os.path.exists(address):
		print(f"\nCreating the folder {folderName} on your device...")
		os.makedirs(address)

	print("Attempting to connect to google drive API client...")
	service = build("drive", "v3", credentials=creds)
	print("Connection successful.")

	print(f"Querying API client for files and folders in {folderName}...")
	response = service.files().list(
		q = "'" + folderId + "' in parents",
		pageSize = 10,
		fields = "nextPageToken, files(id,name,mimeType)"
	).execute()
	print()
	print("Recieved response from API client.")
	items = response.get('files',[])
	for item in items:
		itemType = item.get('mimeType')
		if (itemType == folderType):
			subfolders.append(item)
		else:
			files.append(item)
	for file in files:
		print(f"Downloading {file.get('name')}...")
		download_file(file.get('id'), file.get('name'), address)		
	while subfolders:
		copy_folder(subfolders[-1].get('id'), subfolders[-1].get('name'), address)
		subfolders.pop()
	return
  	



def get_folders(title):
  """Search file in drive location

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    folders = []
    page_token = None
    while True:
      # pylint: disable=maybe-no-member
      response = (
          service.files()
          .list
          (
	            q = "mimeType = '" + folderType + "' and fullText contains " + title,
              spaces="drive",
              fields="nextPageToken, files(id, name)",
              pageToken=page_token,
          )
          .execute()
      )
#      for file in response.get("files", []):
        # Process change
#        print(f'Found file: {file.get("name")}, {file.get("id")}')
      folders.extend(response.get("files", []))
      page_token = response.get("nextPageToken", None)
      if page_token is None:
        break
  except HttpError as error:
    print(f"An error occurred: {error}")
    folders = None
  return folders


def get_credentials():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds



if __name__ == "__main__":
	creds = get_credentials()
	title = courseTitles[0]
	folders = []
	for title in courseTitles:
		folders.extend(get_folders(title))
	for folder in folders:
		copy_folder(folder.get('id'), folder.get('name'), root)
	print("Failed to download files with the following IDs:\n")
	if failedDownloadID.size() > 0:
		for ID in failedDownloadID:
			print(ID)
