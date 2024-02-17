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
import re, shutil, webbrowser, os, sqlite3

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
log('Passed all checks. Creating API object...', nso.Color.GREEN)
with nso.NSOAppletAPI(headers = headers) as api, open('../server/C_CREATE.sql', 'r') as cFile, open('../server/G_CREATE.sql', 'r') as gFile:
    cSQL = cFile.read()
    gSQL = gFile.read()

    country = input('Input your country code (US/GB/JP/etc). Leave blank for US\n> ')
    if not country:
        country = 'US'
    right_categories = api.getV1UserRightCategories(country)

    rights_path = os.path.join(os.getcwd(), 'rights')
    if not os.path.exists(rights_path):
        os.makedirs(rights_path)
    categoryDB_PATH = os.path.join(os.getcwd(), 'rights/category.db')
    categoryDB_EXISTS = os.path.isfile(categoryDB_PATH)

    with sqlite3.connect(categoryDB_PATH) as categoryCon:
        categoryCursor = categoryCon.cursor()
        if not categoryDB_EXISTS:
            categoryCursor.execute(cSQL)
            categoryCon.commit()

        for category in right_categories:
            category_path = os.path.join(rights_path, category.key)
            if not os.path.exists(category_path):
                os.makedirs(category_path)
            
            db_path = os.path.join(category_path, '%s.db' % category.key)
            db_exists = os.path.isfile(db_path)
            with sqlite3.connect(db_path) as con:
                cursor = con.cursor()
                if not db_exists:
                    cursor.execute(gSQL)
                    con.commit()

                for right in category.rights:
                    right_path = os.path.join(category_path, right.gift.id + '.webp')
                    if not os.path.isfile(right_path):
                        with open(right_path, 'wb+') as file:
                            file.write(api._get(right.content_url).content)
                    cursor.execute('SELECT count(*) FROM gifts WHERE id = ?', (right.gift.id,))
                    count = cursor.fetchone()[0]
                    if count == 0:
                        cursor.execute(
                            'INSERT INTO gifts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (right.gift.id, right.gift.name, ' '.join(right.gift.tags), right.gift.meta, right.gift.created_at, right.gift.updated_at, right.content_url, -1, '?', '?'),
                        )
                con.commit()

                categoryCursor.execute('SELECT count(*) FROM categories WHERE key = ?', (category.key,))
                count = categoryCursor.fetchone()[0]
                if count == 0:
                    categoryCursor.execute(
                        'INSERT INTO categories VALUES (?, ?, ?, ?, ?)',
                        (category.key, category.name, category.image_url, '?', '?'),
                    )
                    categoryCon.commit()
                icon_path = os.path.join(category_path, category.key + '.webp')
                if not os.path.isfile(icon_path):
                    with open(icon_path, 'wb+') as file:
                        file.write(api._get(category.image_url).content)
                
log('Done dumping all assets and data', color = nso.Color.GREEN)
