from tkinter.filedialog import askopenfilenames
from tkinter import *
from firebase_admin import credentials, initialize_app, storage ,db
import os
from datetime import datetime
import time

# Init firebase with your credentials
cred = credentials.Certificate("depiction-d1b54-8044137b453f.json")
initialize_app(cred, {'storageBucket': 'depiction-d1b54.appspot.com','databaseURL':"https://depiction-d1b54-default-rtdb.asia-southeast1.firebasedatabase.app/"})





def InitializeEnv():
    global filelist ,Imagelinks
    Imagelinks=[]
    filelist=[]


def printFileList():
    for i in filelist:
        print(i)
        print("")

def openFilePicker():
    global filelist
    filelist.clear()

    filetuple = askopenfilenames()
    filelist=list(filetuple)
    # for i in filetuple:
    #     filelist.append(os.path.basename(i).split('/')[-1])
    



def onUploadclick():
    openFilePicker()
    printFileList()
    filenamesListbox.delete(0, END)
    var.set(filelist)


def getRuntimeUrl():
    return FirebaseRuntimebucketUrl.get()
def getCloudUrl():
    return FirebaseCloudbucketUrl.get()





def CreatePairDataSet(fileLinks,keys):
    print("Creating DataSet.....")    
    data = {}
    lenght=len(fileLinks)
    for i in range(lenght):
        key=keys[i]
        data[key]=fileLinks[i]
    print("Data set Created")
    return data
    





def uploadfilesToRuntime(filenameLinks,filenamekey):

    keyValuePair=CreatePairDataSet(filenameLinks,filenamekey)
    ref = db.reference('/').child(RuntimebucketPath.get())
    ref.update(keyValuePair)
    print("All Process Done")
    reset()





def uploadfilesToCloud(filenames,uploadPath):
    counter=0
    fileuploadname=[]
    for fileName in filenames:
        bucket = storage.bucket()
        # blob = bucket.blob(uploadPath+"/"+os.path.basename(fileName).split('/')[-1])                       # Put your local file path
        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d_%H_%M_%S").replace('/','_')
        key=dt_string+str(counter)
        blob = bucket.blob(uploadPath+"/"+key)
        fileuploadname.append(key)
        counter+=1


        blob.upload_from_filename(fileName)
        blob.make_public()                                 # Opt : if you want to make public access from the URL
        Imagelinks.append(blob.public_url)
        print("File Uploaded: ",fileName)
        time.sleep(1)
        
    
    uploadfilesToRuntime(Imagelinks,fileuploadname)



def fileUploadStart():
    printFileList()
    uploadfilesToCloud(filelist,StoragebucketPath.get())


def reset():
    global filelist ,Imagelinks
    filelist.clear()
    Imagelinks.clear()

room=Tk()
room.maxsize(600,600)
room.minsize(600,600)
room.title("Firebase-Adapter")
room.config(bg="#EEEE9B")


main=Frame(room,height=50)
main.pack(fill=X,pady=5)

Label(main, text="Choose your files from pc").pack()

fileseclector=Button(main,text="Choose files",command=onUploadclick)
fileseclector.pack(pady=10)


var=StringVar()
Label(main,text="File Name/Path List",fg="red").pack(anchor=NW,padx=10,pady=10)
filenamesListbox =Listbox(main,listvariable=var, height=10,bg="white")
filenamesListbox.pack(fill=X,padx=10)


fieldsFrame=Frame(room)
fieldsFrame.pack(fill=X)

frameBucket=Frame(fieldsFrame)
frameBucket.pack(fill=X)

FirebaseCloudbucketUrl=StringVar()
FirebaseCloudbucketUrl.set("depiction-d1b54.appspot.com")
Label(frameBucket,text="FireStorage Cloud Bucket",fg="red").pack()
filebucketEntry=Entry(frameBucket,textvariable=FirebaseCloudbucketUrl)
filebucketEntry.pack(padx=10,fill=X)

Label(frameBucket,text="Firebase Storage Bucket Path 'Default set to-> /'  ").pack(anchor=NW,padx=10)
StoragebucketPath=StringVar()
StoragebucketPath.set("pyImages")
StorageBucket_PathEntry=Entry(frameBucket,textvariable=StoragebucketPath)
StorageBucket_PathEntry.pack(padx=10,anchor=NW)


frameRuntimeBucket=Frame(fieldsFrame)
frameRuntimeBucket.pack(fill=X,pady=10)

FirebaseRuntimebucketUrl=StringVar()
FirebaseRuntimebucketUrl.set("https://depiction-d1b54-default-rtdb.asia-southeast1.firebasedatabase.app/")
Label(frameRuntimeBucket,text="FireStorage Runtime Url",fg="red").pack()
fileRunbucketEntry=Entry(frameRuntimeBucket,textvariable=FirebaseRuntimebucketUrl)
fileRunbucketEntry.pack(padx=10,fill=X)
 
Label(frameRuntimeBucket,text="Firebase Runtime Bucket Path 'Default set to-> /' ").pack(anchor=NW,padx=10)
RuntimebucketPath=StringVar()
RuntimeBucket_PathEntry=Entry(frameRuntimeBucket,textvariable=RuntimebucketPath)
RuntimeBucket_PathEntry.pack(padx=10,anchor=NW)



firebaseUploadButton=Button(room,text="Upload Data",command=fileUploadStart)
firebaseUploadButton.pack(pady=10)





InitializeEnv()

room.mainloop()