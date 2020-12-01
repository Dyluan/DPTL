from PIL import Image

import pandas as pd

df = pd.read_csv('boelsBrico.csv', sep=';', encoding='cp1252')

for ind in df.index:
    image_name = df['item_id'][ind]

    image_path = 'C:\\Users\\Dylan\\Documents\\python\\django\\apprendre\\mysite\\appartements\\aliloca\\boelsBrico\\images\\' + str(image_name) + '.png'

    im = Image.open(image_path)

    cr = im.crop((392, 199, 892, 696))

    cr.save(image_path)

    print(image_name, 'cropped successfully.')