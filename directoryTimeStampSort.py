#
# Sort Directory By Timestamp by Matthew Relph
# v 1.00
# Python Script Version
#
#
# Taking a directory full of files, and putting them in folders based on the date of their last modification
# Works good for lots of things, logs, pictures, piles of HL7 pharmacy requests, you name it!
#
#
# Some error checking. Should stop and report to shell on any error
# As always, use at your own risk
#
# 1st Argument = Source Path
# 2nd Argument = Destination Path
# 3rd Argument = Option Flags
#
# Example use (Python Script in bash):
# python scriptName Source Destination -c -p -y -o

#
# Possible future additions:
# Filter by extension, relative paths, more error checking, Cross Platform testing

import shutil
import sys
import argparse
import os
import os.path
import time




def check_args(argsDict, statusDict):

    if (statusDict["debugFlag"]):
        print("Made it to the Check Args Function")
        print("This is the name of the script: ", sys.argv[0])
        print("Number of arguments: ", len(sys.argv))
        print("The arguments from sys.arg are: ", str(sys.argv))

    # Parse arguments
    parser = argparse.ArgumentParser(description='Reorganizes files by time stamp.')

    # Add optional switches
    parser.add_argument('sourcePath', action='store',
                        help='Source Directory')
    parser.add_argument('destinationPath', action='store',
                        help='Destination Directory')
    parser.add_argument('-c', action='store_false', dest='moveFlag',
                        help='Copy to new directory only (Leaves Originals)')
    parser.add_argument('-v', action='store_true', dest='moveFlag',
                        help='Move to new directory')
    parser.add_argument('-n', action='store_false', dest='promptFlag',
                        help='No prompts (overrides other options)')
    parser.add_argument('-p', action='store_true', dest='promptFlag',
                        help='Prompt at conflicts')
    parser.add_argument('-y', action='store_const', const='y', dest='sortBy',
                        help='Split By Year')
    parser.add_argument('-m', action='store_const', const='m', dest='sortBy',
                        help='Split By Month')
    parser.add_argument('-d', action='store_const', const='d', dest='sortBy',
                        help='Split By Day')
    parser.add_argument('-o', action='store_false', dest='noOverwriteFlag',
                        help='Default action is to overwrite on conflict')
    parser.add_argument('-x', action='store_true', dest='noOverwriteFlag',
                        help='Default action is to make a copy on conflict')
    args = parser.parse_args()  #Exits on error
    argsDict.update(args.__dict__.copy())   #Returns values to argsDict parameter
    if (statusDict["debugFlag"]):
        print("The arguments from argparse are: ", argsDict)

    #Test Input Directory
    if (argsDict["sourcePath"] != None):
        print("Source Path: ", argsDict["sourcePath"])
        if ((os.path.exists(argsDict["sourcePath"])) and (os.path.isdir(argsDict["sourcePath"]))):
            if (statusDict["debugFlag"]):
                print("\tSource Path Exists and is a Directory")
        else:
            print("\tNot a valid Source Path\n\tCannot Continue.")
            statusDict["continueFlag"] = False
    #Test Output Directory
    if (statusDict["continueFlag"] and (argsDict["destinationPath"] != None)):
        print("Destination Path: ", argsDict["destinationPath"])
        if ((os.path.exists(argsDict["destinationPath"])) and (os.path.isdir(argsDict["destinationPath"]))):
            if (statusDict["debugFlag"]):
                print("\tDestination Path Exists and is a Directory")
        else:
            print("\tNot a valid Destination Path")

            makeNewPathFlag = False
            if (argsDict["promptFlag"]):    #Prompt if user wants to create a new directory
                newPathPrompt = input("\tAttempt to create destination path? (y/n)  ")
                newPathPrompt.lower()
                if (newPathPrompt == "y"):
                    makeNewPathFlag = True
                else:
                    makeNewPathFlag = False
            elif (not (argsDict["noOverwriteFlag"])):
                makeNewPathFlag = True
            else:
                statusDict["continueFlag"] = False

            if (makeNewPathFlag):   #Attemp to make a new directory
                try:
                    os.makedirs(argsDict["destinationPath"])
                except OSError:
                    print("\tCreation of the directory %s failed. \n\tCannot Continue." % argsDict["destinationPath"])
                    statusDict["continueFlag"] = False
                else:
                    print("\tSuccessfully created the directory %s " % argsDict["destinationPath"])


    if (statusDict["continueFlag"] ):
        print("Options:")
        print("\tMove=", argsDict["moveFlag"])
        print("\tPrompt=", argsDict["promptFlag"])
        switcher = {"y": "Year", "m": "Month", "d": "Day"}
        print("\tSort By=", switcher.get(argsDict["sortBy"], "Year"))
        print("\tOverwrite=", (not (argsDict["noOverwriteFlag"])))
#End check_args

def main_task(argsDict, statusDict):
    if (statusDict["debugFlag"]):
        print("Made it to the Main Task")
    print("Preparing to copy...")
    # Get list of files in source directory - Files only, please
    fileCopyList = [f for f in os.listdir(argsDict["sourcePath"]) if os.path.isfile(os.path.join(argsDict["sourcePath"], f))]
    for file in fileCopyList:

        sourceFilePath = argsDict["sourcePath"] +"/" + file

        # Get last modified date of each file
        sourceFileMTime = os.path.getmtime(sourceFilePath)
        sourceFileDate = time.localtime(sourceFileMTime)
        sourceFileYear = time.strftime("%Y", sourceFileDate)
        sourceFileMonth = time.strftime("%m", sourceFileDate)
        sourceFileDay = time.strftime("%d", sourceFileDate)
        if (statusDict["debugFlag"] ):
            print("File Name: ", sourceFilePath)
            print(sourceFileYear, sourceFileMonth, sourceFileDay)

        # Get year string and append to path
        extendedDestinationPath = argsDict["destinationPath"] +"/" + sourceFileYear

        print(argsDict["sortBy"], extendedDestinationPath)
        if ((argsDict["sortBy"] == "m") or (argsDict["sortBy"] == "d")):
            # Append month to extended path depending on Sort By Choice
            extendedDestinationPath = extendedDestinationPath + "/" + sourceFileMonth
        print(argsDict["sortBy"], extendedDestinationPath)
        if (argsDict["sortBy"] == "d"):
            # Append day to extended path depending on Sort By Choice
            extendedDestinationPath = extendedDestinationPath + "/" + sourceFileDay
        print(argsDict["sortBy"], extendedDestinationPath)
        if (not (os.path.exists(extendedDestinationPath)) and  not (os.path.isdir(extendedDestinationPath))):
            # Lets create the new sort path if it doesn't exist
            try:
                os.makedirs(extendedDestinationPath)
            except OSError:
                print("\tCreation of the directory %s failed. \n\tCannot Continue." % extendedDestinationPath)
                statusDict["continueFlag"] = False
                break
            else:
                if (statusDict["debugFlag"] ):
                    print("\tSuccessfully created the directory %s " % extendedDestinationPath)
        # Set destination file location
        destinationFilePath = extendedDestinationPath + "/" + file
        # Now we check if the file exists, and determine what we need to do on conflict
        conflictFlag = False
        if (os.path.exists(destinationFilePath)):
            conflictFlag = True

        # If prompts are on, we check with the user on conflict
        overwriteNext = not argsDict["noOverwriteFlag"]
        if (conflictFlag and argsDict["promptFlag"] ):
            print("\tFile %s already exists" % destinationFilePath)
            conflictAction = input(", overwrite (o) or make a new copy(c) ? (o/c)  ")
            conflictAction.lower()
            if (conflictAction == "o"):
                overwriteNext = True
            else:
                overwriteNext = False
        # During conflict If we choose to copy, we make a new copy with a unique file name, otherwise we continue on and overwrite the file
        if (not overwriteNext and conflictFlag):
            fileVersion = 0
            while ((os.path.exists(destinationFilePath)) and (fileVersion<255)):    #We artificially limit the copies to 255, just in case
                destinationFilePath = extendedDestinationPath + "/(" + str(fileVersion) + ")" + file
                fileVersion += 1

        # Final file copy
        try:
            shutil.copy2(sourceFilePath, destinationFilePath)   # Use Copy2 to maintain modified date after copy
        except IOError as e:
            print("Unable to copy file. %s \nCannot Continue" % e)
            exit(1)
        except:
            print("Unexpected error: %s  \nCannot Continue" % sys.exc_info())
            exit(1)
        else:
            if (statusDict["debugFlag"]):
                print("\tSuccessfully copied to %s " % destinationFilePath)

    print("Copy Complete")

    # Remove source files if we are setup to move instead of just copy.
    # Only remove files from the list we copied (Some files may have been added since we started)
    if (argsDict["moveFlag"]):
        print("Removing Originals from Source Directory...")
        for removeFile in fileCopyList:
            removeFilePath = argsDict["sourcePath"] + "/" + removeFile
            try:
                os.remove(removeFilePath)
            except IOError as e:
                print("Unable to delete file. %s \nCannot Continue" % e)
                exit(1)
            except:
                print("Unexpected error: %s  \nCannot Continue" % sys.exc_info())
                exit(1)
            else:
                if (statusDict["debugFlag"]):
                    print("\tSuccessfully deleted %s " % removeFilePath)
        print("Removals Complete")
    print("Sorting Complete\nEnd Script")
# End main_task





# End of functions

# Begin main script
statusDict = {"debugFlag": False, "continueFlag": True}
argsDict = {}
check_args(argsDict, statusDict)
if (argsDict["promptFlag"] and statusDict["continueFlag"]):
    proceedPrompt = input("Continue with these options? (y/n)  ")
    proceedPrompt.lower()
    if (proceedPrompt == "n"):
        statusDict["continueFlag"] = False
        print("Cannot continue.")


if (statusDict["continueFlag"]):
    main_task(argsDict, statusDict)
else:
    print("\n")


