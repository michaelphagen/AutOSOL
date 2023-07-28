import os
import json
from osol import *
from folder import *

def getVars():
   if not os.path.isfile("config.ini"):
    MonitorFolders=[""]
    EADesktopPath=""
    EAGamesPaths=[""]
    return MonitorFolders,EADesktopPath,EAGamesPaths
    #open config file to get vars
   with open("config.ini", 'r') as file:
    # Read the file
    filedata = file.read()
    # Fill in the EA Games Path
    MonitorFoldersString=filedata.split("MonitorFolders=")
    if len(MonitorFoldersString)>1:
        MonitorFolders=MonitorFoldersString[1].split("\n")[0].split(",")
    else:
        MonitorFolders=[""]
    EADesktopPathString=filedata.split("EADesktopPath=")
    if len(EADesktopPathString)>1:
        EADesktopPath=EADesktopPathString[1].split("\n")[0]
    else:
        EADesktopPath=""
    EAGamesPathsString=filedata.split("EAGamesPaths=")
    if len(EAGamesPathsString)>1:
        EAGamesPaths=EAGamesPathsString[1].split("\n")[0].split(",")
    else:
        EAGamesPaths=[""]
    return MonitorFolders,EADesktopPath,EAGamesPaths

def updateVars(variable,value):
    if not os.path.isfile("config.ini"):
        with open("config.ini", 'w') as file:
            file.write("MonitorFolders=\nEADesktopPath=\nEAGamesPaths=")
    #open config file to get vars
    with open("config.ini", 'r') as file:
        # Read the file
        filedata = file.read()
        # Fill in the EA Games Path
        if variable=="MonitorFolder":
            if "MonitorFolders=" in filedata:
            #if MonitorFolders value isn't empty
                if filedata.split("MonitorFolders=")[1].split("\n")[0]!="":
                    if value in filedata.split("MonitorFolders=")[1].split("\n")[0].split(","):
                        return getVars()
                    filedata=filedata.replace("MonitorFolders="+filedata.split("MonitorFolders=")[1].split("\n")[0],"MonitorFolders="+filedata.split("MonitorFolders=")[1].split("\n")[0]+","+value)
                else:
                    filedata=filedata.replace("MonitorFolders=","MonitorFolders="+value)
            else:
                filedata=filedata+"\nMonitorFolders="+value
        elif variable=="EADesktopPath":
            if "EADesktopPath=" in filedata:
            #if EADesktopPath value isn't empty
                if filedata.split("EADesktopPath=")[1].split("\n")[0]!="":
                    if value in filedata.split("EADesktopPath=")[1].split("\n")[0].split(","):
                        return getVars()
                    filedata=filedata.replace("EADesktopPath="+filedata.split("EADesktopPath=")[1].split("\n")[0],"EADesktopPath="+filedata.split("EADesktopPath=")[1].split("\n")[0]+","+value)
                else:
                    filedata=filedata.replace("EADesktopPath=","EADesktopPath="+value)
            else:
                filedata=filedata+"\nEADesktopPath="+value
        elif variable=="EAGamesPath":
            if "EAGamesPaths=" in filedata:
            #if EAGamesPaths value isn't empty
                if filedata.split("EAGamesPaths=")[1].split("\n")[0]!="":
                    if value in filedata.split("EAGamesPaths=")[1].split("\n")[0].split(","):
                        return getVars()
                    filedata=filedata.replace("EAGamesPaths="+filedata.split("EAGamesPaths=")[1].split("\n")[0],"EAGamesPaths="+filedata.split("EAGamesPaths=")[1].split("\n")[0]+","+value)
                else:
                    filedata=filedata.replace("EAGamesPaths=","EAGamesPaths="+value)
            else:
                filedata=filedata+"\nEAGamesPaths="+value
        # Write the file out again
        with open("config.ini", 'w') as file:
            file.write(filedata)
        return getVars()

def getGames():
    # Get games from current manifest and OSOL inis (when applicable)
    games=[]
    # Get games from current manifest
    if os.path.isfile(os.path.join(os.getcwd(),"manifest.json")):
        with open(os.path.join(os.getcwd(),"manifest.json"), 'r') as file:
            games=json.loads(file.read())
    # If manifest is targeting OriginSteamOverlayLauncher.exe, check for OSOL inis
    for game in games:
        if game["target"].split("\\")[-1]=="OriginSteamOverlayLauncher.exe":
            if os.path.isfile(os.path.join(os.getcwd(),"OSOL",game["title"],"OriginSteamOverlayLauncher.ini")):
                # Read the ini
                with open(os.path.join(os.getcwd(),"OSOL",game["title"],"OriginSteamOverlayLauncher.ini"), 'r') as file:
                    # Read the file
                    filedata = file.read()
                    # Fill in the EA Games Path
                    game["target"]=filedata.split("GamePath=")[1].split("\n")[0]
                    # Startin is the folder containing the target
                    game["startIn"]=os.path.dirname(game["target"])
                    game["type"]="OSOL"
        else:
            game["type"]="DRM-Free"
    return games

def scan(MonitorFolders,EAGamesPaths,games):
    if EAGamesPaths!=[""]:
        EAGames=[]
        EAGamesToRemove=[]
        for EAGamesPath in EAGamesPaths:
            EAGames=EAGames + searchFolder(EAGamesPath,getEAExecutable)
        # If path (startIn) is already in games, remove it
        for game in EAGames:
            game["type"]="OSOL"
            found=False
            for game2 in games:
                if game["title"]==game2["title"] or game["target"]==game2["target"]:
                    found=True
            if found:
                print(game["title"]+" is already in manifest, not updating it")
                EAGamesToRemove.append(game)
            else:
                print(game["title"]+" is not in manifest, adding it")
                games.append(game)
        for game in EAGamesToRemove:
            EAGames.remove(game)
    if MonitorFolders!=[""]:
        print("Scanning Monitor Folders for DRM-Free games")
        DRMFreeGames=[]
        DRMFreeGamesToRemove=[]
        for MonitorFolder in MonitorFolders:
            DRMFreeGames=DRMFreeGames + searchFolder(MonitorFolder,searchExe)
        # If path (startIn) is already in games, remove it
        for game in DRMFreeGames:
            game["type"]="DRM-Free"
            found=False
            for game2 in games:            
                if game["title"]==game2["title"] or game["target"]==game2["target"]:
                    found=True
            if found:
                print(game["title"]+" is already in manifest, not updating it")
                DRMFreeGamesToRemove.append(game)
            else:
                print(game["title"]+" is not in manifest, adding it")
                games.append(game)
        for game in DRMFreeGamesToRemove:
            DRMFreeGames.remove(game)
    # Write new manifest
    return games

def createManifest(games,EADesktopPath):
    for game in games:
        if game["type"]=="OSOL":
            osolGame=createOSOLConfig(game,EADesktopPath)
            if osolGame:
                game["startIn"]=osolGame["startIn"]
                game["target"]=osolGame["target"]
                game["type"]="OSOL"
    # Create manifest
    with open(os.path.join(os.getcwd(),"manifest.json"), 'w') as file:
        file.write(json.dumps(games))
    return games