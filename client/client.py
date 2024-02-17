def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_module(module) -> bool:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        print('Couldn\'t find %s' % module)
        return False
    return True

def safe_install(module) -> bool:
    if check_module(module):
        return True

    import pip

    with open('requirements.txt', 'r') as file:
        packages = file.read().strip().split('\n')

    print('Installing packages: %s' % ', '.join(packages))
    for package in packages:
        pip.main(['install', package])
    
    return check_module(module)

def check_token() -> int:
    regex_JWT = r'NASID=[\w-]+\.[\w-]+\.[\w-]+$' # https://stackoverflow.com/a/74221374/
    pattern = re.compile(regex_JWT)
    try:
        from private import headers
    except ImportError:
        log('private.headers missing', color = nso.Color.RED)
        return 0
    
    if pattern.search(headers['Cookie']) is None:
        log('private.headers missing NASID', color = nso.Color.RED)
        return 1

    log('Found NASID in private.headers', color = nso.Color.GREEN)
    return 2

if not safe_install('nso'):
    raise ImportError('failed to install nso-applet-api')
try: import readline
except ImportError: pass
import re, shutil, webbrowser, os

log = lambda *text, color = nso.Color.WHITE: nso.NSOAppletAPI._log(None, *text, color = color)

clear()
token_status = check_token()
while token_status != 2:
    if token_status == 0:
        shutil.copyfile('template.private.py', 'private.py')
    elif token_status == 1:
        print('You do not have the necessary headers in place in order to run this app.\n'
        + 'Would you like to open a URL to display the instructions on your webbrowser?')
        response = input('[Y]/[N]/[T]ry again\n> ')
        if response.lower().startswith('n'):
            quit()
        elif response.lower().startswith('y'):
            URL = 'https://github.com/MCMi460/NSO-IconDB/blob/main/client/README.md'
            webbrowser.open(URL)
            print('If the URL has not opened in your browser already, please copy the link below:\n'
            + URL)
            quit()
    token_status = check_token()
from private import headers
