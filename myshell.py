#!/usr/bin/env python3.7

# A python shell written by Adam Conway. Commands not natively understood are piped to the system and the output is sent back to our shell. The help command requires a readme to be stored in the same folder as the program.

from cmd import Cmd
import os
import sys
import subprocess
import time

shell = os.getcwd()

class MyPrompt(Cmd):

    intro = "Welcome! Type help to get help."
    #creates an environment variable called SHELL and assigns the current working directory at launch/myshell
    os.environ['SHELL'] = shell+'/myshell'

    #Reads the HOME environemnt variable, gets the current working directory and compares them. If the current working directory
    #equals or contains the home path, then it substitutes that part of the path for a ~, as is standard Linux. If it doesn't
    #find a match, then it just displays the username, machine name and working directory.
    if os.environ['HOME'] == os.getcwd()[0:len(os.environ['HOME'])]:
        prompt = '{}@{}:~{} $ '.format(os.environ['USER'], os.uname()[1], os.getcwd()[len(os.environ['HOME']):])
    
    else:
        prompt = '{}@{}:{} $ '.format(os.environ['USER'], os.uname()[1], os.getcwd())

    def default(self, args):
        a = args.split()

        check = os.path.isfile(a[0])
        
        #If the file exists and length of the input is greater than 1, we run this function.
        if check and (len(a) > 1):
        	#Checking if the user input has an output redirection symbol
            for i in range(0, len(a[:-1])):
                if a[i] == ">":
                    try:
                    	#Creating an overwrite function made it easier for output redirection on commands that don't exist in our shell.
                        overwrite(a[:i], a[i+1:], 0)
                    except IndexError:
                        print("Error no filename given")
                elif a[i] == ">>":
                    try: 
                    	#Creating an append function made it easier for output redirection on commands that don't exist in our shell.
                        append(a[:i], a[i+1], 0)
                    except IndexError:
                        print("Error no filename given")


        #If there is no input given after the command, then we just run it like any other.
        elif (len(a) == 0):                            
                try:
                	#Creating a process, assigning it to the value of p and piping the output of process "p" to the string "text", which we later print.
                    p = subprocess.Popen([args], shell=True, universal_newlines=True, stdout=subprocess.PIPE)
                    text = p.communicate()[0]
                    print(text)

                except FileNotFoundError as e:
                    print(e)
                    print("Error: No such command")

       	#If the last entry in our list "a" is an ampersand, then we run the command in the background.
        elif (a[-1] == "&"):
        	#We assign everything except for the ampersand to our string "b"
            b = " ".join(a[:-1])
            for i in range(0, len(a[:-1])):
                if a[i] == ">":
                    try:
                        overwrite(a[:i], a[i+1:])
                    except IndexError:
                        print("Error no filename given")
                elif a[i] == ">>":
                    try: 
                        append(a[:i], a[i+1])
                    except IndexError:
                        print("Error no filename given")
             
                else:
                    #If there is no output redirection, we run the program in the background anyway.
                    try:
                        p = subprocess.Popen([b], shell=True, universal_newlines=True, stdout=subprocess.PIPE)

                    except FileNotFoundError as e:
                        print(e)
                        print("Error: No such command")

        #Any other condition a file can be launched. This should never be called, but it's kept in just in case there are edge cases.
        else:
            try:
                p = subprocess.Popen([args], shell=True, universal_newlines=True, stdout=subprocess.PIPE)
                text = p.communicate()[0]
                print(text)

            except FileNotFoundError:
                print("File does not exist")



    def do_quit(self, args):
        print ("Quitting.")
        raise SystemExit

    def help_quit(self):
        print("Exits the program.")

    def do_cd(self, args):


        a = args.split()

        #If the user doesn't enter an input, cd should just return the current working directory.
        if len(args) == 0:
            print("Current directory: " + os.getcwd())

        else:
            try:
                #We try to change the directory to the one provided. We check if we are in the home direcotry or not, in order to update the prompt correctly.
                os.chdir(args)

                if os.environ['HOME'] == os.getcwd()[0:len(os.environ['HOME'])]:
                    currDir = os.getcwd()[len(os.environ['HOME']):]
                    username = os.environ['USER']
                    sysname = os.uname()[1]
                    MyPrompt.prompt = '{}@{}:~{} $ '.format(username, sysname, currDir)
                else:
                    currDir = os.getcwd()
                    username = os.environ['USER']
                    sysname = os.uname()[1]
                    MyPrompt.prompt = '{}@{}:{} $ '.format(username, sysname, currDir)

            except FileNotFoundError:           
                print('Error: No such directory')
            except IndexError:
                print(os.getcwd())

    def help_cd(self):
        print("\nChanges the current working directory to a specified one. Using this without a parameter will tell you the current working directory.\n\nUsage: cd <directory>")

    def do_clr(self, args):
        #ANSI escape code
        print("\033[2J\033[H", end="")

    def help_clr(self):
        print("\nClears the screen.")

    def do_dir(self, args):
        #We save the current directory to a temporary variable that we will switch back to later.
        tmp = os.getcwd()

        a = args.split()

        #If the input is greaeter than 0, we save the directory to the first word of the directory string. Otherwise, we just change directory.

        if(len(args) > 0):
            direc = a[0]
        else:
            direc = os.getcwd()

        tmp = os.getcwd()

        print(direc)

        if args == "":
            os.chdir(direc)
            try:
                files = os.listdir()
                for name in files:
                    full_path = os.path.join(os.getcwd(), name)
                    print("Relative path: " + full_path) #Relative path
            except:
                print("No valid path")


        #If it's longer than a single input, then we check for output redirection.
        else:
            if (len(a) > 1):
                for i in range(0, len(a[:-1])):
                    if a[i] == ">":
                        try:
                            os.chdir(direc)
                            fh = open(os.path.join(tmp, a[i+1]), "w+")
                            files = os.listdir()
                            for name in files:
                                full_path = os.path.join(os.getcwd(), name)
                                fh.write("Relative path: " + full_path + "\n") #Relative path
                        except IndexError:
                            print("Error no filename given")
                    elif a[i] == ">>":
                        try:
                            os.chdir(direc)
                            fh = open(os.path.join(tmp, a[i+1]), "a")
                            files = os.listdir()
                            fh.write("\n")
                            for name in files:
                                full_path = os.path.join(os.getcwd(), name)
                                fh.write("Relative path: " + full_path + "\n") #Relative path
                        except IndexError:
                            print("Error no filename given")
            else:
                os.chdir(args)
                try:
                    files = os.listdir()
                    for name in files:
                        full_path = os.path.join(os.getcwd(), name)
                        print("Relative path: " + full_path) #Relative path
                except:
                    print("No valid path")
                
        #We change back to our previous directory.  
        os.chdir(tmp)
        print("Current directory: " + os.getcwd())

    def help_dir(self):
        print("\nLists the contents of a typed directory on screen.\n\nUsage: dir <directory>\n\nIf you do not enter a directory, then this command will default to the current one.")

    def do_environ(self, args):
        a = args.split()

        #Checking for output redirection or background execution of environ
        if (len(a) > 1):
            for i in range(0, len(a[:-1])):

                #Check for background execution
                if a[-1] == "&":
                    for i in range(0, len(a[:-1])):
                        if a[i] == ">":
                            try:
                                fh = open(a[i+1], "w+")
                                for item, value in os.environ.items():
                                    fh.write('{}: {}\n'.format(item, value))
                            except IndexError:
                                print("Error no filename given")
                        elif a[i] == ">>":
                            try:
                                fh = open(a[i+1], "a")
                                fh.write("\n")
                                for item, value in os.environ.items():
                                    fh.write('{}: {}\n'.format(item, value))
                            except IndexError:
                                print("Error no filename given")

                #Check for output redirection
                elif a[i] == ">":
                    try:
                        fh = open(a[i+1], "w+")
                        for item, value in os.environ.items():
                            fh.write('{}: {}\n'.format(item, value))
                    except IndexError:
                        print("Error no filename given")

                    for item, value in os.environ.items():
                        print('{}: {}'.format(item, value))

                elif a[i] == ">>":
                    try:
                        fh = open(a[i+1], "a")
                        fh.write("\n")
                        for item, value in os.environ.items():
                            fh.write('{}: {}\n'.format(item, value))
                    except IndexError:
                        print("Error no filename given")
                    
                    for item, value in os.environ.items():
                        print('{}: {}'.format(item, value))

        #No additional inputs, just run the environ command.
        elif (len(a) == 0):
            for item, value in os.environ.items():
                    print('{}: {}'.format(item, value))


    def help_environ(self):
        print("\nPrints the system environment variables to the screen.")

    def do_echo(self, args):

        a = args.split()


        #If nothing to echo, do nothing.
        if not a:
            pass

        #Background execution with output redirection for echo            
        elif(a[-1] == "&"):
            for i in range(0, len(a[:-1])):
                if a[i] == ">":
                    with open(a[i+1], "w+") as fh:
                        for j in range(0, len(a[:-3])):
                            fh.write("" + a[j]+ " ")

                if a[i] == ">>":
                    f = open(a[i+1], "a")
                    f.write("\n")
                    with open(a[i+1], "a") as fh:
                        for j in range(0, len(a[:-3])):
                            fh.write("" + a[j]+ " ")

        #Output redirection for echo

        elif(len(a) > 1):
            print(args)
            for i in range(0, len(a[:-1])):
                if a[i] == ">":
                    with open(a[i+1], "w+") as fh:
                        for j in range(0, len(a[:-2])):
                            fh.write("" + a[j]+ " ")

                if a[i] == ">>":
                    f = open(a[i+1], "a")
                    f.write("\n")
                    with open(a[i+1], "a") as fh:
                        for j in range(0, len(a[:-2])):
                            fh.write("" + a[j]+ " ")

        #Otherwise, just print

        else:
            print(args)

    def help_echo(self):
        print("\nRepeats an entered text back to you.")
                

    def do_pause(self, args):
        i = input()

    def help_pause(self):
        print("\nPauses input until the user presses the enter key.")

    def do_help(self, args):

        a = args.split()

        if(len(a) == 0):
            try:
                fh = open("readme", "r")
                j = 0
                for i in fh:
                    j += 1
                    print(i)
                    if(j % 20 == 0):
                        k = input()

            
            except IndexError:
                print("No manual found. Do you have a readme file?")

        elif(a[-1] == "&"):
            for i in range(0, len(a[:-1])):
                if a[i] == ">":
                    f = open(a[i+1], "w")
                    with open(a[i+1], "w+") as fh:
                        try:
                            fh = open("readme", "r")
                            j = 0
                            for l in fh:
                                j += 1
                                f.write(l)

                        except IndexError:
                            print("No manual found. Do you have a readme file?")

                elif a[i] == ">>":
                    f = open(a[i+1], "a")
                    f.write("\n")
                    with open(a[i+1], "a") as fh:
                        try:
                            fh = open("readme", "r")
                            j = 0
                            for l in fh:
                                j += 1
                                f.write(l)

                        except IndexError:
                            print("No manual found. Do you have a readme file?")

        elif(len(a) > 1):
            for i in range(0, len(a[:-1])):
                if a[i] == ">":
                    f = open(a[i+1], "w")
                    with open(a[i+1], "w+") as fh:
                        try:
                            fh = open("readme", "r")
                            j = 0
                            for l in fh:
                                j += 1
                                print(l)
                                f.write(l)
                                if(j % 20 == 0):
                                    k = input()

                        except IndexError:
                            print("No manual found. Do you have a readme file?")

                if a[i] == ">>":
                    f = open(a[i+1], "a")
                    f.write("\n")
                    with open(a[i+1], "a") as fh:
                        try:
                            fh = open("readme", "r")
                            j = 0
                            for l in fh:
                                j += 1
                                print(l)
                                f.write(l)
                                if(j % 20 == 0):
                                    k = input()
                        except IndexError:
                            print("No manual found. Do you have a readme file?")

    def emptyline(self):
        pass

        

def overwrite(procin, args):
    #We assign our process to the variable "p", which we can then pull the piped text output from and save it to a variable text.
    
    p = subprocess.Popen([procin[0]], shell=True, universal_newlines=True, stdout=subprocess.PIPE)
    text = p.communicate()[0]

    try:
        fh = open(args[0], "w+")
        fh.write(text)
        fh.write("\n")

    except IndexError:
        print("Usage: <command> > <filename>")

def append(procin, args):
    p = subprocess.Popen([procin[0]], shell=True, universal_newlines=True, stdout=subprocess.PIPE)
    text = p.communicate()[0]

    try:
        fh = open(args[0], "a")
        fh.write(text)
        fh.write("\n")

    except IndexError:
        print("Usage: <command> > <filename>")



if __name__ == '__main__':
    #Command line argument input for launching a program
    if len(sys.argv) > 1:
        try:
            fh = open(sys.argv[1], "r")
            fread = fh.readlines()
            #Run every line in the text file.
            for x in fread:
                subprocess.Popen([x], shell=True, universal_nxewlines=True)
                time.sleep(.2)
        except FileNotFoundError:
            print("No file input found")
        
    else:
        MyPrompt().cmdloop()
