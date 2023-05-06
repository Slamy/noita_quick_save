import win32con
import win32gui
import win32process

from . import util


# Stolen from https://github.com/k-Knight/NoitaSaveScummer
def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds_out):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds_out.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def kill_noita_wait_for_termination(noita_proc):
    # Don't use noita_proc.terminate() as Noita doesn't save in that case
    # Use the win32 api to close the Noita window gracefully
    hwnd = get_hwnds_for_pid(noita_proc.pid)
    win32gui.PostMessage(hwnd[0], win32con.WM_CLOSE, 0, 0)

    noita_proc.wait(10)
    print("Noita has terminated!")


def find_steam_cmd():
    steam_proc = util.find_process("steam.exe")
    assert steam_proc, "Steam not running!"
    return steam_proc.exe()
