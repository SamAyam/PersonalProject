import random, datetime

# ANDROID VERSION


# making it compatible for android:
#
# From
# "saved/"
# To
# "/storage/emulated/0/com.hipipal.qpyplus/projects3/Options & Decisions/saved/"
#
# From
# "FileNotFoundError"
# To
# "IOError"
#
# From
# "from sync import sync_to_web"
# To
# "from mobile_sync import sync_to_web"
#
# -optional- put "start" in main()



# TODO list:
# create new start file
# try to break the program, find errors
#    like putting letters in edit->count
#    or editing a non existant note


def sync_files(dothis):
    """Runs the "sync.py" program."""
    try:
        from mobile_sync import sync_to_web
    except ImportError:
        print("\n\nNo sync program.\n")
        return
    if dothis=='ask':
        sync_to_web()
    else:
        sync_it=input("\n\nDo you want to "+dothis+" the files first?\n(y, n) ")
        print("\n\n")
        if sync_it == "y":
            if dothis=='download':
                sync_to_web('download all')
            elif dothis=='upload':
                sync_to_web('upload')
    
            

def record_change(change_type, change):
    log=open(save_folder+"/CHANGE_LOG.txt", 'a')
    log.write('\n  -New change- \n')
    log.write(change_type)
    log.write('\n')
    log.write(str(datetime.datetime.now()))
    log.write('\n')
    log.write(change)
    log.write('\n  -End of change- \n\n')
    log.close()


def file_to_options(file_name):
    #try:
    filename=file_name.replace(" ","_")
    thisfile=open(save_folder+filename+'.txt', 'r')
    string=thisfile.read()
    thisfile.close()
    #except IOError:
    #    print("\nFile not found.\n")
    #    return
    the_list=[]
    sub_list=[]
    option=[]
    optionlist=[]
    new_option=True
    end_option=False
    temp_list=string.split("\n")
    #print(string)
    for items in temp_list:
        #print(the_list)
        if items=="":
            
            #if new_option==True:
            #    #print("working")
            #    if optionlist!=[]:
            #        option.append(optionlist)
            #        the_list.append(option)
            #    optionlist=[]
            #    option=[]
            if end_option==True:
                new_option=True
                end_option=False
                #print("working")
                option.append(optionlist)
                the_list.append(option)
                optionlist=[]
                option=[]
            else:
                end_option=True
                if sub_list!=[]:
                    optionlist.append(sub_list)
                    sub_list=[]

        else:
            if new_option==True:
                option.append(items)
                new_option=False
                end_option=False
            else:
                sub_list.append(might_be_int(items))
                end_option=False
    option.append(optionlist)
    the_list.append(option)
    return the_list

def option_to_file(the_list):
    string=''
    for items in the_list:
        #string=string+"\n"
        if type(items)==list:
            #string=string+"\n"
            for thing in items:
                if type(thing)==list:
                    string=string+"\n"
                    
                    for each in thing:

                            string=string+str(each)+"\n"
                else:
                    string=string+"\n"+str(thing)
        else:
            string=string+str(items)+"\n"
    return string


def list_to_file(the_list):
    string=''
    for items in the_list:
        #string=string+"\n"
        if type(items)==list:
            string=string+"\n"
            for thing in items:
                if type(thing)==list:
                    string=string+"\n"
                    
                    for each in thing:
                        if type(each)==list:
                            string=string+"\n"
                            for option in each:
                            #    if type(option)==list:
                                #string=string+"\n"
                            #        for this in option:
                                string=string+str(option)+"\n"
                                        #print(string)
                                #else:
                                #    string=string+str(option)+"\n"
                        else:
                            string=string+str(each)+"\n\n"
                else:
                    string=string+"\n"+str(thing)
        else:
            string=string+str(items)+"\n"
    return string


def list_to_string(the_list):
    string=''
    for items in the_list:
        string=string+"\n"
        for thing in items:
            string=string+str(thing)+"\n"
    return string


def string_to_list(string):
    the_list=[]
    sub_list=[]
    temp_list=string.split("\n")
    for items in temp_list:
        if items=="":
            if sub_list!=[]:
                the_list.append(sub_list)
            sub_list=[]
        else:
            sub_list.append(might_be_int(items))
    return the_list

            
def might_be_int(string):
    try: 
        number=int(string)
        return number
    except ValueError:
        return string

def check_option(opt_name, file_name='none'):
    """Returns false if option already exists and
    overwrite permission is not given.
    Returns True if it is ok to save.
    """
    while file_name=='none':
        if file_name=="":
            return False
        else:
            file_name=input("\nWhat start file should it be attached to?\n\n")
    file_name=file_name.replace(" ","_")
    file=open(save_folder+file_name+'.txt', 'r')
    all_text=file.read()
    file.close()
    all_options=string_to_list(all_text)
    
    found=False
    for this_opt in all_options:
        if this_opt[0]==opt_name:
            found=True
            
    if found==True:
        rewrite=input("Are you sure you want to overwrite this option?"
                      "\n(y, n) ")
        if rewrite=='y' or rewrite=='Y':
            return True
        else:
            return False
    else:
        return True



def check_file(file_name):
    """Returns false if file already exists and
    overwrite permission is not given.
    Returns True if it is ok to save.
    """
    try:
        file_name=file_name.replace(" ","_")
        file=open(save_folder+file_name+'.txt', 'r')
        file.close()
        rewrite=input("Are you sure you want to overwrite this file?"
                      "\n(y, n) ")
        if rewrite=='y' or rewrite=='Y':
            return True
        else:
            return False
    except IOError:
        return True



def remove_from_file(option, file_name):
    file_name=file_name.replace(" ","_")
    #file=open(save_folder+file_name+'.txt', 'r')
    #text=file.read()
    #file.close()
    all_options=file_to_options(file_name)
    for each in all_options:
        if each[0]==option:
            all_options.remove(each)
    file=open(save_folder+file_name+'.txt', 'w')
    file.write(list_to_file(all_options))
    file.close()
    


def add_to_file(option, file_name):
    file=open(save_folder+file_name+'.txt', 'a')
    file.write("\n\n"+str(option_to_file(option))+"\n")
    file.close()


def edit(fname, name='none'):
    options=[]
    been_saved=False
    if name=="none":
        name=input("\nWhat is the name of the option? ")
        
    while options==[]:
        if name=="":
            return
        try:
            #file=open(save_folder+fname+'.txt', 'r')
            #text=file.read()
            #file.close()
            all_options=file_to_options(fname)
            for things in all_options:
                if name == things[0]:
                    options=things[1]
            if options==[]:
                print("\nOption Not Found\n")
                return
            else:
                print("\n\n        "+name+":")
                print(list_to_string(options))
        except IOError:
            name=input("\nSorry, I couldn't find that file."
                        '\nTry another file name. ')

    edit=input("\nDo you want to ADD, REMOVE, RENAME, MOVE, DELETE,"
               "\nCOUNT, make a NOTE, SAVE, or QUIT editing files? ")
    while edit != "quit":
        
        if edit == "add":
            add=input("\nWhat do you want to add? ")
            options.append([add, 0])
            been_saved=False
                
        elif edit=='remove':
            remove=input('What do you want to remove? ')
            for item in options:
                if remove == item[0]:
                    options.remove(item)
                    been_saved=False

        elif edit=="rename":
            which_one=input("Which one do you want to rename? ")
            what=input("What do you want to change it to? ")
            for item in options:
                if which_one == item[0]:
                    item[0]=what
                    been_saved=False
            
        elif edit=="move":
            #been_saved=False
            which_one=input("Which one do you want to move? ")
            where=input("\nWhich one should it come after?\n"
                        'or type "0" if it\'s first. ')
            been_saved=False
            for item in options:
                if which_one == item[0]:
                    i=options.index(item)
                    if where =="0":
                        options.insert(0, item)
                        del options[i+1]
                    else:
                        for after_me in options:
                            if where in after_me:
                                j=options.index(after_me)
                                options.insert(j+1, item)
                                if j>i:
                                    del options[i]
                                else:
                                    del options[i+1]

        elif edit=="delete":
            sure=input("\nAre you sure you want to delete this option?\n(y, n) ")
            if sure=='y':
                remove_from_file(name, fname)
                print("\n\nFile removed.\n")
                return
                
        elif edit=='count':
            #been_saved=False
            which_one=input("\nWhich one do you want to count? ")
            to_what=input("\nEnter the number of views"
                          '\nor leave blank to add 1 view. ')
            been_saved=False
            for item in options:
                if which_one == item[0]:
                    if to_what=="":
                        item[1]=int(item[1])+1
                    else:
                        item[1]=int(to_what)

        elif edit=='note':
            been_saved=False
            which_one=input("\nChange the notes for which one? ")
            
            for this_one in options:
                if which_one in this_one:
                    do_this=input('\nDo you want to add, remove, rename or move? ')
                    if do_this=='add':
                        more=input("\nNote: ")
                        while more != "":
                            if len(this_one)==2:
                                this_one.append("    NOTES:")
                            this_one.append(more)
                            more=input("Next note: ")
                    elif do_this=='remove':
                        rmv=input("\nWhich one should be removed? ")
                        #try
                        #except
                        #break
                        if this_one.index(rmv)<3:
                            print("That is not a note.")
                        else:
                            this_one.remove(rmv)
                            if len(this_one)<4:
                                del this_one[2]
                    elif do_this=='rename':
                        old_name=input("\nWhich one? ")
                        #try
                        #except
                        #break
                        i=this_one.index(old_name)
                        if i<3:
                            print("\nThat is not a note.")
                        else:
                            new_name=input("\nWhat is the new name? ")
                            this_one[i]=new_name
                    elif do_this=='move':
                        old_name=input("Which one do you want to move? ")
                        # this can cause an error, use "try" instead
                        # error if index doesn't exist, and can't find numbers
                        #    check_if_int?
                        #try
                        #except
                        #break
                        i=this_one.index(old_name)
                        while i<3:
                            print("\nThat is not a note.")
                            old_name=input("Which one do you want to move? ")
                            i=this_one.index(old_name)
                        where=input("\nWhich one should it come after?\n"
                                    'or type "0" if it\'s first. ')
                        if where =="0":
                            this_one.insert(3, this_one[i])
                            del this_one[i+1]
                        else:
                            for after_me in this_one:
                                if where == after_me:
                                    j=this_one.index(after_me)
                                    if j<2:
                                        print("\nThat is not a spot for notes")
                                    else:
                                        this_one.insert(j+1, this_one[i])
                                        if j>i:
                                            del this_one[i]
                                        else:
                                            del this_one[i+1]
                    else:
                        print("\nOops, there must be a typo.\n")
            
        elif edit=='save':
            overwrite=input("\nDo you want to overwrite the old option"
                            "\nwith the same name? (y, n) ")
            if overwrite=='y':
                #name=name.replace(" ","_")
                #opt=[]
                #print(fname)
                opt=[name]
                opt.append(options)
                remove_from_file(name, fname)
                
                add_to_file(opt, fname)
                
                #add_to_file(name, fname)
                #file=open(save_folder+name+".txt", 'w')
                #file.truncate()
                #file.write(list_to_string(options))
                #file.close()
                record_change("Overwrite "+name, list_to_string(options))
                print("\nThe file was saved.")
                been_saved=True
            else:
                safe_to_save=False
                while safe_to_save==False:
                    opt_name=input("\nWhat do you want to save it as? ")
                    safe_to_save=check_option(opt_name, fname)
                if opt_name!="":
                    #fname=fname.replace(" ","_")
                    #remove_from_file(name)
                    opt=[opt_name]
                    opt.append(options)
                    add_to_file(opt, fname)
                    #file=open(save_folder+fname+".txt", 'w')
                    #file.truncate()
                    #file.write(list_to_string(options))
                    #file.close()
                    record_change("Edit "+opt_name, list_to_string(options))
                    print("\nThe file was saved.")
                    been_saved=True
                else:
                    print("\nThe file was NOT saved.")

        else:
            print("\nTry again... ")

        print("\n\n        "+name+":")
        print(list_to_string(options))
        edit=input("\nDo you want to ADD, REMOVE, RENAME, MOVE, DELETE,"
                   "\nCOUNT, edit a NOTE, SAVE, or QUIT editing files? ")
        
        if edit == "quit":   # if changes were made but the file was not saved
            if been_saved==False:
                quick_check=input("\nSave changes first? (y, n) ")
                if quick_check=="y":
                    overwrite=input("\nDo you want to overwrite the old file"
                                    "\nwith the same name? (y, n) ")
                    if overwrite=='y':
                        #name=name.replace(" ","_")
                        opt[0]=name
                        opt.append(options)
                        remove_from_file(name, fname)
                        add_to_file(opt, fname)
                        #file=open(save_folder+name+".txt", 'w')
                        #file.truncate()
                        #file.write(list_to_string(options))
                        #file.close()
                        record_change("Overwrite "+name, list_to_string(options))
                        print("\nThe file was saved.")
                        been_saved=True
                    else:
                        safe_to_save=False
                        while safe_to_save==False:
                            file_name=input("\nWhat do you want to save it as? ")
                            safe_to_save=check_file(file_name)
                        if file_name!="":
                            file_name=file_name.replace(" ","_")
                            opt[0]=name
                            opt.append(options)
                            remove_from_file(name, fname)
                            add_to_file(opt, fname)
                            #file=open(save_folder+file_name+".txt", 'w')
                            #file.truncate()
                            #file.write(list_to_string(options))
                            #file.close()
                            record_change("Edit "+file_name, list_to_string(options))
                            print("\nThe file was saved.")
                            been_saved=True
                        else:
                            print("\nThe file was NOT saved.")
                else:
                    print("\nThe file was NOT saved.")

    return options
        

def load_file(name):
    passed=False
    while passed==False:
        if name=="":
            return True
        if name==".":
            return False
        try:
            all_options=file_to_options(name)
            passed=True
        except IOError:
            name=input("\nSorry, I couldn't find that file."
                        '\nTry another file name: ')
    load_and_run(name, name)
        
def load_and_run(name, fname):
    stop=False
    passed=False
    while passed==False:
        if name=="":
            return True
        if name==".":
            return False

        try:
            #filename=name.replace(" ","_")
            #file=open(save_folder+filename+'.txt', 'r')
            #text=file.read()
            #file.close()
            all_options=file_to_options(fname)
            #jdjd=irir
            #print(all_options)

            for this_option in all_options:
                if str(this_option[0])==str(name):
                    options=this_option[1]
                    #name=name.replace(" ","_")
                    #file=open(save_folder+name+'.txt', 'r')
                    #text=file.read()
                    #file.close()
                    #options=string_to_list(text)
                    passed=True

            if passed==False:
                name=input("\nSorry, I couldn't find that option."
                            '\nTry another file name'
                            '\nor enter "." to go back: ')

            

        except IOError:
            filename=input("\nSorry, I couldn't find that file."
                        '\nTry another file name'
                        '\nor enter "." to go back: ')


                       
        

    print("\n\n        "+name+":")
    print(list_to_string(options))
    
    then_what=input('\nPick one \nor enter "," for a random choice'
                    '\nor ";" to edit this file'
                    '\nor "." to go back a file: ')
    while stop==False:
        if then_what==",":
            new_name=random_choice(options)
            print("\n\n"+str(new_name))
            again=input('\nType "y" to run the related file. ')
            if again=="y":
                count_it=input("Count and save choice? (y, n) ")
                if count_it=='y':
                    for item in options:
                        if new_name in item:
                            #i=options.index(item)
                            item[1]=1+int(item[1])
                            #name=name.replace(" ","_")
                            remove_from_file(name, fname)
                            opt=[name]
                            opt.append(options)
                            add_to_file(opt, fname)
                            #file=open(save_folder+fname+".txt", 'a')
                            #file.truncate()
                            #file.write(list_to_string(options))
                            #file.close()
                            record_change('Counted "'+new_name+'" in '+name, list_to_string(options))
                            print("\nCounted and saved.")
                stop=load_and_run(new_name, fname)
            else:
                print("\n\n    "+name+"\n"+list_to_string(options))
            
        elif then_what ==";":
            options=edit(fname, name)
            print("\n\n")
            stop=load_and_run(name, fname)

        elif then_what==".":
            return False
        
        elif then_what=="":
            return True
        
        else:
            found_it=False
            for item in options:
                if then_what in item[0]:
                    found_it=True
                    count_it=input("Count and save choice? (y, n) ")
                    if count_it=='y':
                        #i=options.index(item)
                        item[1]=1+int(item[1])
                        remove_from_file(name, fname)
                        opt=[name]
                        opt.append(options)
                        #name=name.replace(" ","_")
                        add_to_file(opt, fname)
                        #file=open(save_folder+name+".txt", 'w')
                        #file.truncate()
                        #file.write(list_to_string(options))
                        #file.close()
                        record_change('Counted "'+item[0]+'" in '+name, list_to_string(options))
                        print("\nCounted and saved.")
                    stop=load_and_run(item[0], fname)
            if found_it==False:
                stop=load_and_run(then_what, fname)
                
                    
        if stop == False:
            print("\n\n        "+name+":")
            print(list_to_string(options))
            then_what=input('\nPick one \nor enter "," for a random choice'
                            '\nor ";" to edit this file'
                            '\nor "." to go back a file: ')
    return True


def random_choice(options):
    count=len(options)-1
    number=random.randint(0,count)
    return options[number][0]


def manually():
    options=[]
    count=1
    print('\nAdd "...." to an option to give it notes.')
    option=input("\nGive me option 1: ")
    while option!="":
        count=count+1
        if "...." in option:
            option = option.replace("....", "")
            morestuff=[option, 0, "Notes: "]
            more=input("Type the note: ")
            while more != "":
                morestuff.append(more)
                more=input("Next note: ")
            options.append(morestuff)
        else:
            options.append([option, 0])
        option=input("Give me option "+str(count)+": ")
    return options


#____________________________________________

def main(choice="none"):
    sync_files('download')

    startFile="My_Start"
    
    running=True
    while running == True:

        if choice=="none":
            choice=str(input("\n\n  ________MAIN MENU________\n(start file: "+str(startFile)+
                             ")\nDo you want to ... \n\nLOAD a file\nEDIT a file\nCreate a NEW file"
                             "\nManually enter a QUICK list\nROLL dice of any size"
                             "\nRun the START file\nRun the SYNC program"
                             "\nPICK a start file\nOr QUIT the program? "))

        if choice == "load":
            name=input("\nWhat is the option called? ")
            #name=name.replace(" ","_")
            load_and_run(name, startFile)
            choice="none"

        elif choice == "edit":
            options=edit(startFile)
            choice ="none"
                
        elif choice == "new":
            safe_to_save=False
            while safe_to_save==False:
                name=input("\nWhat do you want to save it as? ")
                if name=="":
                    break
                filename=input("\nWhich start file should it get attached to?"
                               "\n(leave blank for the current start file)")
                if filename=="":
                    filename=startFile
                filename=filename.replace(" ","_")
                safe_to_save=check_option(name, filename)
            if name!="":
                options=manually()
                remove_from_file(name, filename)
                opt=[name]
                opt.append(options)
                add_to_file(opt, filename)
                #file=open(save_folder+name+".txt", 'w')
                #file.truncate()
                #file.write(list_to_string(options))
                #file.close()
                fname=startname.replace(" ","_")
                record_change('New '+name, list_to_string(options))
                print("\nFile saved.")
                choice="none"
            else:
                print("\nThe file was NOT saved.")
                choice="none"
            
        elif choice=="quick":
            again="new"
            while again !='main':
                if again=="new":
                    choices=manually()
                    chosen=random_choice(choices)
                    print("")
                    print(chosen)
                elif again == "":
                    chosen=random_choice(choices)
                    print("")
                    print(chosen)
                elif again == "save":
                    safe_to_save=False
                    while safe_to_save==False:
                        name=input("\nWhat do you want to save it as? ")
                        fname=input("\nWhich file do you want to attach it to?"
                                    "\n(leave blank for current file) ")
                        fname.replace(" ","_")
                        if fname=="":
                            fname=startFile
                        if name=="":
                            again='main'
                            break
                        safe_to_save=check_option(name, fname)
                    remove_from_file(name, fname)
                    opt=[name]
                    opt.append(choices)
                    add_to_file(opt, fname)
                    print("\nThe file was saved.")
                    record_change('QuickList '+name+fname, list_to_string(choices))
                    again="none"
                elif again == "quit":
                    running=False
                    again='main'
                    return
                
                if again!="main":
                    again=input("\nPress only enter to randomly choose again"
                                '\nor type "save" to save this list'
                                '\nor type "new" to make a new quick list'
                                '\nor type "main" to go to the main menu'
                                '\nor type "quit" to quit the program. ')
            choice="none"

        elif choice=="roll":
            again=True
            while again==True:
                how_many=input("\n\nHow many dice?\nLeave blank for only one. ")
                print("\n")
                if how_many=="":
                    how_many=1
                dielist=[]
                for die in range(0,int(how_many)):
                    sides=input("\nHow many sides for die #"+str(die+1)+"? ")
                    if sides=="":
                        sides=6
                    dielist.append(sides)
                input("\n\nPress enter to roll! ")
                print("\n\n")
                keeprolling=True
                while keeprolling==True:
                    diecount=0
                    for die in dielist:
                        diecount=diecount+1
                        if len(dielist)==1:
                            print("==== "+str(random.randint(1,int(die))))
                        else:
                            print("#"+str(diecount)+" = "+str(random.randint(1,int(die))))
                    ask_again=input("\nPress only enter to roll again. ")
                    print("\n\n")
                    if ask_again!="":
                        keeprolling=False
                ask_again=input("\nDo you want to choose new dice? (y, n) ")
                if ask_again!="y":
                    again=False
            choice="none"
            
        elif choice=="start":
            startname=startFile.replace("_"," ")
            load_and_run(startname, startFile)
            choice='none'

        elif choice=='sync':
            sync_files("ask")
            choice='none'

        elif choice=='pick':
            startname=input("\nWhat is the name of the start file?"
                            "\nLeave blank for the default file,"
                            '\nor enter "." to create a new start file. ')
            if startname=="":
                startname="My Start"
                
            if startname==".":
                safe_to_save=False
                while safe_to_save==False:
                    name=input("What is the name of the new start file? ")
                    safe_to_save=check_file(name)
                    if name=="":
                        choice="none"
                        break
                if name!="":    
                    options=manually()
                    file=open(save_folder+name.replace(" ","_")+".txt", 'w')
                    file.write("\n"+name+"\n")
                    file.write(list_to_string(options))
                    file.close()
                    startFile=name.replace(" ","_")
                    record_change("NewFile "+name, list_to_string(options))
                    
            else:
                try:
                    tempFile=startname.replace(" ","_")
                    file=open(save_folder+tempFile+".txt","r")
                    file.read()
                    file.close()
                    startFile=tempFile
                    print("\n\nChanged.\n")
                except IOError:
                    input("\n\nStart file not found.\n")
            choice="none"

        elif choice=='quit':
            sync_files('upload')
            running=False

        else:
            choice=input("\nERROR \nHere are the options:\n"
                         "load\nedit\nnew\nquick\nroll"
                         "\nstart\nsync\npick\nquit\n"
                         "Please choose from this list. ")
            

if __name__ == '__main__':
    
# CHANGE THE SAVE FOLDER HERE
    save_folder="/storage/emulated/0/com.hipipal.qpyplus/projects3/Options & Decisions/saved/"
    
    main('start')
