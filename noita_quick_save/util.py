import os
import time
from datetime import datetime
from pathlib import Path

import psutil

PROTON_NOITA_CWD_TO_SAVE_00 = "../../compatdata/881100/pfx/drive_c/" \
                              "users/steamuser/AppData/LocalLow/Nolla_Games_Noita/save00"

SECONDS_TO_WAIT_FOR_NOITA = 25


def time_string():
    return datetime.now().strftime("%Y_%m_%d-%H_%M_%S")


def find_process(name):
    for proc in psutil.process_iter():
        if name == proc.name().lower():
            print(f"Found {name} process with pid {proc.pid}")
            return proc
    print(f"{name} not found")
    return None


def find_noita_process():
    return find_process("noita.exe")


def wait_until_noita_is_running():
    for i in range(SECONDS_TO_WAIT_FOR_NOITA):
        noita_proc = find_noita_process()
        if noita_proc:
            return noita_proc
        time.sleep(1)
    raise RuntimeError("No Noita process found")


def find_noita_save_folder(noita_proc):
    # First try position on linux using proton
    linux_save_folder = Path(noita_proc.cwd()).joinpath(PROTON_NOITA_CWD_TO_SAVE_00).resolve()
    print(linux_save_folder)
    if os.path.exists(linux_save_folder):
        print(f"Noita save game in proton style location {linux_save_folder}")
        return linux_save_folder

    # Well, now try the Windows position
    windows_save_folder = Path.home().joinpath('AppData/LocalLow/Nolla_Games_Noita/save00').resolve()
    if os.path.exists(windows_save_folder):
        print(f"Noita save game in Windows style location {windows_save_folder}")
        return windows_save_folder

    raise RuntimeError("The game was never saved before!")
