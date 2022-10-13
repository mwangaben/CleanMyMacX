#!/usr/bin/env python3

from pathlib import Path
from os import system

def app_not_found(name):
    print(f'{name} not found. Please make sure you have installed the latest version of CleanMyMac X from the AppStore.')

def function_not_found(name):
    print(f'FAILED: Function `{name}` not found.')

def apply_patch(binary, offset, patch):
    for i in range(len(patch)):
        binary[offset + i] = patch[i]

def main():
    app_path = Path('/Applications/CleanMyMac-MAS.app')
    binary_path = app_path.joinpath('Contents/MacOS/CleanMyMac-MAS')

    menu_app_path = app_path.joinpath('Contents/Library/LoginItems/CleanMyMac-MAS Menu.app')
    menu_binary_path = menu_app_path.joinpath('Contents/MacOS/CleanMyMac-MAS Menu')

    if not binary_path.is_file():
        app_not_found('CleanMyMac X')
        return

    if not menu_binary_path.is_file():
        app_not_found('Menu')
        return

    print(f"Patching {binary_path}...")

    with open(binary_path, 'rb+') as file:
        binary = bytearray(file.read())

        # Function: -[CMMASLimitation isExceeded]
        # Signature: 55 48 89 E5 48 8B 35 B2 D0 64 00 FF 15 1C 5E 55 00 31 C9 48 85 C0 0F 9E C1 89 C8 5D C3
        # Patch: 48 31 C0 C3

        offset = binary.find(b'\x55\x48\x89\xE5\x48\x8B\x35\xB2\xD0\x64\x00\xFF\x15\x1C\x5E\x55\x00\x31\xC9\x48\x85\xC0\x0F\x9E\xC1\x89\xC8\x5D\xC3')

        if offset == -1:
            function_not_found('-[CMMASLimitation isExceeded]')
            return

        apply_patch(binary, offset, b'\x48\x31\xC0\xC3')

        # Function: -[_TtC10CleanMyMac20ModulesListViewModel isUnlockFullVersionButtonHidden]
        # Signature: 55 48 89 E5 E8 77 0E 00 00 0F B6 C0 83 E0 01 5D C3
        # Patch: 48 C7 C0 01 00 00 00 C3

        offset = binary.find(b'\x55\x48\x89\xE5\xE8\x77\x0E\x00\x00\x0F\xB6\xC0\x83\xE0\x01\x5D\xC3')

        if offset == -1:
            function_not_found('-[_TtC10CleanMyMac20ModulesListViewModel isUnlockFullVersionButtonHidden]')
            return

        apply_patch(binary, offset, b'\x48\xC7\xC0\x01\x00\x00\x00\xC3')

        file.seek(0)
        file.write(binary)

    print(f"Patching {menu_binary_path}...")

    with open(menu_binary_path, 'rb+') as file:
        binary = bytearray(file.read())

        # Function: -[CMMASMenuLimitation isExceeded]
        # Signature: 55 48 89 E5 48 8B 35 99 15 2E 00 FF 15 7B 68 27 00 31 C9 48 85 C0 0F 9E C1 89 C8 5D C3
        # Patch: 48 31 C0 C3

        offset = binary.find(b'\x55\x48\x89\xE5\x48\x8B\x35\x99\x15\x2E\x00\xFF\x15\x7B\x68\x27\x00\x31\xC9\x48\x85\xC0\x0F\x9E\xC1\x89\xC8\x5D\xC3')

        if offset == -1:
            function_not_found('-[CMMASMenuLimitation isExceeded]')
            return

        apply_patch(binary, offset, b'\x48\x31\xC0\xC3')

        file.seek(0)
        file.write(binary)

    print(f'Re-signing {app_path}...')

    system(f'codesign -fs - {app_path} --deep')
    system(f'codesign --verify {app_path} --verbose')

    print('Enjoy!')

if __name__ == '__main__':
    main()
