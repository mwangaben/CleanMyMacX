import sys, os, re

app_path = '/Applications/CleanMyMac X.app'
bin_path = f'{app_path}/Contents/MacOS/CleanMyMac X'

print(f'Patching {bin_path} ...')

with open(bin_path, 'rb+') as file:
    binary = file.read()

    # Name: isExceeded
    # Signature: 55 48 89 E5 41 57 41 56 53 50 48 89 FB 48 8B 7F 08 48 8B 35 ? ? ? ? 4C 8B 3D ? ? ? ? 41 FF D7 48 8B 35 ? ? ? ? 48 89 DF 41 FF D7 48 89 C7 E8 ? ? ? ? 41 89 C6
    # Patch: 48 31 C0 C3

    match = re.search(b'\x55\x48\x89\xE5\x41\x57\x41\x56\x53\x50\x48\x89\xFB\x48\x8B\x7F\x08\x48\x8B\x35[\x00-\xFF][\x00-\xFF][\x00-\xFF][\x00-\xFF]\x4C\x8B\x3D[\x00-\xFF][\x00-\xFF][\x00-\xFF][\x00-\xFF]\x41\xFF\xD7\x48\x8B\x35[\x00-\xFF][\x00-\xFF][\x00-\xFF][\x00-\xFF]\x48\x89\xDF\x41\xFF\xD7\x48\x89\xC7\xE8[\x00-\xFF][\x00-\xFF][\x00-\xFF][\x00-\xFF]\x41\x89\xC6', binary)
    
    if match == None:
        sys.exit('ERROR: Function `isExceeded` not found.')
    
    offset = match.start(0);

    file.seek(offset)
    file.write(b'\x48\x31\xC0\xC3')

print(f'Re-signing {app_path} ...')

cmd_app_path = app_path.replace(' ', r'\ ')

os.system(f'codesign -fs - {cmd_app_path} --deep')
os.system(f'codesign --verify {cmd_app_path} --verbose')

print('Enjoy!')

