from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

import pandas as pd

driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

df = pd.read_csv('boelsBrico.csv', sep=';', encoding='cp1252')

#see: https://www.geeksforgeeks.org/iterating-over-rows-and-columns-in-pandas-dataframe/

for ind in df.index:
    print(df['img_link'][ind])
    filename = df['item_id'][ind]
    driver.get(df['img_link'][ind])
    driver.implicitly_wait(5)
    driver.get_screenshot_as_file('C:/Users/Dylan/Documents/python/django/apprendre/mysite/appartements/aliloca/boelsBrico/images/'+filename+'.png')
    
    driver.implicitly_wait(5)

driver.quit()