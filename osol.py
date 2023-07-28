# This app will look at the EA Desktop database and create an OSOL.ini file for each game, along with a manifest that can be digested by Steam Rom Manager
import os
import xml.etree.ElementTree as ET
from folder import searchExe
from util import *

def getEAExecutable(dir,game):
    # Looks for executable matching the title of the game using the _Installer xml, the 
    # Check for _Installer xml
    if os.path.isfile(os.path.join(dir,"__Installer","installerdata.xml")):
        print("Found _Installer xml for "+game, "reading...")
        # Read the xml
        tree = ET.parse(os.path.join(dir,"__Installer","installerdata.xml"))
        root = tree.getroot()
        # Check for the game in either <DiPManifest><runtime><launcher>
        for child in root:
            if child.tag == "runtime":
                for child in child:
                    if child.tag == "launcher":
                        for child in child:
                            if child.tag == "filePath":
                                executable=child.text.split("Install Dir]")[1]
                                print("Found executable: "+executable)
                                return (dir+"\\"+executable)
    else:
        print("No _Installer xml for "+game)
    # Look in the various folders for the game
    executable=searchExe(dir,game)
    if executable:
        print("Found executable: "+executable)
        return executable
    else:
        print("No executable found for "+game)
        return False

def createOSOLConfig(game, EADesktopPath):
    eaDesktop=os.path.join(EADesktopPath,"EADesktop.exe") 
    if not os.path.exists(os.path.join(os.getcwd(),"OSOL",game["title"])):
        print("Creating folder: "+os.path.join(os.getcwd(),"OSOL",game["title"]))
        os.makedirs(os.path.join(os.getcwd(),"OSOL",game["title"]))
        # Copy OriginSteamOverlayLauncher.ini from OSOL folder to game folder
    print("Generating OSOL ini in "+os.path.join(os.getcwd(),"OSOL",game["title"]))
    with open(os.path.join(os.getcwd(),"OSOL","OriginSteamOverlayLauncher.ini"), 'r') as file:
        # Confirm OriginSteamOverlayLauncher.exe exits
        if not os.path.isfile(os.path.join(os.getcwd(),"OSOL","OriginSteamOverlayLauncher.exe")):
            print("OriginSteamOverlayLauncher.exe not found!")
            return False
        filedata = file.read()
        # Fill in LauncherPath= with eaDesktop
        filedata = filedata.replace("LauncherPath=", "LauncherPath="+eaDesktop)
        # Fill in GamePath= with game executable
        filedata = filedata.replace("GamePath=", "GamePath="+game["target"])
        # Write the file out again
        with open(os.path.join(os.getcwd(),"OSOL",game["title"],"OriginSteamOverlayLauncher.ini"), 'w') as file:
            file.write(filedata)
            # Add ini folder to game object
            game["startIn"]=os.path.join(os.getcwd(),"OSOL",game["title"])
            game["target"]=os.path.join(os.getcwd(),"OSOL","OriginSteamOverlayLauncher.exe")
    return game

