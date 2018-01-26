import os
import string
import threading

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
    def __init__(self, keyword, extension, path):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.extension = extension
        self.path = path
    def run(self):
        find_in_all_readable(self.keyword, self.extension, self.path)

def showPath():
    #This one just shows the current path
    print(os.getcwd(), end='>')

#-------ERROR-------
#Below are definitions of errors to be shown.

def noFile_error(Filename):
    #This function shows that Filename was not found.
    #End the exec of the function after calling this  function
    print(Filename+" : Not Found\a")

def unknown_error(param):
    #param is used to know which function called this error
    print("\aSome unknown error occured. Err no : "+str(param)+"\nPlease take a look at the command syntax using 'man [COMMAND]'", end='')

def option_not_available(option, command):
    #This will show if the provided option is not found available for the command
    #End the exec of the function after calling this  function
    print(option+"\a : No such option available in "+command+" command")

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
    'ls':'Usage : ls [DIR NAME] \nUsed to list a directory.',
    'touch':'Usage : touch [FILE NAME] \nUsed to create a new file.',
    'rm':'Usage : rm [FILE NAME] \nUsed to remove a file or folder.',
    'mkdir':'Usage : mkdir [DIR NAME]\nUsed to create a new directory.',
    'clear':'Usage : clear \nUsed to clear the screen.',
    'mv':'Usage : mv [SOURCE] [DESTINATION] \nUsed to move a file from SOURCE to DESTINATION',
    'cat':'Usage : cat [OPTION] [FILENAME] \nUsed to ',
    'locate' : 'Usage : locate [FILENAME] \nUsed to locate a file in the working Drive.\nNOTE : Make sure not to try on the drive where Windows is installed since there is lack of permission.',
    'grep' : 'Usage : grep [OPTION] "KEYWORD" [FILENAME]. \nUsed to find keyword in the given file.',
    }
    #fun is a dictionary. [Functio Name] : [Command Name]
    #It should be updated after adding a working function
    try:
        whichFun = command[4:]
        print(fun[whichFun], end='')
    except:
        print("Please enter a valid Command\a. The Syntax is man [COMMAND NAME]", end='')

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

def ls(cmd):
    #The list directory command.
    folder = os.getcwd()
    if len(cmd) > 2:
        try:
            tempFolder = cmd[3:]
            if os.path.isdir(tempFolder):
                folder = tempFolder
            else:
                print(tempFolder+" : No such directory found\a")
                return False
        except:
            pass
    printCount = 0
    #printCount is just to keep track of printing so that the output doesnt look messy
    for files in os.listdir(folder):
        if printCount == 4 :
            print("")
            printCount = 0
        print(files, end=' ')
        printCount += 1

def touch(nameOfFile):
    #Makes a new file.
    make = open(nameOfFile, "w")
    make.close()

def rm(fileName):
    #Remove command.
    if fileName[:3] == "-rf":
            os.remove(fileName[4:])
    else:
        if os.path.isdir(fileName):
            counter  = 0
            for files in os.listdir(fileName):
                if counter > 0 or not files:
                    break
                counter += 1
            if counter > 0:
                print("\a Folder is not empty!", end='')
        else:
            if is_available(fileName):
                os.remove(fileName)
            else:
                noFile_error(fileName)

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
        os.rename(fileToMove, whereToMove)
    except:
       unknown_error(2)
 
#--------cat-------------
#Definition of all functions used for cat start here. 

def checkCat(name):
    #The cat commnad.
    #NOTE Some Options of cat has to be reworked. Will work on it tommorow.
    #This function just checks the options. The main function would be done by the following cat_exec() function. 
    #The syntax is cat [OPTION] [FILE]...
    #We can make the OPTION default to read which will read and display the contents of the file
    #We need to make a list of options available to check if the passed option is valid.
    #If its not a valid option then pass the option to file name and see if the file exists in the working directory
    available_Options_cat = ['n', 'e', 'T', 'r', 'm', 'a', 'w']
    Option = "r"
    File = ""
    File2 = ' '
    posSpace = -1
    while True:
        try:
            try:
                #We need to put this in Try because if no option is added it will show error
                #But no option means we just need to read the file
                posSpace = name.index(" ") 
                Option = name[1:posSpace]
            except:
                #If it failed in try then check if a new file should be created, i:e if ><filename> is passed
                try:
                    if name[0] == '>' : 
                        #Probably a new file should be made.
                        Option = 'm'
                        File = name[1:]
                        break 
                    else:
                        #If it enters here then we need to check for cat [Filename] > [Filename]
                        try:
                            if '>' in name:
                                pos = name.index('>')
                                if name[pos+1] == '>':
                                    #This means we need to append
                                    Option = 'a'
                                    File = name[:pos-1]
                                    File2 = name[pos+3:]
                                else:
                                    #This means we need to overwrite stuff in File2 with what is in File1
                                    Option = 'w'
                                    File = name[:pos-1]
                                    File2 = name[pos+2:]
                            if not is_available(File2):
                                noFile_error()
                                return False
                        except:
                            unknown_error(3)
                            return False
                except:
                    unknown_error(3)
                    return False
            if Option not in available_Options_cat:
                option_not_available(Option, "cat")
                return False
            File = name[posSpace+1:]
        except:
            pass
        if not is_available(File):
                noFile_error(File)
                return False
        cat_exec(Option, File, File2)
        break

def cat_exec(Option, File1, File2 = " "):
    openMode = {'w':'w', 'a':'a'}
    open_the_File = open(File1, "r")
    countLine = 0
    while True:
            readLine = open_the_File.readline()
            if not readLine:
                break
            if Option == "n":
                countLine += 1
                print(str(countLine)+" "+readLine, end='')
            elif Option == "e":
                if readLine == " ":
                    print("$", end='')
                else:
                    print(readLine[:len(readLine)-1]+"$", end='\n')
            elif Option == "T":
                '^I'.join(readLine.split())
                print(readLine, end='')
            elif Option == 'r':
                print(readLine, end='')
            elif Option == 'm':
                touch(File1)
            elif Option == 'a' or Option == 'w':
                open_File2 = open(File2, openMode[Option])
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
        print(name+" : No such file found\a")
    else:
        os.startfile(name)

#-------grep---------

available_Options_grep = ['', '-n', '-v', '^', '$']
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
        unknown_error(4)
        return False

def grep_exec(Option, fileName, keyword):
    #This will execute the grep command
    if Option == '':
        if fileName != 'file*.*':
            find_in_File(fileName, keyword)
        else:
            for i in range(len(extension_of_Files_tosearch)):
                find_in_all_readable(keyword, extension_of_Files_tosearch[i], give_rootPath())
    elif Option == '-n' or Option == '-v' or Option == '^' or Option == '$':
        find_in_File(fileName, keyword, Option)

def find_in_File(file, keyword, conditions = ''):
    #This will find keyword in file
    open_File = open(file, 'r')
    print("Finding in "+file, end=':\n')
    countLine = 0
    while True:
        read_word = open_File.readline()
        if not read_word:
            return True
        if conditions == '-n':
            countLine += 1
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
        else:
            if keyword in read_word:
                print(read_word, end='')

def find_in_all_readable(keyword, extension, path):
    #This will find the keyword in all files with given extension
    for stuff in os.listdir(path):
        if os.path.isdir(stuff) and stuff != "System Volume Information":
            thread = grepThread(keyword, extension, path+"\\"+stuff)
            thread.start()
            thread.join()
        else:
            if stuff.endswith(extension):
                find_in_File(path+"\\"+stuff, keyword)

#------COMMANDS/----------
#The function list ends here.

def runCommand(cmd):
    #This function checks the command and sends it to be executed. 
    if cmd == "exit":
        return 0
    elif cmd[:2] == "ls":
        ls(cmd)
    elif cmd[:6] == "locate":
        locate(cmd)
    elif cmd[:3] == "man":
        showman(cmd)
    elif cmd[:2] == "cd":
        cd(cmd[3:])
    elif cmd[:5] == "touch":
        touch(cmd[6:])
    elif cmd[:2] == "rm":
        rm(cmd[3:])
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
    else:
        openFile(cmd)

def main():
    while True:
        showPath()
        prompt = input()
        ret = runCommand(prompt)
        print("")
        if ret == 0:
            break

main()