import time

from system_hotkey import SystemHotkey

from . import save_manager


def main():
    manager = save_manager.SaveManager()

    hk = SystemHotkey()
    hk.register(('control', 'shift', 'f5'), callback=lambda _: manager.quick_save())
    hk.register(('control', 'shift', 'f6'), callback=lambda _: manager.quick_load())

    print("Waiting for Hotkeys...")
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
