import base64, json, urllib, hashlib
from urllib.request import Request, urlopen
from os import listdir
from os.path import isfile, join


# WINDOWS VERSION


# making it compatible for android:
#
# From
# "saved/"
# To
# "/storage/emulated/0/com.hipipal.qpyplus/projects3/Options & Decisions/saved/"



def sync_to_web(choice='none'):
    """This program syncronizes files with an online server."""
    
    # FOLDER FOR SAVE FILES:
    save_folder="saved/"
    
    # (if you want to use a different folder, this is the line to change)
    


    # getting user account numbers:
    file=open(save_folder+"My_Account.txt")
    text=(file.read().split("\n"))
    file.close()

    account_id=(text[0].split('=')[1])
    application_key=(text[1].split('=')[1])
    bucket_id =(text[2].split('=')[1])


    ###################### AUTHORIZE FIRST:#####################
    id_and_key = account_id+':'+application_key
    id_and_key=(base64.b64encode(id_and_key.encode('utf-8')))
    id_and_key=id_and_key.decode('utf-8')
    basic_auth_string = 'Basic ' + id_and_key
    headers = { 'Authorization':basic_auth_string}
    request = Request(
        'https://api.backblaze.com/b2api/v1/b2_authorize_account',
        headers = headers
        )
    try:
        response=urlopen(request)
    except urllib.error.URLError:
        print("\n\nSorry, couldn't access the website\n"
              "or the member numbers are wrong.")
        return
    response_bytes=response.read()
    response_text=response_bytes.decode('utf-8')
    response_data=json.loads(response_text)
    response.close()


    
    account_authorization_token = response_data['authorizationToken']
    api_url = response_data['apiUrl']
    download_url = response_data['downloadUrl']


    
    ### setting upload url and token:
    data=json.dumps({ 'bucketId' : bucket_id })
    request = Request(
            '%s/b2api/v1/b2_get_upload_url' % api_url,
            data=bytes(json.dumps({ 'bucketId' : bucket_id }),'utf-8'),
            headers = { 'Authorization': account_authorization_token }
            )
    response = urlopen(request)
    response_bytes=response.read()
    response_text=response_bytes.decode('utf-8')
    response_data=json.loads(response_text)
    response.close()

    

    uploadUrl = response_data['uploadUrl']
    upload_authorization_token = response_data['authorizationToken']



    ###################### DONE AUTHORIZING #####################
    

    if choice=="none":
        up_or_down=input('Enter "n" to DOWNload\n'
                         'or "p" to UPload. ')
        if up_or_down=='p':
            choice="upload"
        elif up_or_down=='n':
            choice="download all"

        

    if choice=="upload":
        then_what=input("What file do you want to UPLOAD?\n"
                        "(leave blank to upload all)\n")
        if then_what=='':
            choice="upload all"
        else:
            choice="upload one"
            which_file=then_what



    if choice=="list files":
        data=json.dumps({ 'bucketId' : bucket_id })

        request = Request(
                '%s/b2api/v1/b2_list_file_names' % api_url,
                data=bytes(data,'utf-8'),
                headers = { 'Authorization': account_authorization_token})
        response = urlopen(request)
        response_text=response.read()
        response_data=response_text.decode('utf-8')
        response.close()

        print(response_data)
        whenDone=input("\n\nDONE  ")



    elif choice=="list buckets":
        data=json.dumps({'accountId' : account_id })

        request = Request(
                '%s/b2api/v1/b2_list_buckets' % api_url,
                data=bytes(data,'utf-8'),
                headers = { 'Authorization': account_authorization_token})
        response = urlopen(request)
        response_text=response.read()
        response_data=response_text.decode('utf-8')
        response.close()

        print(response_data)
        whenDone=input("\n\nDONE  ")



    elif choice=='download one':
        # put file id here:
        file_id = ""

        response = (urlopen(download_url + '/b2api/v1/b2_download_file_by_id?fileId=' + file_id))
        response_text=response.read()
        response_data=response_text.decode('utf-8')
        response.close()

        print(response_data)
        whenDone=input("\n\nDONE")



    elif choice=='download all':
        ready=input("\nPress enter to DOWNLOAD ALL.\n"
                    'Press any other key first to cancel and quit. '
                    )
        if ready!='':
            done=input("\nDownload cancelled.\n")
            return
        data=json.dumps({ 'bucketId' : bucket_id })  # used for getting files list

        request = Request(
                '%s/b2api/v1/b2_list_file_names' % api_url,
                data=bytes(data,'utf-8'),
                headers = { 'Authorization': account_authorization_token})
        response = urlopen(request)
        response_bytes=response.read()
        response_text=response_bytes.decode('utf-8')
        response_data=json.loads(response_text)
        response.close()
        
        files=response_data['files']
        matches=[]
        for each in files:
            if "fileName" in each:
                matches.append(each["fileName"])

        print("\n...Downloading All...\n")

        for item in files:
            newFileName=matches[0]
            del matches[0]
            if 'fileId' in item:
                file_id=(item['fileId'])
                response = (urlopen(download_url + '/b2api/v1/b2_download_file_by_id?fileId=' + file_id))
                response_text=response.read()
                response_data=response_text.decode('utf-8')
                response.close()
                f=open(save_folder+newFileName,"w")
                f.write(response_data)
                f.close()

        whenDone=input("\n\nDONE DOWNLOADING  ")
        

    elif choice=="upload one":
        try:
            str(which_file)
        except UnboundLocalError:
            which_file=input('Enter the name of the text file to UPLOAD (without ".txt")\n ')
        
        file_name=which_file.replace(" ","_")
        f=open(save_folder+file_name+".txt",'r')
        file_data=f.read()
        f.close()
        content_type = "text/plain"
        sha1_of_file_data = hashlib.sha1(bytes(file_data,'utf-8')).hexdigest()
        headers = {
            'Authorization' : upload_authorization_token,
            'X-Bz-File-Name' :  file_name+".txt",
            'Content-Type' : content_type,
            'X-Bz-Content-Sha1' : sha1_of_file_data
            }
        request = Request(uploadUrl, data=bytes(file_data,'utf-8'), headers=headers)

        keep_trying=True
        while keep_trying==True:
            try:
                print("...Uploading...")
                response=urlopen(request)
                response_bytes=response.read()
                response_text=response_bytes.decode('utf-8')
                response_data=json.loads(response_text)
                response.close()

                print(response_data['fileName']+"   ....Uploaded ")
                again=input("\nUpload another text file? (y, n) ")
                if again=='y':
                    which_file=input('\n\nEnter the name of the next text file to UPLOAD (without ".txt")\n ')
                    
                    file_name=which_file.replace(" ","_")
                    f=open(save_folder+file_name+".txt",'r')
                    file_data=f.read()
                    f.close()
                    sha1_of_file_data = hashlib.sha1(bytes(file_data,'utf-8')).hexdigest()
                    headers = {
                        'Authorization' : upload_authorization_token,
                        'X-Bz-File-Name' :  file_name+".txt",
                        'Content-Type' : content_type,
                        'X-Bz-Content-Sha1' : sha1_of_file_data
                        }
                    request = Request(uploadUrl, data=bytes(file_data,'utf-8'), headers=headers)

                    
                else:
                    keep_trying=False
            except urllib.error.HTTPError:
                new_choice=input("\n\nERROR: Not all of the files were uploaded.\n"
                                  "\nLeave blank try again, \n"
                                  "Enter anything else to cancel upload.  ")
                if new_choice=='':
                    print("\n...Trying again...\n")
                else:
                    whenDone=input("\n...Upload cancelled...\n  ")
                    keep_trying=False
                    return
        whenDone=input("\n\nDONE UPLOADING  ")



    elif choice=="upload all":
        ready=input("\nPress enter to UPLOAD ALL.\n"
                    'Press any other key first to cancel and quit. '
                    )
        if ready!='':
            done=input("\nUpload cancelled.\n")
            return

        print("Getting files ready...")
        onlyfiles = [f for f in listdir(save_folder) if isfile(join(save_folder, f))]
        requestList=[]
        for item in onlyfiles:
            print(item)
            f=open(save_folder+item,'r')
            file_data=f.read()
            f.close()
            file_name = item
            content_type = "text/plain"
            sha1_of_file_data = hashlib.sha1(bytes(file_data,'utf-8')).hexdigest()

            headers = {
                'Authorization' : upload_authorization_token,
                'X-Bz-File-Name' :  file_name,
                'Content-Type' : content_type,
                'X-Bz-Content-Sha1' : sha1_of_file_data
                }
            request = Request(uploadUrl, data=bytes(file_data,'utf-8'), headers=headers)
            requestList.append(request)

        total=len(requestList)
        print("\nFiles ready.\nUploading all... \n")

        count=0
        for eachone in requestList:
            count=count+1
            keep_trying=True
            while keep_trying==True:
                try:
                    response=urlopen(eachone)
                    response_bytes=response.read()
                    response_text=response_bytes.decode('utf-8')
                    response_data=json.loads(response_text)
                    response.close()

                    print(response_data['fileName']+"        ....Uploaded "
                          +str(count)+"/"+str(total))
                    keep_trying=False
                except urllib.error.HTTPError:
                    new_choice=input("\n\nERROR: Not all of the files were uploaded.\n"
                                      "\nLeave blank try again, \n"
                                      'Enter "SKIP" to skip this file,\n'
                                      "Enter anything else to cancel all uploads.  ")
                    if new_choice=='':
                        print("\n...Trying again...\n")
                        keep_trying=True
                    elif new_choice=='skip':
                        print("\n...File skipped...\n")
                        keep_trying=False
                    else:
                        return
            
        whenDone=input("\n\nDONE UPLOADING  ")
        


    else:
        whenDone=input("\n\nNo actions were chosen.  ")

def main(ch='none'):
    """This is so the main function is not named "main"
    so it can be imported.
    """
    sync_to_web(ch)


if __name__=='__main__':
    main()
