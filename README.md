# Steam Rom Manager Helper (Previously AutOSOL)

Automatically Create Manifests for OSOL launched games and DRM Free Game folders for import into Steam Rom Manager

## What is this?

This is an applet that will automatically create [OriginSteamOverlayLauncher](https://github.com/WombatFromHell/OriginSteamOverlayLauncher) configs for each EA Desktop Game installed and generate a manifest.json file for [Steam Rom Manager](https://github.com/SteamGridDB/steam-rom-manager) to import. It can also add DRM-Free games from a monitored folder to the manifest.

## Why not just use the EA Desktop preset in Steam Rom Manager?

The EA Desktop preset in Steam Rom Manager is great for launching the game, but it doesn't hook the Steam Overlay into the game. This means that Steam Input won't work, nor will Steam Link/Remote Play. OSOL hooks into the game process, but setting it up can take a while if you have a lot of games installed. This script automates that process. It also doesn't support importing games from a folder, like itch.io or Amazon Games (previously Twitch Games) which are DRM free.

## How do I use this?

1. [Download the latest release from the releases page](https://github.com/michaelphagen/Steam-Rom-Manager-Helper/releases)
2. Move the executable to a folder you'd like to create the OSOL configs and SRM manifest in
3. Set your EA Games folder and DRM-Free folders using the "Add EA/DRM-Free Folder" buttons
4. Click "Scan Folders" to scan for games
5. Edit any games by double clicking on them in the list
6. Click Update Manifest to create SRM compatible manifest
7. Import the manifest.json file into Steam Rom Manager as a "Manual" type parser
