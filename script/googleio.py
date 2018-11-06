#Copyright (c) 2018 Ian Pendleton - MIT License
#### Some useful links for later, possibly
########################################################################################
### https://stackoverflow.com/questions/43865016/python-copy-a-file-in-google-drive-into-a-specific-folder
### https://github.com/gsuitedevs/PyDrive
### https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


##Authentication for pydrive, designed globally to minimally generate token (a slow process)
gauth = GoogleAuth()
gauth.LoadCredentialsFile("localfiles/mycred.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth() #Creates local webserver and auto handles authentication.
elif gauth.access_token_expired:
    gauth.LocalWebserverAuth() #Creates local webserver and auto handles authentication.
else:
    gauth.Authorize() #Just run because everything is loaded properly
gauth.SaveCredentialsFile("localfiles/mycred.txt")
drive=GoogleDrive(gauth)

##Creating template directory for later copying of relevant files
def DriveCreateFolder(title1):
    tgt_folder_id='11vIE3oGU77y38VRSu-OQQw2aWaNfmOHe' #Target Folder for debugging
    file_metadata = {
        'title': title1,
        "parents": [{"kind": "drive#fileLink","id": tgt_folder_id}],
        'mimeType': 'application/vnd.google-apps.folder'  #mimetype sets the type of object to a folder type
    }
    file = drive.CreateFile(file_metadata)
    file.Upload()
    print("Directory Created: " + "%s" %(title1))
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % tgt_folder_id}).GetList()
    for file1 in file_list:       
        if file1['title']==title1:
            return(file1['id'])
        else:
            pass

##Copies all files from template directory into the new directory
##Returns a referenced dictionary of files (title, Gdrive ID)
def DriveAddTemplates(opdir, RunID):
#    template_folder='1HneaSFzgJgHImDAL-8OgQfSx1ioFJp6S'  #Debugging target folder
    template_folder='131G45eK7o9ZiDb4a2yV7l2E1WVQrz16d' #New template 11/5/2018
    file_template_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % template_folder}).GetList()
    for templatefile in file_template_list:       
            basename=templatefile['title']
            drive.auth.service.files().copy(fileId=templatefile['id'], body={"parents": [{"kind": "drive#fileLink", "id": opdir}], 'title': '%s_%s' %(RunID,basename)}).execute(),
    newdir_list = drive.ListFile({'q': "'%s' in parents and trashed=false" %opdir}).GetList()
    ExpDataFile="%s_ExpDataEntry"%(RunID)
    new_dict={}
    for file1 in newdir_list:
        new_dict[file1['title']]=file1['id']
    return(new_dict)

def GupFile(opdir, filelist, rxndict):
    for file in filelist:
        outfile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": opdir}]})
        outfile.SetContentFile(file)
        outfile['title']=file.split('/')[1]
        outfile.Upload()
    logfile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": opdir}]})
    logfile.SetContentFile(rxndict['logfile'])
    logfile['title']='%s_LogFile.txt'%rxndict['RunID']
    logfile.Upload()
    print((filelist), logfile['title'], "Successfully Uploaded")