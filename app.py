#Generate a basic UI window
import PySimpleGUI as sg

from util import *
from folder import *
from osol import *

games=[]

def formatData(games):
    # Format games for display
    tree_data = sg.TreeData()
    parents=[]
    view=[]
    for game in games:
        if game["type"] not in parents:
            parents.append(game["type"])
            view.append(["",game["type"],game["type"],"",""])
        view.append([game["type"],game["type"]+"-tag-"+game["title"],game["title"],game["target"],game["startIn"]])
    for row in view:
      tree_data.Insert(row[0], row[1], row[2], row[3:])
    return tree_data

def editGame(games,game):
    # Find index of game in games
    index=0
    for game2 in games:
        if game2["title"]==game["title"]:
            break
        index+=1
    # Create windows with title, target, and startIn fields
    layout = [
        [sg.Text("Title"), sg.InputText(game["title"], key="title")],
        [sg.Text("Target"), sg.InputText(game["target"], key="target")],
        [sg.Text("StartIn"), sg.InputText(game["startIn"], key="startIn")],
        [sg.Radio('OSOL', "RADIO1", default=game["type"]=="OSOL", key="OSOL"), sg.Radio('DRM-Free', "RADIO1", default=game["type"]=="DRM-Free", key="DRM-Free")],
        [sg.Button("Save"), sg.Button("Cancel")]#delete button if game is not new
        if index==len(games) else [sg.Button("Save"), sg.Button("Cancel"), sg.Button("Delete",button_color=("white","red"))]
    ]
    window = sg.Window("Edit Game", layout)
    while True:
        event, values = window.read()
        if event == "Save":
            # If any fields are empty, show popup and continue
            if values["title"]=="" or values["target"]=="" or values["startIn"]=="":
                sg.popup("No Fields can be blank")
                continue
            # Check that target is an exe and startIn is a folder
            if not (values["target"].endswith(".exe") and os.path.isdir(values["startIn"])):
                sg.popup("Target and StartIn must be an exe and a folder, respectively")
                continue
            game["title"]=values["title"]
            game["target"]=values["target"]
            game["startIn"]=values["startIn"]
            if values["OSOL"]:
                game["type"]="OSOL"
            elif values["DRM-Free"]:
                game["type"]="DRM-Free"
            else:
                sg.popup("Please select a type")
                continue
            window.close()
            # If game is new, append it to games
            if index==len(games):
                games.append(game)
            else:
                games[index]=game
            return games
        if event == "Delete":
            # Delete game from games
            del games[index]
            window.close()
            return games
        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            return games


def main():
    # Get vars from config
    MonitorFolders,EADesktopPath,EAGamesPaths=getVars()
    # Get games from current manifest and OSOL inis (when applicable)
    games=getGames()
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
        [sg.Stretch(), sg.Button("Add Game Manually"),sg.Button("Add EA Folder"),sg.Button("Add DRM-Free Folder"), sg.Button("Scan Folders"), sg.Button("Update Manifest"), sg.Stretch()],
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
            if MonitorFolders==[""] and EAGamesPaths==[""]:
                sg.popup("No Monitor Folder or EA Games Path found, be sure to set it if you want to import games")
            else:
                games=scan(MonitorFolders,EAGamesPaths,games)
                window["-GAMELIST-"].update(values=formatData(games))
        if "Update Manifest" in event:
            createManifest(games,EADesktopPath)
        if "_double_clicked" in event:
            selection=event[1]["-GAMELIST-"][0]
            if "-tag-" in selection: 
                title=selection.split("-tag-")[1]
                type=selection.split("-tag-")[0]
                game = [game for game in games if game["title"] == title and game["type"]==type][0]
                games=editGame(games,game)
                if games:
                    window["-GAMELIST-"].update(values=formatData(games))
        if "Add Game Manually" in event:
            emptyGame={"title":"","target":"","startIn":"","type":""}
            games=editGame(games,emptyGame)
            if games:
                window["-GAMELIST-"].update(values=formatData(games))
        if sg.WIN_CLOSED in event:
            break


if __name__ == "__main__":
    main()