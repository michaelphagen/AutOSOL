#Generate a basic UI window
import PySimpleGUI as sg
from folder import *
from util import *
from osol import *
from tkinter import *
from tkinter import ttk

import json

games=[]

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
    ## THIS NEEDS TO CHECK IF VAR ISD ALREADY IN CONFIG
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


def getGames(EAGamesPaths):
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
    if MonitorFolders==[""] and EAGamesPaths==[""]:
        sg.popup("No Monitor Folder or EA Games Path found, be sure to set it if you want to import games")
        return games
    if EAGamesPaths!=[""]:
        EAGames=[]
        for EAGamesPath in EAGamesPaths:
            EAGames=EAGames + searchFolder(EAGamesPath,getEAExecutable)
        # If path (startIn) is already in games, remove it
        for game in EAGames:
            game["type"]="OSOL"
            found=False
            for game2 in games:
                if game["title"]==game2["title"]:
                    found=True
            if found:
                print(game["title"]+" is already in manifest, not updating it")
                EAGames.remove(game)
            else:
                print(game["title"]+" is not in manifest, adding it")
                games.append(game)
    if MonitorFolders!=[""]:
        print("Scanning Monitor Folders for DRM-Free games")
        DRMFreeGames=[]
        for MonitorFolder in MonitorFolders:
            DRMFreeGames=DRMFreeGames + searchFolder(MonitorFolder,searchExe)
        # If path (startIn) is already in games, remove it
        for game in DRMFreeGames:
            game["type"]="DRM-Free"
            found=False
            for game2 in games:            
                if game["title"]==game2["title"]:
                    found=True
            if found:
                print(game["title"]+" is already in manifest, not updating it")
                DRMFreeGames.remove(game)
            else:
                print(game["title"]+" is not in manifest, adding it")
                games.append(game)
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

def formatData(games):
    # Format games for display
    tree_data = sg.TreeData()
    parents=[]
    view=[]
    for game in games:
        # check if type key exists
        if "type" not in game:
            print("Type not found for "+game["title"]+"!")
        if game["type"] not in parents:
            parents.append(game["type"])
            view.append(["",game["type"],game["type"],"",""])
        view.append([game["type"],game["type"]+"-tag-"+game["title"],game["title"],game["target"],game["startIn"]])
    for row in view:
      tree_data.Insert(row[0], row[1], row[2], row[3:])
    return tree_data

def editGame(games,selection):
    if "-tag-" not in selection:
        return
    title=selection.split("-tag-")[1]
    type=selection.split("-tag-")[0]
    game = [game for game in games if game["title"] == title and game["type"]==type][0]
    # Create windows with title, target, and startIn fields
    layout = [
        [sg.Text("Title"), sg.InputText(game["title"], key="title")],
        [sg.Text("Target"), sg.InputText(game["target"], key="target")],
        [sg.Text("StartIn"), sg.InputText(game["startIn"], key="startIn")],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]
    window = sg.Window("Edit Game", layout)
    while True:
        event, values = window.read()
        if event == "Save":
            print("Saving "+values["title"]+" as "+values["target"]+" in "+values["startIn"])
            game["title"]=values["title"]
            game["target"]=values["target"]
            game["startIn"]=values["startIn"]
            # Replace game in games
            for i in range(len(games)):
                if games[i]["title"]==title and games[i]["type"]==type:
                    games[i]=game
            window.close()
            return games
        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            return games


def main():
    # Get vars from config
    MonitorFolders,EADesktopPath,EAGamesPaths=getVars()
    # Get games from current manifest and OSOL inis (when applicable)
    games=getGames(EAGamesPaths)
    headings = ['Target','StartIn']
    layout = [
        [sg.Stretch(), sg.Text("SRM Helper"), sg.Stretch()],
        # Here we list the Games we can add to SRM
        [sg.Stretch(), sg.Text("Games:"), sg.Stretch()],
        [sg.Tree(
      data=formatData(games),
      headings=headings,
      auto_size_columns=True,
      select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
      num_rows=10,
      key="-GAMELIST-",
      show_expanded=True,
      enable_events=True,
      expand_x=True,
      expand_y=True
   )],
        [sg.Stretch(), sg.Button("Add EA Folder"),sg.Button("Add DRM-Free Folder"), sg.Button("Scan Folders"), sg.Button("Update Manifest"), sg.Stretch()],
    ]
    window = sg.Window(
        "SRM Helper",
        layout,
        default_element_size=(12, 1),
        resizable=True,
        finalize=True,
    )  # this is the chang
    window.bind("<Configure>", "Event")
    window.bind('<Double-Button-1>', '_double_clicked')
    while True:
        event = window.read()
        if "Add EA Folder" in event:
            # Create pop up with 2 buttons to add a regular foldedr or an EA folder
            folder = sg.popup_get_folder("Select an EA Games folder to monitor")
            if folder:
                MonitorFolders,EADesktopPath,EAGamesPaths=updateVars("EAGamesPath",folder)
            if not EADesktopPath:
                folder = sg.popup_get_folder("Select an EA Desktop folder")
                if folder:
                    MonitorFolders,EADesktopPath,EAGamesPaths=updateVars("EADesktopPath",folder)
        if "Add DRM-Free Folder" in event:
            # Create pop up with 2 buttons to add a regular foldedr or an EA folder
            folder = sg.popup_get_folder("Select an DRM-Free Games folder to monitor")
            if folder:
                MonitorFolders,EADesktopPath,EAGamesPaths=updateVars("MonitorFolder",folder)
        if "Scan Folders" in event:
            games=scan(MonitorFolders,EAGamesPaths,games)
            window["-GAMELIST-"].update(values=formatData(games))
        if "Update Manifest" in event:
            createManifest(games,EADesktopPath)
        if "_double_clicked" in event:
            selection=event[1]["-GAMELIST-"][0]
            games=editGame(games,selection)
            if games:
                window["-GAMELIST-"].update(values=formatData(games))
        if sg.WIN_CLOSED in event:
            break


if __name__ == "__main__":
    main()