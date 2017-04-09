"""
Regularly backs up files from Dropbox
Project Members:
    - Brooks Olney
    - Chris Salgado
    - Carlos Perez -
    - Patrick Cook
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


# **********************************
# authorization token, generated from development page of Dropbox
TOKEN = 'C27L8RWZZpkAAAAAAAANfcaGjLoOvAKsJ_7e3DYHc-zYifjRDDaO-F7JIm6_TEWM'

# this is brooks token, its the one we used in the hackathon
# TOKEN = 'S-aVck8tNgAAAAAAAAAAIInlY4_XleRSGvTFV95_fglkcLh51JOHGg66tq_bV-3z'
# **********************************



# ********** REMEMBER TO CHANGE BACKUPPATH FILE PATH TO YOUR MACHINES FILEPATH*******

# backup path and log file that will be created/modified inside of it
BACKUPPATH = 'backupPrac/'
if(os.path.exists(BACKUPPATH + 'log.txt')):
    LOG = open(BACKUPPATH + 'log.txt', 'w')
else:
    LOG = open(BACKUPPATH + 'log.txt', 'aw')
LOG.write('\t  Files \t\t\t\t  Date : Time\n')


#get file names in dropbox root
def get_files_and_folders(dbx):
    allFiles = dict()   # stores metadata in key value pair structure
    otherDirectories = []
    client = dropbox.client.DropboxClient(TOKEN)
    metadata = client.metadata('/')

    print("\t - Gathering file paths")
    files = [content['path'].split('/')[-1] for content in metadata['contents']]
    for x in files:
        if x.find('.') > -1:
            metadata = dbx.files_get_metadata('/' + x).content_hash
            allFiles[x] = metadata
        else:
            otherDirectories.append(x)

    compare_to_local(dbx, allFiles)


# compare dropbox files to files in backup location, note differences
# remote to local
# files contains the meta data for each file
def compare_to_local(dbx, files):
    # can localFiles be an array/list?
    localFiles = dict()
    downloadThese = []
    uploadThese = []

    #This is comparing the time since last modification of local to remote
    temp = [f for f in listdir(BACKUPPATH) if isfile(join(BACKUPPATH, f))]
    for path in temp:
        file_mod_time = os.stat(BACKUPPATH + path).st_mtime
        localFiles[path] = file_mod_time;

    print("\t - Comparing directories")

    for x, y in files.items():        # what is the metadata it is searching through
        downloadThese.append(x)

    for x, y in localFiles.items():   # iterating through each files mod time
        inDropbox = 0
        for w, z in files.items():
            if(w == x):
                inDropbox = 1
        if(inDropbox == 0):
            uploadThese.append(x)

    updateDirectories(dbx, downloadThese, uploadThese)


# upload files from local backup, download files from dropbox
def updateDirectories(dbx, downloadThese, uploadThese):
    print("\t - Updating your directories")
    dropBoxPath = ""

    for path in downloadThese:
        dbx.files_download_to_file(BACKUPPATH + path, '/' + path)
        LOG.write(path + ' \t\t\t '
                + datetime.datetime.now().strftime('%Y-%m-%d : %H:%M:%S') + '\n\n')

    for path in uploadThese:
        if(path != "log.txt"):
            dbx.files_upload(BACKUPPATH + path, '/' + path, mode=WriteMode('add'))
            # writing to log!
            LOG.write(path + ' \t\t\t '
                    + datetime.datetime.now().strftime('%Y-%m-%d : %H:%M:%S') + '\n\n')



    print("\t - Syncing has finished\n")
    print("Consult log.txt for further information\n")


# **************************** This is where the program starts *****************
if __name__ == '__main__':

    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. "
            "Open up backup-and-restore-example.py in a text editor and "
            "paste in your token in line 14.")


    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Initiating connection with Dropbox...")
    dbx = dropbox.Dropbox(TOKEN)
    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
            "access token from the app console on the web.")

    '''
    #works but functions are not created
    # consider selection menu

    print('what would you like to do?')
    print('\t 1) Backup 2) Restore \n\t 2) Delete \n\t 3) Ignore\n\n')
    usrChoice = raw_input('Please enter 1, 2, or 3: ')

    if (usrChoice == 1):
        get_files_and_folders(dbx)
    elif (usrChoice == 2)):
        call restore function
    ilif (usrChoice == 3):
        Call delete function:
    else (usrChoice == 4:
        Call ignore function)
    '''

    # **** Start program cycle ****
    get_files_and_folders(dbx)


    LOG.close()
