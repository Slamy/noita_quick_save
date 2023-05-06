import os
import platform
import shutil
from datetime import datetime
from pathlib import Path

from . import util

if platform.system() == "Windows":
    from . import util_windows as os_util
else:
    from . import util_linux as os_util

"""
Based on the works of
https://github.com/mcgillij/noita_save_manager
https://github.com/k-Knight/NoitaSaveScummer
"""


class SaveManager:
    backup_folder_path = None
    noita_save00_path = None
    steam_cmd = None

    def __init__(self):
        self.backup_folder_path = Path.home().joinpath("noita_save_backups").resolve()
        print(f"Backup folder for archives at {self.backup_folder_path}")
        try:
            os.mkdir(self.backup_folder_path)
        except FileExistsError:
            pass

        self.steam_cmd = os_util.find_steam_cmd()
        noita_proc = self.find_or_start_noita()

        assert noita_proc, "Unable to find Noita process"
        self.noita_save00_path = util.find_noita_save_folder(noita_proc)
        print("Perform early quick save just to be sure")
        self.backup_to_save_zip()

    def find_or_start_noita(self):
        proc = util.find_noita_process()
        if proc is None:
            print("Noita is not running. Starting it.")

            shell_cmd_start_noita = f'"{self.steam_cmd}" steam://rungameid/881100'
            print(shell_cmd_start_noita)
            os.system(shell_cmd_start_noita)
            proc = util.wait_until_noita_is_running()
        else:
            print("Noita already running. Not starting...")

        return proc

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
        print(f"---- Perform Quick Save ----")
        noita_proc = util.find_noita_process()
        assert noita_proc, "Unable to find Noita process"
        os_util.kill_noita_wait_for_termination(noita_proc)
        self.find_or_start_noita()
        self.backup_to_save_zip()
        print("Quick Save finished!")

    def quick_load(self):
        try:
            print("---- Perform Quick Load ----")
            noita_proc = util.find_noita_process()
            assert noita_proc, "Unable to find Noita process"
            os_util.kill_noita_wait_for_termination(noita_proc)
            self.restore_from_save_zip()
            self.find_or_start_noita()
            print("Quick Load finished!")
        except Exception as e:
            print(e)
