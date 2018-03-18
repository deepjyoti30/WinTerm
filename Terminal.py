from __future__ import print_function
from colorama import init, Fore, Style
import os
import shutil
import threading
import sys

init()
#Below is a class to use threading to find files.
class myThread(threading.Thread):
    def __init__(self, pathToSearch, fileTofind):
        threading.Thread.__init__(self)
        self.pathToSearch = pathToSearch
        self.fileTofind = fileTofind
    def run(self):
        List(self.pathToSearch, self.fileTofind)

#Below is a class to run functions used in grep in multiple threads
class grepThread(threading.Thread):
    def __init__(self, keyword, extension, path, Option):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.extension = extension
        self.path = path
        self.Option = Option
    def run(self):
        find_in_all_readable(self.keyword, self.extension, self.path, self.Option)

def showPath():
    #This one just shows the current path
    print(os.getcwd(), end='>')

#---List of functions to be used by other functions.

working_Functions = ['ls', 'man', 'cd', 'touch', 'rm', 'rmdir', 'mkdir', 'clear', 'mv', 'locate', 'cp']

wip_Functions = ['grep', 'cat']

#-------Show on launch---------

def show_about():
    #This will show the available commands at launch.
    print(Fore.GREEN + '2017-18 : developed by Deepjyoti Barman' + Style.RESET_ALL)
    print('Working functions are : ', end='')
    for func in working_Functions:
        print(Fore.CYAN + func, end=' | ')
    print(Style.RESET_ALL + '\n\nWork in progress functions are : ', end='')
    for func in wip_Functions:
        print(Fore.RED + func, end=' | ')
    print(Style.RESET_ALL + '\n\nTo know more about them use : man "command name"')
    input("press any Key when you are done.")
    os.system('cls')

#-------ERROR-------
#Below are definitions of errors to be shown.

#This is a dict that stores the param passed by function when they throw an unknown error. MAkes easier to debug. 
unknow_error_dict = {1 : 'is_available', 2 : 'mv', 3 : 'grep', 4 : 'rm', 5 : 'cat_singleFile', 6 : 'cp', 7 : 'showman'}

def noFile_error(Filename=''):
    #This function shows that Filename was not found.
    #End the exec of the function after calling this  function
    print(Fore.RED + Filename+" : Not Found\a" + Style.RESET_ALL)

def unknown_error(param):
    #param is used to know which function called this error
    print(Fore.RED + "\aSome unknown error occured. Err no : "+str(param)+"\nPlease take a look at the command syntax using 'man [COMMAND]'" + Style.RESET_ALL, end='')

def option_not_available(option, command):
    #This will show if the provided option is not found available for the command
    #End the exec of the function after calling this  function
    print(Fore.RED + option+"\a : No such option available in "+command+" command" + Style.RESET_ALL)

def unknown_command(cmd):
    #This will be called when an unknown command is passed  by the user
    print('\a' + cmd + Fore.RED + ' : No such command Available' + Style.RESET_ALL, end=' ')

#----------Error def end here------------

def give_rootPath():
    #This one returns the rootpath of the current working directory
    currentPath = os.getcwd()
    rootPath = currentPath[:currentPath.index("\\")] + "\\"
    return rootPath

def is_available(pathToFile):
    #This function checks if file or folder is available.
    #Return : True or False
    #Note : pathToFile can be a path to a file or just a file also.
    #Here we need to check three things.
    #If pathToFile is a folder or it is a path to a file within folders or just a file in the working directory. 
    #Try to see if it is a folder.
    try:
        if os.path.isdir(pathToFile) : 
            #It is a folder
            return True
    except:
        pass
        #If not a folder then try to see if it is a file within folders.
    try:
        file_Path = os.path.dirname(pathToFile) 
        #file_Path is the directory name where the file should be.
        file_Name = os.path.basename(pathToFile) 
        #file_Name is the files name
        #If pathToFile is just a filename without directories than file_Path is equal to ""
        if file_Path != "":
            if file_Name in os.listdir(file_Path) :
                #It is a file within folders
                return True
        else:
            if file_Name in os.listdir(os.getcwd()) :
                #It is a file in the working directory
                return True
            else:
                noFile_error(pathToFile)
                return False
    except:
        unknown_error(1)

def showman(command):
    #This shows the available functions in this terminal
    #The syntax is man [COMMAND NAME]
    #The command is passed to see which functions manual the user wants
    fun = {'cd':'Usage : cd [DIR NAME] \nUsed to change directory.',
    'ls':'Usage : ls [DIR NAME] -[OPTION] \nUsed to list a directory.',
    'touch':'Usage : touch [FILE NAME] \nUsed to create a new file.',
    'rm':'Usage : rm [FILE NAME] \nUsed to remove a file or folder.',
    'mkdir':'Usage : mkdir [DIR NAME]\nUsed to create a new directory.',
    'clear':'Usage : clear \nUsed to clear the screen.',
    'mv':'Usage : mv [SOURCE] [DESTINATION] \nUsed to move a file from SOURCE to DESTINATION',
    'cat':'Usage : cat [OPTION] [FILENAME] \nUsed to ',
    'locate' : 'Usage : locate [FILENAME] \nUsed to locate a file in the working Drive.\nNOTE : Make sure not to try on the drive where Windows is installed since there is lack of permission.',
    'grep' : 'Usage : grep [OPTION] "KEYWORD" [FILENAME]. \nUsed to find keyword in the given file.',
    'rmdir' : 'Usage : rmdir [DIRECTORY NAME]\n Used to remove directories.',
    'cp' : 'Usage : cp [SOURCE] [DESTINATION]\n Used to Copy files or folders', 
    }
    #fun is a dictionary. [Functio Name] : [Command Name]
    #It should be updated after adding a working function
    try:
        whichFun = command[4:]
        if whichFun in working_Functions:
            print(Fore.GREEN + fun[whichFun] + Style.RESET_ALL)
        elif whichFun in wip_Functions:
            print(Fore.RED + 'This command is still being worked on!\a' + Style.RESET_ALL)
            print(Fore.CYAN + fun[whichFun] + Style.RESET_ALL)
        else:
            print("\nPlease enter a valid Command\a. The Syntax is man [COMMAND NAME]", end='')
        '''print(fun[whichFun], end='')
        if whichFun == 'cat':
            print("\nOPTIONS are : ", end='')
            for i in range(len(available_Options_cat)):
                print(available_Options_cat[i], end='  ')
        elif whichFun == 'grep':
            print("\nOPTIONS are : ", end='')
            for i in range(len(available_Options_grep)):
                print(available_Options_grep[i], end='  ')'''
    except:
        unknown_error(7)

#------COMMANDS--------
#Below is the definition of all the commands.

#Locate functions all def start here
def Show(pathtoLaunch):                   
    exitFlag = True   
    input("Found in " + pathtoLaunch)
    main()

def List(pathToSearch, fileTofind):
    for files in os.listdir(pathToSearch):
        if files == fileTofind:
            Show(pathToSearch)
        else :
            try:
                if os.path.isdir(pathToSearch + files) and files != "System Volume Information" :
                    thread = myThread(pathToSearch + files + "\\", fileTofind)
                    thread.start()
                    thread.join()
            except:
                pass

def locate(details):
    #The function to search files
    #Right Now it doesn't function the way locate works in Linux. Needs improvisation.
    #For Now syntax is locate [File to Find]
    try:
        fileName = details[7:]
        List(give_rootPath(), fileName)
    except:
        print("Please Follow the syntax", end='')

#Ends here

def cd(command):
    #The change directory command.
    if command[:2] == "..":
        #Find dirname of currentPath
        os.chdir(os.path.dirname(os.getcwd()))
    elif command[:2] == "--":
        #If -- is present then we want to move to the root of the working directory path
        os.chdir(give_rootPath())
    else:
        newPath = command
        if os.path.isdir(newPath):
            os.chdir(newPath)
        else:
            print(newPath+": No such directory found\a", end='')

#----------ls command-----------

#This list will contain all the executable files in windows to show them with a green accent in terminal
executables = ['py', 'exe', 'msi', 'bat']

#This will be the list pof available options in ls used to check if the option is valid or not
options_in_ls = ['l', 'r', 't']

def grab(cmd):
    #This should grab all the extra options.
    #The ls command should be like this ls -[OPTIONS][OPTIONS]
    #So it will search for all the valid options after the '-' sign
    folder = os.getcwd()
    if len(cmd) > 2:
        try:
            flag = False
            posSpace_ls = cmd.index(' ')
            try:
                posSign_ls = cmd.index('-')
                if posSign_ls - posSpace_ls > 1:
                    flag = True
            except:
                #If the execution comes here then prob there was no '-' in the command
                tempFolder = cmd[posSpace_ls+1:len(cmd)]
            if flag:
                #If flag happens to be true then probably we need to name tempFolder
                tempFolder = cmd[posSpace_ls+1:posSign_ls-1]
            #Since we have tempFolder now, just check if the folder is available or not
            if os.path.isdir(tempFolder):
                folder = tempFolder
            else:
                print(tempFolder+" : No such directory found\a")
                return False
        except:
            pass
    #Above checks if any directory is passed as argue then it exists or not.
    try:
        opt = cmd[cmd.index('-')+1:]
        try:
            for single_options in opt:
                if single_options in options_in_ls:
                    disp(folder, single_options)
                    return True 
        except:
            option_not_available(opt, 'ls')
    except:
        disp(folder)

def disp(folder, option = ' '):
    #This will display.
    #It will do the final task of displaying.
    end_option = ' '
    #files in folder will be the list of files in the folder
    files_inFolder = os.listdir(folder)
    if option == 'l':
        end_option = '\n'
    if option == 'r':
        files_inFolder =  files_inFolder[::-1]
    for files in files_inFolder:
        if os.path.isdir(folder + '\\' + files):
            #If its a directory then print in blue
            print(Fore.BLUE + files + Style.RESET_ALL, end=end_option)
        else :
            #Check if its an exec file
            flag  = False
            for ext in executables:
                if files.endswith(ext):
                    flag = True
                    print(Fore.GREEN + files + Style.RESET_ALL, end= end_option)
                    break
            if not flag :
                print(files, end= end_option)

#-----ls ends here-------

def touch(nameOfFile):
    #Makes a new file.
    make = open(nameOfFile, "w")
    make.close()

def rm(fileName):
    #Remove command.
    try:
        if fileName[1:4] == "-rf":
            if is_available(fileName[5:]):
                shutil.rmtree(fileName[5:])
            else:
                noFile_error(fileName[5:])
        elif fileName[:3] == 'dir':
            if is_available(fileName[4:]):
                shutil.rmtree(fileName[4:])
        elif is_available(fileName[1:]):
            if os.path.isdir(fileName[1:]):
                counter  = 0
                for files in os.listdir(fileName[1:]):
                    if counter > 0 or not files:
                        break
                    counter += 1
                if counter > 0:
                    print("\a Folder is not empty!", end='')
                else:
                    os.rmdir(fileName[1:])
            else:
                os.remove(fileName[1:])
        else:
            noFile_error()
    except:
        unknown_error(4)

def MakeDir(name):
    #Makes a new folder.
    #Before making we need to check if existing directory with same name is available.
    #MAYBE we can do that by try
    try:
        os.mkdir(name)
    except:
        print("\aERROR : Directory with same name exists.", end='')

def clear():
    #Clears the screen.
    os.system("cls")

def mv(names):
    #Moves the file to the said directory.
    #Heres a catch. Damn it!
    #We need to know if where we need to move is a dir name or just a filename.
    #Coz if its just a file name, we need not check if it exists. 
    posSpace = names.index(" ")
    try:
        fileToMove = os.getcwd()+"\\"+names[:posSpace]  #The path to the file to be moved.
    except:
        print("\aPlease follow the syntax of command.", end='')
        return False
    if not is_available(fileToMove):
        return False
    whereToMove = names[posSpace+1:]                #The path where it is to be moved. 
    #whereToMove can be just a file name too. So lets just try to check if its a dir.
    #If not a dir, then probably a filename.
    try:
        #This will try to see if where to move has a dir name in it.
        #If it does then it will check if its a dir by calling is_available()
        if os.path.dirname(whereToMove) != "" :
            if not is_available(os.path.dirname(whereToMove)):
                return False
    except:
        pass
    #If it got past above then probably the source and destination are available
    try:
        shutil.move(fileToMove, whereToMove)
    except:
       unknown_error(2)
 
#--------cat-------------
#Definition of all functions used for cat start here. 

available_Options_cat = ['-n', '-e', '-T', ]

def checkCat(name):
    #The cat commnad.
    #This function just checks the options. The main function would be done by the following cat_exec() function. 
    #The syntax is cat -[OPTION] [FILE]...
    #We can make the OPTION default to read which will read and display the contents of the file
    #We need to make a list of options available to check if the passed option is valid.
    #If its not a valid option then pass the option to file name and see if the file exists in the working directory
    #This will be like the executor.
    #It will send the name to be checked if it is for single file or multiple files
    Option = cat_singleFile(name)
    if Option == 0:
        return False
    if not Option:
        Option = cat_doubleFiles(name)
        if not Option:
            option_not_available('','cat')
            return False
    return True
            

def cat_singleFile(name):
    #This will check if the command is for single files
    #If it is then it will be sent to cat_exec() to be executed
    #RETURNS : TRUE OR FALSE OR 0 if the option is -[] type but not available in the list
    Option = ''
    File = ''
    try:
        #Try to find the - in the passed argue which is name
        if name[0] == '-' :
            Option = name[:2]
            if Option not in available_Options_cat:
                option_not_available(Option, 'cat')
                return 0
            File = name[3:]
            cat_exec(Option, File)
            return True
        else:
            #If Options not in available Options list then theres a possibility that it is just a command to read the file
            #Or something like cat >name : we need to create name in this case
            #First lets check if its a > cat command
            if name[0] == '>':
                cat_exec('m', name[1:])
                return True
            elif '>' not in name and '<' not in name:
                print("Entered")
                if is_available(name):
                    cat_exec('', name)
                    return True
    except:
        unknown_error(5)

def cat_doubleFiles(name):
    #This will check name for stuff like file1 > file2 or file1 >> file2 or file1 < file2
    File = ''
    File2 = ''
    try:
        if '>' in name or '<' in name:
            #There's a possibility its a two file operation
            try:
                pos = name.index('>')
                #If > is not there then it will give error so it is in try
                if name[pos+1] == '>':
                    #We need to append file1 to file2
                    File = name[:pos-1]
                    File2 = name[pos+3:]
                    cat_exec('>>', File, File2)
                    return True
                else:
                    #We need to overwrite file2 and put file1 stuff in there
                    File = name[:pos-1]
                    File2 = name[pos+2:]
                    cat_exec('>', File, File2)
                    return True
            except:
                #Here we should try to see if it is the < command
                pass
    except:
        pass

def cat_exec(Option, File1, File2 = ''):
    if Option != 'm':
        open_the_File = open(File1, "r")
    if File2 != '':
        if Option == '>>':
            open_File2 = open(File2, 'a')
        elif Option == '>':
            open_File2 = open(File2, 'w')
    countLine = 0
    while True:
            if Option != 'm':
                readLine = open_the_File.readline()
                if not readLine:
                    break
            if Option == '-n':
                countLine += 1
                print(str(countLine)+" "+readLine, end='')
            elif Option == "-e":
                if readLine == " ":
                    print("$", end='')
                else:
                    print(readLine[:len(readLine)-1]+"$", end='\n')
            elif Option == "-T":
                '^I'.join(readLine.split())
                print(readLine, end='')
            elif Option == '':
                print(readLine, end='')
            elif Option == 'm':
                touch(File1)
                return True
            elif Option == '>' or Option == '>>':
                open_File2.write(readLine)
    open_the_File.close()    

#Definition ends here.

def openFile(name):
    #This one opens a file after checking if the file is available in the working directory and is not a folder
    fileAvailable = False
    for files in os.listdir(os.getcwd()):
        if name == files and not(os.path.isdir(files)):
            fileAvailable = True
            break
    if not fileAvailable:
        noFile_error(name)
    else:
        os.startfile(name)

#-------cp---------
def cp(name):
    #This function will work similar to cp.
    #We need to extract the source and destination from from name
    posSpace = name.index(" ")
    #The source and destination should be seperated by a spcace
    is_dir = False
    try:
        src = name[:posSpace]
        #Now check if src exists or not.
        if is_available(src):
            #So it exists. Now we nned to check if its a file or folder.
            if os.path.isdir(src):
                is_dir = True
        #Now we need to check destination
        dst = name[posSpace+1:]
        if is_dir:
            if not is_available(os.path.dirname(dst)):
                MakeDir(os.path.dirname(dst))
            shutil.copytree(src, dst)
        else:
            #We need to check if the directory of dst exists or not
            if not is_available(os.path.dirname(dst)):
                MakeDir(os.path.dirname(dst))
            shutil.copy(src, dst)
    except:
        unknown_error(6)

#-------grep---------

available_Options_grep = ['', '-n', '-v', '^', '$', '-c']
extension_of_Files_tosearch = ['txt', 'html', 'py',]

def grep(command):
    #This function will work like the grep command.
    #The syntax is grep [OPTION] "[string to find]" [FILENAME]
    #If no FILENAME is provided, it will search the root directory of the working path. 
    Option = ''
    try:
        pos = command.index('"')
        if pos != 0:
            Option = command[:pos-1]
        if Option not in available_Options_grep:
            option_not_available(Option, "grep")
            return False
        file_name = command[-command[::-1].index('"')+1:]
        if file_name != 'file*.*':
            if not is_available(file_name):
                noFile_error(file_name)
                return False
        #If file_name == file*.* then we need to check all files with extensions in extension_of_Files_tosearch 
        #Now that we have the file we want to search and the option
        keyword = command[command.index('"')+1:-1-command[::-1].index('"')]
        #We need to check if start of keyword has ^ or end has $
        if keyword[0] == '^':
            #We need to show only the ones that begin with keyword. 
            Option = '^'
            keyword = keyword[1:]
        elif keyword[len(keyword)-1] == '$':
            #We need to show only the ones that end with keyword. 
            Option = '$'
            keyword = keyword[:-1]
        grep_exec(Option, file_name, keyword)
        #Now we have the kewyword too.
    except:
        unknown_error(3)
        return False

def grep_exec(Option, fileName, keyword):
    #This will execute the grep command
    if fileName != 'file*.*':
        find_in_File(fileName, keyword, Option)
    else:
        for i in range(len(extension_of_Files_tosearch)):
            find_in_all_readable(keyword, extension_of_Files_tosearch[i], give_rootPath(), Option)

def find_in_File(file, keyword, conditions = ''):
    #This will find keyword in file
    open_File = open(file, 'r')
    print("Finding in "+file, end=':\n')
    countLine = 0
    countmatch = 0
    while True:
        read_word = open_File.readline()
        if not read_word:
            return True
        if conditions == '-n':
            countLine += 1
            if keyword in read_word:
                print(str(countLine)+" "+read_word, end='')
        elif conditions == '-v':
            if keyword not in read_word:
                print(read_word, end='')
        elif conditions == '^':
            if read_word[:len(keyword)] == keyword:
                print(read_word, end='')
        elif conditions == '$':
            if read_word[-len(keyword):] == keyword:
                print(read_word, end='')
        elif conditions == '-c':
            if keyword in read_word:
                countmatch += 1
                print("Match : "+str(countmatch)+" "+read_word, end='')
        else:
            if keyword in read_word:
                print(read_word, end='')

def find_in_all_readable(keyword, extension, path, Option = ''):
    #This will find the keyword in all files with given extension
    for stuff in os.listdir(path):
        if os.path.isdir(stuff) and stuff != "System Volume Information":
            thread = grepThread(keyword, extension, path+"\\"+stuff, Option)
            thread.start()
            thread.join()
        else:
            if stuff.endswith(extension):
                find_in_File(path+"\\"+stuff, keyword, Option)

#------COMMANDS/----------
#The function list ends here.

def runCommand(cmd):
    #This function checks the command and sends it to be executed. 
    if cmd == "exit":
        return 0
    elif cmd[:2] == "ls":
        grab(cmd)
    elif cmd[:6] == "locate":
        locate(cmd)
    elif cmd[:3] == "man":
        showman(cmd)
    elif cmd[:2] == "cd":
        cd(cmd[3:])
    elif cmd[:5] == "touch":
        touch(cmd[6:])
    elif cmd[:2] == "rm":
        rm(cmd[2:])
    elif cmd[:5] == "mkdir":
        MakeDir(cmd[6:])
    elif cmd[:5] == "clear":
        clear()
    elif cmd[:2] == "mv":
        mv(cmd[3:])
    elif cmd[:3] == "cat":
        checkCat(cmd[4:])
    elif cmd[:4] == 'grep':
        grep(cmd[5:])
    elif cmd[:2] == 'cp':
        cp(cmd[3:])
    else:
        openFile(cmd)

show_about()
def main():
    while True:
        showPath()
        prompt = input()
        ret = runCommand(prompt)
        print("")
        if ret == 0:
            break

main()