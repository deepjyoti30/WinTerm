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

rootpath = "E:\\"

def showPath():
    #This one just shows the current path
    print(os.getcwd(), end='>')

def isFile_available(fileName, path):
    #This function checks if fileName is available in the given path.
    #Return : True or False
    whole_dir_searched = False
    #This variable checks if the whole directory is searched. If still it is False then the file was not found in the path.
    path += "\\"
    if '\\' in path:
        try:
            iniPath = fileToMove[:len(fileToMove)-(fileToMove[::-1].index("\\"))]
            if not os.path.isdir(iniPath) :
                print(iniPath+" : No such directory found\a", end='')
                return False
        except:
            pass
    try:
        finPath = whereToMove[:len(whereToMove)-(whereToMove[::-1].index("\\"))]
        if not os.path.isdir(finPath):
            print(finPath+" : No such directory found\a", end='')
            return False
    except:
        pass
    try:
        for files in os.listdir(path):
            whole_dir_searched = True
            if files == fileName:
                return True
    except:
        return False
    if not whole_dir_searched: 
        return False

def noFile_error(Filename):
    #This function shows that Filename was not found and calls main after execution.
    print(Filename+" : Not Found\a", end='\n')
    main()

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
    'cat':'Usage : cat [OPTION] [FILENAME] \nUsed to '}
    #fun is a dictionary. [Functio Name] : [Command Name]
    #It should be updated after adding a working function
    try:
        whichFun = command[4:]
        print(fun[whichFun], end='')
    except:
        print("Please enter a valid Command\a. The Syntax is man [COMMAND NAME]", end='')

#Below is the definition of all the commands.

#Locate functions all def start here
def Show(pathtoLaunch):                   
    exitFlag = True   
    input("\t\tFound in " + pathtoLaunch)
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
            except:
                pass
    if threading.active_count() == 1:
        exitFlag = True
        input("\t\tFile Not Found!")

def locate(details):
    #The function to search files
    #Right Now it doesn't function the way locate works in Linux. Needs improvisation.
    #For Now syntax is locate [File to Find]
    try:
        fileName = details[7:]
        List(rootpath, fileName)
    except:
        print("Please Follow the syntax", end='')

#Ends here

def cd(command):
    #The change directory command.
    if command[:2] == "..":
        currentPath = os.getcwd()
        #Find if \ is present from end
        pos = currentPath[::-1].index("\\")
        newPath = currentPath[:len(currentPath) - pos]
        os.chdir(newPath)
    elif command[:2] == "--":
        os.chdir(rootpath)
    else:
        newPath = command
        if os.path.isdir(newPath):
            os.chdir(newPath)
        else:
            print(newPath+": No such directory found\a", end='')

def listDir(cmd):
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
    for files in os.listdir(folder):
        print(files, end=' ')

def touch(nameOfFile):
    #Makes a new file.
    make = open(nameOfFile, "w")
    make.close()

def rm(fileName):
    #Remove command.
    if fileName[:3] == "-rf":
            os.remove(cmd[4:])
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
            if isFile_available(fileName, os.getcwd()):
                os.remove(fileName)
            else:
                noFile_error(fileName)

def MakeDir(name):
    #Makes a new folder.
    os.mkdir(name)

def clear():
    #Clears the screen.
    os.system("cls")

def mv(names):
    #Moves the file to the said directory.
    posSpace = names.index(" ")
    fileToMove = os.getcwd()+"\\"+names[:posSpace]
    whereToMove = names[posSpace+1:]
    #Need to check if both directories exist.
    #Need to take the path out of fileToMove.
    try:
        iniPath = fileToMove[:len(fileToMove)-(fileToMove[::-1].index("\\"))]
        if not os.path.isdir(iniPath) :
            print(iniPath+" : No such directory found\a", end='')
            return False
    except:
        pass
    try:
        finPath = whereToMove[:len(whereToMove)-(whereToMove[::-1].index("\\"))]
        if not os.path.isdir(finPath):
            print(finPath+" : No such directory found\a", end='')
            return False
    except:
        pass
    #If the directories exist, we need to check if the said file is available
    try:
        File = ((fileToMove[::-1])[:-len(fileToMove)+(fileToMove[::-1].index("\\"))])[::-1]
        #flag is to check if the file is found in the given folder
        flag = False
        if isFile_available(File, iniPath):
            flag = True
    except:
        pass
    if flag:
        os.rename(fileToMove, whereToMove)
    else:
        noFile_error(fileToMove)

#Definition of all functions used for cat start here. 

def checkCat(name):
    #The cat commnad.
    #This function just checks the options. The main function would be done by the following cat_exec() function. 
    #The syntax is cat [OPTION] [FILE]...
    #We can make the OPTION default to read which will read and display the contents of the file
    #We need to make a list of options available to check if the passed option is valid.
    #If its not a valid option then pass the option to file name and see if the file exists in the working directory
    availableOptions = ['n', 'e', 'T', 'r']
    Option = "r"
    File = ""
    posSpace = -1
    while True:
        try:
            try:
                #We need to put this in Try because if no option is added it will show error
                #But no option means we just need to read the file
                posSpace = name.index(" ") 
                Option = name[1:posSpace]
            except:
                pass
            if Option not in availableOptions:
                print(Option+" : No such Option found in cat", end='')
                return False
            File = name[posSpace+1:]
            if not isFile_available(File, os.getcwd()):
                noFile_error(File)
                break
        except:
            pass
        cat_exec(Option, File)
        break

def cat_exec(Option, File1, File2 = " "):
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

#The function list ends here. Below is the main()

def runCommand(cmd):
    #This function executes the command
    if cmd == "exit":
        return 0
    elif cmd[:2] == "ls":
        listDir(cmd)
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