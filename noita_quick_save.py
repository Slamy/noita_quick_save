import os
import shutil
import time
from datetime import datetime
from pathlib import Path

import psutil
import pyautogui
from system_hotkey import SystemHotkey

"""
Based on the works of
https://github.com/mcgillij/noita_save_manager
https://github.com/k-Knight/NoitaSaveScummer
"""

NOITA_CWD_TO_SAVE_00 = "../../compatdata/881100/pfx/drive_c/users/steamuser/AppData/LocalLow/Nolla_Games_Noita/save00"
SHELL_CMD_START_NOITA = 'steam steam://rungameid/881100'

class SaveManager:
    backup_folder_path = None
    noita_save00_path = None

    def __init__(self):
        self.backup_folder_path = Path.home().joinpath("noita_save_backups").resolve()
        print(f"Backup folder for archives at {self.backup_folder_path}")
        try:
            os.mkdir(self.backup_folder_path)
        except FileExistsError:
            pass

        noita_proc = self.find_or_start_noita()
        assert noita_proc, "Unable to find Noita process"
        self.noita_save00_path = self.find_noita_save_folder(noita_proc)
        print("Perform early quick save just to be sure")
        self.backup_to_save_zip()

    def find_or_start_noita(self):
        proc = self.find_noita_process()
        if proc is None:
            print("Noita is not running. Starting it.")
            os.system(SHELL_CMD_START_NOITA)
            proc = self.wait_until_noita_is_running()
        else:
            print("Noita already running. Not starting...")

        return proc

    @staticmethod
    def find_noita_process():
        for proc in psutil.process_iter():
            if "noita.exe" == proc.name().lower():
                print(f"Found noita process with pid {proc.pid}")
                return proc
        print("Noita not found")
        return None

    @staticmethod
    def find_noita_save_folder(noita_proc):
        save_folder = Path(noita_proc.cwd()).joinpath(NOITA_CWD_TO_SAVE_00).resolve()
        assert os.path.exists(save_folder), "The game was never saved before!"
        return save_folder

    def wait_until_noita_is_running(self):
        for i in range(10):
            noita_proc = self.find_noita_process()
            if noita_proc:
                return noita_proc
            time.sleep(1)
        raise RuntimeError("No Noita process found")

    @staticmethod
    def kill_noita_wait_for_termination(noita_proc):
        # Don't use terminate as Noita doesn't save in that case
        # proc.terminate()
        # Use keystrokes instead. First we need to release ctrl and shift as these were part of our hotkeys
        print("Activate Hotkey for Alt + F4")
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('shift')
        pyautogui.hotkey('alt', 'f4')

        noita_proc.wait(10)
        print("Noita has terminated!")

    def backup_to_save_zip(self):
        # uncompressed save game - active
        time_string = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        backup_name = f"noita_backup_{time_string}"
        backup_path = Path(self.backup_folder_path).joinpath(backup_name)

        print(f"Archiving {self.noita_save00_path} to {backup_path}")
        shutil.make_archive(
            str(backup_path),
            "zip",
            root_dir=self.noita_save00_path,
            dry_run=False,
        )
        print("Backup created")

    def find_most_recent_save_zip(self):
        return sorted(self.backup_folder_path.glob("noita_backup_*.zip"))[-1]

    def restore_from_save_zip(self):
        # Create backup of current save folder to avoid destruction by corrupted archives
        timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        backup_path = Path(self.noita_save00_path).joinpath(f"../{timestamp}.bak").resolve()
        print(f"Moving {self.noita_save00_path} to {backup_path} to be safe")
        shutil.move(self.noita_save00_path, backup_path)

        # Create empty dir in its place.
        zip_archive_path = self.find_most_recent_save_zip()
        print(f"Create empty {self.noita_save00_path} and unpack {zip_archive_path}")
        os.mkdir(self.noita_save00_path)
        shutil.unpack_archive(zip_archive_path, self.noita_save00_path)

    def quick_save(self):
        try:
            print(f"---- Perform Quick Save ----")
            noita_proc = self.find_noita_process()
            assert noita_proc, "Unable to find Noita process"
            self.kill_noita_wait_for_termination(noita_proc)
            self.find_or_start_noita()
            self.backup_to_save_zip()
            print("Quick Save finished!")
        except Exception as e:
            print(e)

    def quick_load(self):
        try:
            print("---- Perform Quick Load ----")
            noita_proc = self.find_noita_process()
            assert noita_proc, "Unable to find Noita process"
            self.kill_noita_wait_for_termination(noita_proc)
            self.restore_from_save_zip()
            self.find_or_start_noita()
            print("Quick Load finished!")
        except Exception as e:
            print(e)


def main():
    manager = SaveManager()

    hk = SystemHotkey()
    hk.register(('control', 'shift', 'f5'), callback=lambda _: manager.quick_save())
    hk.register(('control', 'shift', 'f6'), callback=lambda _: manager.quick_load())

    print("Waiting for Hotkeys...")
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
