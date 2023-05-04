# Yet another NoitaQuickSave project

## What is this?

This is a quick-save tool to make the game Noita a little bit more respectful to your time and allows risky experimentation with dangerous wands if required.

## Why?

For some while I've used the [Noita save manager](https://github.com/mcgillij/noita_save_manager) but it lacked a quick save via hotkeys and an automatic restart of Noita. Then I've found [NoitaSaveScummer](https://github.com/k-Knight/NoitaSaveScummer) but it is for Windows only.
This project is yet another implementation of an external save file manager for Noita. Compared to both mentioned tools it has:

* Quick Save and Load via Hotkeys
    * Ctrl + Shift + F5 restarts Noita and archives the current save file
    * Ctrl + Shift + F5 restarts Noita with the most recent quick state restored.
* Non destructive
    * Like [Noita save manager](https://github.com/mcgillij/noita_save_manager) this tool will not delete save folders. They are just moved to another location with a timestamp in case problems arise.

## Building from Source

Because of certain dependencies (system_hotkey), python 3.9 must be used at the moment. [pyenv](https://bgasparotto.com/install-pyenv-ubuntu-debian) may be used here to install a specific python version.

    pyenv install 3.9
    pyenv global 3.9
    pip install -r requirements.txt


## Building single binary for easier distribution

    pyinstaller -F noita_quick_save.py