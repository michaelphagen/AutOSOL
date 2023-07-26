# This app will look at the EA Desktop database and create an OSOL.ini file for each game, along with a manifest that can be digested by Steam Rom Manager
import json
import os
import xml.etree.ElementTree as ET

# open config.ini
with open("config.ini", 'r') as file:
    #set global variables
    global EAGamesPath
    # Read the file
    filedata = file.read()
    # Fill in the EA Games Path
    EAGamesPath=filedata.split("EAGamesPath=")[1].split("\n")[0]
    print("EAGamesPath: "+EAGamesPath)
    # Fill in the EA Desktop Path
    global EADesktopPath
    EADesktopPath=filedata.split("EADesktopPath=")[1].split("\n")[0]

    print("EADesktopPath: "+EADesktopPath)

def findGames():
    # This function will look at the EA Desktop folder and will return a list of games that are installed
    # Create a list of games
    games = []
    for game in os.listdir(EAGamesPath):
        print("Found path, checking for executable: "+os.path.join(EAGamesPath,game))
        executable=isGame(os.path.join(EAGamesPath,game),game)
        if executable:
            print("in findGames, executable is: "+str(executable))
            games.append({"title":game,"executable":os.path.join(EAGamesPath,game),"executable":executable})
    print("Found "+str(len(games))+" games")
    return games

def isGame(dir,game):
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
    for folder in ["","__Installer","Installer","Game","Bin","bin","bin32","bin64","bin_x86","bin_x64"]:
        if os.path.isfile(os.path.join(dir,folder,game+".exe")):
            return os.path.join(dir,folder,game+".exe")
        # Look for game without spaces
        if os.path.isfile(os.path.join(dir,folder,game.replace(" ","")+".exe")):
            return os.path.join(dir,folder,game.replace(" ","")+".exe")
    return False

def createFolder(game):
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
        filedata = filedata.replace("GamePath=", "GamePath="+game["executable"])
        # Write the file out again
        with open(os.path.join(os.getcwd(),"OSOL",game["title"],"OriginSteamOverlayLauncher.ini"), 'w') as file:
            file.write(filedata)
            # Add ini folder to game object
            game["startIn"]=os.path.join(os.getcwd(),"OSOL",game["title"])
            game["target"]=os.path.join(os.getcwd(),"OSOL","OriginSteamOverlayLauncher.exe")
    return game

def createManifest(games):
    # Create Folders with Game title in OSOL directory within the current directory
    games=list(map(createFolder,games))
    # Create manifest
    with open(os.path.join(os.getcwd(),"manifest.json"), 'w') as file:
        file.write(json.dumps(games))
    return games



    
def sync():
    games=findGames()
    games=createManifest(games)
#Auto run
if __name__ == "__main__":
    sync()

        
        

        