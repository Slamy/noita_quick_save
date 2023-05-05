import xpybutil
import xpybutil.ewmh as ewmh


def kill_noita_wait_for_termination(noita_proc):
    # Don't use noita_proc.terminate() as Noita doesn't save in that case
    # Use the X11 api to close the window gracefully
    window_found = False
    all_windows = xpybutil.ewmh.get_client_list().reply()

    for window in all_windows:
        name = xpybutil.ewmh.get_wm_name(window).reply()

        if "Noita - " in str(name):
            ewmh.request_close_window_checked(window, source=0).check()
            print("Sent request to close Noita window!")
            window_found = True

    assert window_found, "Noita window not found!"
    noita_proc.wait(10)
    print("Noita has terminated!")


def find_steam_cmd():
    # It can be assumed that steam is in the PATH
    return "steam"
