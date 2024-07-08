# Google Drive File Manager 
This script is designed to download specific folders from Google Drive based on given folder names, and organize the downloaded content in a specified local directory. Additionally, it includes utility functions to manage and move downloaded files.

# Prerequisites
  1. Python3.x
  2. Following python libraries must be installed:
    google-auth
    google-auth-oauthlib
    google-auth-httplib2
    google-api-python-client

# Setup
  1. Obtain Google API credentials as `credentials.json` from the Google Cloud Console and place it in the same directory as the script.
  2. OAuth2.0 authentication is used. The first time the script is run, a prompt to authorize access to Google drive is created. This will create       a token.json file for subsequent access without re-authentication.

# Configuration
  1. The "https://www.googleapis.com/auth/drive" scope is required for accessing the Google drive.
  2. Modify the courseTitles list to include the titles of the folders you want to download from Google Drive.
  3. Set the root directory to where the downloaded content needs to be stored.

# Usage
  1. Run the script using:
      python3 assistant.py
  2. The script will authenticate using the Google OAuth2.0 flow and search for the specified folders in Google Drive.
  3. The found folders and their contents will be downloaded to the specified root directory.
  4. If any file downloads fail, their IDs will be printed at the end of the script's execution.

# Failed Downloads
  If any files fail to download, their IDs will be stored in the failedDownloadID list. Download of these files may be reattempted as needed.
