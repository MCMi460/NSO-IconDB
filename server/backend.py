# Made by Deltaion Lee (MCMi460) on Github
import os, time, sqlite3
from nso import NSOAppletAPI
from private import headers

while True:
    with NSOAppletAPI(headers = headers) as api, open('CREATE.sql', 'r') as sql_file:
        create_file = sql_file.read() # Get database creation file

        # Fetch categories
        gift_categories = api.getV1GiftCategories('US')

        for category in gift_categories:
            category_path = os.path.join(os.getcwd(), 'gifts', category.key)
            if not os.path.exists(category_path):
                os.makedirs(category_path) # Make game directory, if not existent

            db_path = os.path.join(category_path, '%s.db' % category.key)
            db_exists = os.path.isfile(db_path)
            with sqlite3.connect(db_path) as con: # Access database for category
                cursor = con.cursor()
                if not db_exists: # Init DB
                    cursor.execute(create_file)
                    con.commit()

                # If not downloaded, download icon file (should always be a .webp)
                for gift in category.gifts:
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

            # Dump rest of category data
            with open(os.path.join(category_path, 'dump.%s.txt' % category.id), 'w+') as file:
                file.write(str(category))

    # Wait an hour before retrying
    time.sleep(3600)
