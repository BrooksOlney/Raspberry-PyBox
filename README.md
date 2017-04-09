# Raspberry-PyBox
## Regularly backup files from Dropbox using the Python SDK


 ###### if you want to do more with accessing backup files create your own dropbox app and change the TOKEN variable in main


###### questions/concerns/notes in main.py:
   - line 7
   - can main be moved to the top?
   - c++ uses a set precision function to make text more
      accurate, maybe python has one so we can make the log file like a table
   - put all functions/code regarding token/backuPath/dbx init into another folder, then in main just call the function to access the needed instruction/information
   - create delete and ignore function to delete or ignore certain files
       - ignore will disregard given file/folder while preforming backup/restore process
   - separate update function to backup or restore based on choice



 program cycle:
   - calls main -> line 102
   - gets files and folders -> line 43
   - comparing directories -> line 65
   - update directories -> line 93
