import os

def searchFolder(path,findExecutableFunction):
    # This function will look at the EA Desktop folder and will return a list of games that are installed
    # Create a list of games
    print("Looking for games in "+path)
    games = []
    for game in os.listdir(path):
        # Check that game is a folder
        if not os.path.isdir(os.path.join(path,game)):
            continue

        executable=findExecutableFunction(os.path.join(path,game),game)
        if executable:
            games.append({"title":game,"startIn":os.path.join(path,game),"target":executable})
    print("Found "+str(len(games))+" games")
    return games

def searchExe(dir,game):
    for folder in ["","__Installer","Installer","Game","Bin","bin","bin32","bin64","bin_x86","bin_x64"]:
        # If folder exists
        if not os.path.exists(os.path.join(dir,folder)):
            continue
        names=[game,game.replace(" ",""),game.replace(" ","_"),game.replace(" ","-"),game.replace(" ","_").lower(),game.replace(" ","-").lower(),game.replace(" ","_").upper(),game.replace(" ","-").upper()]
        # add names from adjacent words in game name, with or without spaces
        if " " in game:
            # split game name into words
            words=game.split(" ")
            # add names with adjacent words
            for i in range(len(words)-1):
                names.append(words[i]+words[i+1])
                names.append(words[i]+"_"+words[i+1])
                names.append(words[i]+"-"+words[i+1])
                names.append(words[i]+words[i+1].lower())
                names.append(words[i]+"_"+words[i+1].lower())
                names.append(words[i]+"-"+words[i+1].lower())
                names.append(words[i]+words[i+1].upper())
                names.append(words[i]+"_"+words[i+1].upper())
                names.append(words[i]+"-"+words[i+1].upper())
        for name in names:
            if os.path.exists(os.path.join(dir,folder,name+".exe")):
                print("Found "+name+" in "+dir)
                return os.path.join(dir,folder,name+".exe")
        # Look for any .exe without "unin"
    for file in os.listdir(os.path.join(dir,dir)):
        if file.endswith(".exe") and not "unin" in file:
            print("Found a name, but not sure if it's the right one: "+file+" in "+dir)
            return os.path.join(dir,file)
    return False