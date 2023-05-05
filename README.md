# Yet another NoitaQuickSave project

## What is this?

This is a quick save tool to make the game [Noita](https://store.steampowered.com/app/881100/Noita/) a little bit more
respectful to your time and allows risky experimentation with dangerous wands if required.

## Why?

For some time, I've used the [Noita save manager](https://github.com/mcgillij/noita_save_manager) but it lacked a
quick save via hotkeys and an automatic restart of Noita.
Then I've found [NoitaSaveScummer](https://github.com/k-Knight/NoitaSaveScummer), but it is Windows only.
This project is yet another implementation of an external save file manager for Noita.

## Features

* Launches Noita and performs an early quick save just to be sure
* Quick Save and Load via Hotkeys
    * Ctrl + Shift + F5 restarts Noita and archives the current save game
    * Ctrl + Shift + F6 restarts Noita with the most recent quick save state restored.
* Non destructive
    * Like [Noita save manager](https://github.com/mcgillij/noita_save_manager) this tool will not delete save folders.
      They are just moved to another location with a timestamp in case problems arise.
* Portable as Windows and Linux is detected
* Archives are stored in the home directory inside the subfolder `noita_save_backups`

## Lack of Features

* No GUI at the moment.
* Quick Load always loads the most recent save archive

## Building from Source

Because of certain dependencies (system_hotkey), python 3.9 must be used at the moment. [pyenv](https://bgasparotto.com/install-pyenv-ubuntu-debian) can be used to install a specific python version. I'm no expert with conda but that might work as well. Debian uses 3.10 on Bookworm so these steps are required if you use that linux distribution.

    pyenv install 3.9
    pyenv global 3.9
    pip install -r requirements.txt

## Building single binary for easier distribution

This is based on [pyinstaller](https://pyinstaller.org/en/stable/)

    pyinstaller -F noita_quick_save.py

## Cross-Distribution using Wine

**Ensure to activate inclusion in PATH so pip and python are available!**

    wget https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe
    wine python-3.9.13-amd64.exe
    wine pip install -r requirements_windows.txt
    wine pip install pyinstaller
    wine pyinstaller -F noita_quick_save.py

