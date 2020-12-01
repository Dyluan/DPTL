from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

import pandas as pd

driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

#driver has to go throuh main page for session purposes.
driver.get('https://boels-nl.brico.be/')
driver.implicitly_wait(5)

#function used to make a new link from the old one.
#FR -> NL
def make_new_link(old_link):
    first_part_of_url = old_link.split('?')
    first_final_url = first_part_of_url[0].replace('fr', 'nl')
    last_part_of_url = old_link.split('&')
    temp = last_part_of_url[0].split('=')
    product_id = temp[-1]

    return first_final_url + '?productId=' + product_id


df = pd.read_csv('boelsBrico.csv', sep=';')

nl_names = []
nl_desc = []

#working correctly. Now I need to add two more columns, 
#one column for product description
#another one for the translation of the product name.
for ind in df.index:
    raw_link = df[' Url'][ind]
    print(make_new_link(raw_link))
    driver.get(make_new_link(raw_link))
    driver.implicitly_wait(5)

    try:
        item_description_path = '/html/body/main/form/div/div[1]/div[3]/p'
        item_description_brut = driver.find_element_by_xpath(item_description_path).text

        item_description = item_description_brut.replace(';', ',')

        print(item_description)
        
    except NoSuchElementException:
        print('description not found.\n')
        item_description = 'None'
    
    nl_desc.append(item_description)
        
    try:
        item_name_path = '/html/body/main/form/div/div[1]/div[3]/h1'
        item_name = driver.find_element_by_xpath(item_name_path).text

        print(item_name)
        
    except NoSuchElementException:
        print('item name not found.\n')
        item_name = 'None'
    
    nl_names.append(item_name)

df[' title_nl'] = nl_names
df[' text_nl'] = nl_desc

df.to_csv('boelsBrico.csv', sep=';', index=False)

driver.quit()