#!/usr/bin/env python3

import sys, os, re

app_path = '/Applications/CleanMyMac-MAS.app'
bin_path = f'{app_path}/Contents/MacOS/CleanMyMac-MAS'

print(f'Patching {bin_path} ...')

with open(bin_path, 'rb+') as file:
    binary = file.read()

    # Name: isExceeded
    # Signature: 55 48 89 E5 48 8B 35 B8 FA 64 00 FF 15 2A 78 55 00 31 C9 48 85 C0 0F 9E C1 89 C8 5D C3
    # Patch: 48 31 C0 C3

    match = re.search(re.escape(b'\x55\x48\x89\xE5\x48\x8B\x35\xB8\xFA\x64\x00\xFF\x15\x2A\x78\x55\x00\x31\xC9\x48\x85\xC0\x0F\x9E\xC1\x89\xC8\x5D\xC3'), binary)

    if match == None:
        sys.exit('ERROR: Function `isExceeded` not found.')
    
    offset = match.start(0);

    file.seek(offset)

    file.write(b'\x48\x31\xC0\xC3')

print(f'Re-signing {app_path} ...')

os.system(f'codesign -fs - {app_path} --deep')
os.system(f'codesign --verify {app_path} --verbose')

print('Enjoy!')

