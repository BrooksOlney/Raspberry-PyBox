"""
Regularly backs up files from Dropbox
Project Members: Brooks Olney, Chris Salgado, Carlos Perez, Patrick Cook
"""

import sys

import dropbox
import time
import datetime

from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import os
from os import listdir
from os.path import isfile, join

# authorization token, generated from development page of Dropbox
TOKEN = 'S-aVck8tNgAAAAAAAAAAIInlY4_XleRSGvTFV95_fglkcLh51JOHGg66tq_bV-3z'

# backup path and log file that will be created/modified inside of it
BACKUPPATH = '/home/brooks/backup/'
if(os.path.exists(BACKUPPATH + 'log.txt')):
    LOG = open(BACKUPPATH + 'log.txt', 'w')
else:
    LOG = open(BACKUPPATH + 'log.txt', 'aw')

#get file names in dropbox root
def get_files_and_folders(dbx):
    allFiles = dict()
    otherDirectories = []
    client = dropbox.client.DropboxClient(TOKEN)
    metadata = client.metadata('/')
    files = [content['path'].split('/')[-1] for content in metadata['contents']]
    for x in files:
        if x.find('.') > -1:
            metadata = dbx.files_get_metadata('/' + x).content_hash
            allFiles[x] = metadata
        else:
            otherDirectories.append(x)


    compare_to_local(dbx, allFiles)

# compare dropbox files to files in backup location, note differences
def compare_to_local(dbx, files):
    localFiles = dict()
    downloadThese = []
    uploadThese = []

    temp = [f for f in listdir(BACKUPPATH) if isfile(join(BACKUPPATH, f))]
    for path in temp:
        file_mod_time = os.stat(BACKUPPATH + path).st_mtime
        localFiles[path] = file_mod_time;

    for x, y in files.items():
        downloadThese.append(x)

    for x, y in localFiles.items():
        inDropbox = 0
        for w, z in files.items():
            if(w == x):
                inDropbox = 1
        if(inDropbox == 0):
            uploadThese.append(x)


    updateDirectories(dbx, downloadThese, uploadThese)

# upload files from local backup, download files from dropbox
def updateDirectories(dbx, downloadThese, uploadThese):
    dropBoxPath = ""

    for path in downloadThese:
        dbx.files_download_to_file(BACKUPPATH + path, '/' + path)
        LOG.write(path + ' has been downloaded to ' + BACKUPPATH +  ' at ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n\n')

    for path in uploadThese:
        if(path != "log.txt"):
            dbx.files_upload(BACKUPPATH + path, '/' + path, mode=WriteMode('add'))
        LOG.write(path + ' has been uploaded to Dropbox/ at ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n\n')


if __name__ == '__main__':
    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. "
            "Open up backup-and-restore-example.py in a text editor and "
            "paste in your token in line 14.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Initiating connection with Dropbox...")
    dbx = dropbox.Dropbox(TOKEN)

    get_files_and_folders(dbx)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
            "access token from the app console on the web.")
    print("Syncing has finished, consult the log for details.")
    LOG.close()
