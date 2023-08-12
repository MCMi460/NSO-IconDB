# Made by Deltaion Lee (MCMi460) on Github
import os, time, sqlite3, datetime, sys
from nso import NSOAppletAPI

def main():
    print(datetime.datetime.now())
    with NSOAppletAPI(headers = headers) as api, open('C_CREATE.sql', 'r') as cFile, open('G_CREATE.sql', 'r') as gFile:
        # Get database creation files
        cSQL = cFile.read()
        gSQL = gFile.read()

        # Fetch categories
        gift_categories = api.getV1GiftCategories('US')

        gifts_path = os.path.join(os.getcwd(), 'gifts')
        if not os.path.exists(gifts_path):
            os.makedirs(gifts_path)
        categoryDB_PATH = os.path.join(os.getcwd(), 'gifts/category.db')
        categoryDB_EXISTS = os.path.isfile(categoryDB_PATH)
        with open('current.txt', 'w+') as file:
            file.write('')

        with sqlite3.connect(categoryDB_PATH) as categoryCon: # Access database for category
            categoryCursor = categoryCon.cursor()
            if not categoryDB_EXISTS: # Init DB
                categoryCursor.execute(cSQL)
                categoryCon.commit()

            for category in gift_categories:
                category_path = os.path.join(gifts_path, category.key)
                if not os.path.exists(category_path):
                    os.makedirs(category_path) # Make game directory, if not existent

                db_path = os.path.join(category_path, '%s.db' % category.key)
                db_exists = os.path.isfile(db_path)
                with sqlite3.connect(db_path) as con: # Access database for category
                    cursor = con.cursor()
                    if not db_exists: # Init DB
                        cursor.execute(gSQL)
                        con.commit()

                    # If not downloaded, download icon file (should always be a .webp)
                    for gift in category.gifts:
                        with open('current.txt', 'a') as file:
                            file.write('%s\n%s\n%s\n' % (category.name, gift.name if gift.name else ' '.join(gift.tags), '/gifts/%s/%s.webp' % (category.key, gift.id)))

                        gift_path = os.path.join(category_path, gift.id + '.webp')
                        if not os.path.isfile(gift_path):
                            with open(gift_path, 'wb+') as file:
                                file.write(api._get(gift.reward.thumbnail_url).content)
                        cursor.execute('SELECT count(*) FROM gifts WHERE id = ?', (gift.id,))
                        count = cursor.fetchone()[0]
                        if count == 0:
                            cursor.execute(
                                'INSERT INTO gifts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (gift.id, gift.name, ' '.join(gift.tags), gift.meta, gift.created_at, gift.updated_at, gift.reward.thumbnail_url, gift.reward.point.platinum, gift.reward.begins_at, gift.reward.ends_at),
                            )
                        else:
                            cursor.execute(
                                'UPDATE gifts SET begins_at = ?, ends_at = ? WHERE id = ?',
                                (gift.reward.begins_at, gift.reward.ends_at, gift.id),
                            )
                    con.commit()

                categoryCursor.execute('SELECT count(*) FROM categories WHERE key = ?', (category.key,))
                count = categoryCursor.fetchone()[0]
                if count == 0:
                    categoryCursor.execute(
                        'INSERT INTO categories VALUES (?, ?, ?, ?, ?)',
                        (category.key, category.name, category.image_url, category.description, category.key_color),
                    )
                    categoryCon.commit()
                icon_path = os.path.join(category_path, category.key + '.webp')
                if not os.path.isfile(icon_path):
                    with open(icon_path, 'wb+') as file:
                        file.write(api._get(category.image_url).content)

                # Dump rest of category data
                #with open(os.path.join(category_path, 'dump.%s.txt' % category.id), 'w+') as file:
                #    file.write(str(category))

    with open('backend.txt', 'w+') as file:
        file.write(str(time.time()))

def getCurrentIcons():
    with open('current.txt', 'r') as file:
        lines = file.read().rstrip().split('\n')
        icons = [ lines[n:n + 3] for n in range(0, len(lines), 3) ]
    return icons

if __name__ == '__main__':
    from private import headers
    while True:
        main()

        # Wait an hour before retrying
        time.sleep(3600)
else:
    import importlib
    headers = importlib.import_module('NSO-IconDB.server.private').headers
