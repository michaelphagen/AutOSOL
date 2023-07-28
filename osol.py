# This app will look at the EA Desktop database and create an OSOL.ini file for each game, along with a manifest that can be digested by Steam Rom Manager
import os
import xml.etree.ElementTree as ET
from folder import searchExe
import urllib.request
import zipfile

def getEAExecutable(dir,game):
    # Looks for executable matching the title of the game using the _Installer xml, the 
    # Check for _Installer xml
    if os.path.isfile(os.path.join(dir,"__Installer","installerdata.xml")):
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
    # Look in the various folders for the game
    executable=searchExe(dir,game)
    if executable:
        print("Found executable: "+executable)
        return executable
    else:
        print("No executable found for "+game)
        return False
    
def downloadOSOL():
    # Download OSOL from https://api.github.com/repos/WombatFromHell/OriginSteamOverlayLauncher/releases/latest
    with urllib.request.urlopen('https://api.github.com/repos/WombatFromHell/OriginSteamOverlayLauncher/releases/latest') as f:
        #decode as json
        html = f.read().decode('utf-8')
    #split by "browser_download_url"
    html = html.split("browser_download_url")
    #split by " and take the second part
    html = html[1].split("\"")
    #get the url
    url = html[2]
    print("Downloading: "+url)
    #download the file
    urllib.request.urlretrieve(url, "OSOL.zip")
    # Unzip OSOL.zip
    with zipfile.ZipFile("OSOL.zip", 'r') as zip_ref:
        zip_ref.extractall("OSOL")
    # Delete OSOL.zip
    os.remove("OSOL.zip")
    # Download ini file from https://raw.githubusercontent.com/michaelphagen/Steam-Rom-Manager-Helper/main/OSOL/OriginSteamOverlayLauncher.ini
    urllib.request.urlretrieve('https://raw.githubusercontent.com/michaelphagen/Steam-Rom-Manager-Helper/main/OSOL/OriginSteamOverlayLauncher.ini',"OriginSteamOverlayLauncher.ini")
    # Move ini file to OSOL folder
    os.replace("OriginSteamOverlayLauncher.ini",os.path.join(os.getcwd(),"OSOL","OriginSteamOverlayLauncher.ini"))

def createOSOLConfig(game, EADesktopPath):
    eaDesktop=os.path.join(EADesktopPath,"EADesktop.exe")
    # Check that EA desktop exe exists
    if not os.path.isfile(eaDesktop):
        print("EA Desktop not found in "+EADesktopPath)
        # Check if it's in EADesktopPath/EA Desktop/EADesktop.exe
        if os.path.isfile(os.path.join(EADesktopPath,"EA Desktop","EADesktop.exe")):
            print("EA Desktop path was wrong, found in "+os.path.join(EADesktopPath,"EA Desktop","EADesktop.exe"))
            eaDesktop=os.path.join(EADesktopPath,"EA Desktop","EADesktop.exe")
    if not os.path.exists(os.path.join(os.getcwd(),"OSOL",game["title"])):
        print("Creating folder: "+os.path.join(os.getcwd(),"OSOL",game["title"]))
        os.makedirs(os.path.join(os.getcwd(),"OSOL",game["title"]))
        # Copy OriginSteamOverlayLauncher.ini from OSOL folder to game folder
    if not os.path.isfile(os.path.join(os.getcwd(),"OSOL","OriginSteamOverlayLauncher.ini")):
        downloadOSOL()
    with open(os.path.join(os.getcwd(),"OSOL","OriginSteamOverlayLauncher.ini"), 'r') as file:
        # Confirm OriginSteamOverlayLauncher.exe exits
        if not os.path.isfile(os.path.join(os.getcwd(),"OSOL","OriginSteamOverlayLauncher.exe")):
            downloadOSOL()
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

