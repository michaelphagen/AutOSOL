# AutOSOL

Automatically Create OSOL configs for integrating with Steam Rom Manager

## What is this?

This is a simple script that will automatically create [OriginSteamOverlayLauncher](https://github.com/WombatFromHell/OriginSteamOverlayLauncher) configs for each EA Desktop Game installed and generate a manifest.json file for [Steam Rom Manager](https://github.com/SteamGridDB/steam-rom-manager) to import.

## Why not just use the EA Desktop preset in Steam Rom Manager?

The EA Desktop preset in Steam Rom Manager is great for launching the game, but it doesn't hook the Steam Overlay into the game. This means that Steam Input won't work, nor will Steam Link/Remote Play. OSOL hooks into the game process, but setting it up can take a while if you have a lot of games installed. This script automates that process.

## How do I use this?

1. [Download](https://github.com/michaelphagen/AutOSOL/archive/refs/heads/main.zip) or `git clone` this repository
2. Make sure the EADesktopPath and EAGamesPath in config.ini match your install of EA Desktop
3. Run `python3 sync.py`
4. Import the manifest.json file into Steam Rom Manager as a "Manual" type parser
