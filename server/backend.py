import os
from nso import NSOAppletAPI
from private import headers

with NSOAppletAPI(headers = headers) as api:
    gift_categories = api.getV1GiftCategories('US')

    for category in gift_categories:
        icon_path = os.path.join(os.getcwd(), 'gifts', category.key)
        if not os.path.exists(icon_path):
            os.makedirs(icon_path)
        for gift in category.gifts:
            gift_path = os.path.join(icon_path, gift.id + '.webp')
            if not os.path.isfile(gift_path):
                with open(gift_path, 'wb+') as file:
                    file.write(api._get(gift.reward.thumbnail_url).content)
        with open(os.path.join(icon_path, 'README.md'), 'w+') as file:
            file.write('# Dumped data:\n\n```\n%s\n```' % category)
