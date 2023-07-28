import os
import json

def createManifest(games):
    # Create manifest
    with open(os.path.join(os.getcwd(),"manifest.json"), 'w') as file:
        file.write(json.dumps(games))
    return games