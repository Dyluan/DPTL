from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
import math

import pandas as pd

driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

driver.maximize_window()

driver.implicitly_wait(5)

driver.get('https://www.boels.be/nl?set_lang=true')

try:
    TVA_path = '/html/body/div[8]/div/div/div[2]/div[2]/div/a[1]'

    pageReadiness = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, TVA_path)))    
    driver.find_element_by_xpath(TVA_path).click()

except TimeoutException as e:

    TVA_path = '/html/body/div[7]/div/div/div[2]/div[2]/div/a[1]/h3'
    
    pageReadiness = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, TVA_path)))    
    driver.find_element_by_xpath(TVA_path).click()

df = pd.read_csv('boels.csv', sep=';', encoding='utf-8')

nl_names = []
nl_desc = []

#itering through the 'id' column in boels.csv
for ind in df.index:

    id = df['id'][ind]

    #checking if the id exist in that column
    if not math.isnan(id):
        print(ind, len(nl_names))

        #possible fix the page never loading
        if ind%100 == 0:
            driver.quit()
            driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

        try:
            x = requests.get('https://www.boels.be/nl?set_lang=true')
            
            if x.status_code in (200, 201):

                driver.get('https://www.boels.be/nl?set_lang=true')
                driver.implicitly_wait(5)

                try:
                    #try except case for when the driver stops responding

                    page_search_menu_path = '/html/body/div[5]/div[2]/div[2]/div/div/div[1]/div[2]/form/div[3]/input'
                    page_search = driver.find_element_by_xpath(page_search_menu_path)

                    #####WARNING#####
                    ###str(id)[:-2]##
                    #because the id column is not correctly formated.#
                    page_search.send_keys(str(id)[:-2])
                    page_search.send_keys(Keys.ENTER)

                    try:
                        item_name_path = '/html/body/div[5]/div[2]/div[2]/div/header/h1'
                        item_name = driver.find_element_by_xpath(item_name_path).text
                        
                        item_name = item_name.replace(';','')
                        
                        #print('Item name:', item_name)

                    except NoSuchElementException as e:
                        
                        #print('Item name:', e)
                        item_name = ''
                    
                    
                    try:
                        #clicking on the "epxand" button if there is one.
                        expand = driver.find_element_by_class_name('product-text-expand')
                        expand.click()
                    except:
                        pass
                    
                    try:
                        item_desc_raw = driver.find_element_by_class_name('product-text-inner').text
                        
                        item_desc = item_desc_raw.replace('Kenmerken','')
                        
                        item_desc = item_desc.replace(';',',')
                        
                        item_desc = item_desc.replace('\n','')
                        
                        #print('Item desc:', item_desc)
                    
                    except NoSuchElementException as e:
                        
                        #print('Item desc:', e)
                        item_desc = ''
                    
                    print('----------\n')

                    nl_desc.append(item_desc)
                    nl_names.append(item_name)
                
                except ElementNotInteractableException as e:
                    print(e)

                    try:
                        TVA_path = '/html/body/div[8]/div/div/div[2]/div[2]/div/a[1]'

                        pageReadiness = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, TVA_path)))    
                        driver.find_element_by_xpath(TVA_path).click()

                    except TimeoutException as e:

                        TVA_path = '/html/body/div[7]/div/div/div[2]/div[2]/div/a[1]/h3'
                        
                        pageReadiness = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, TVA_path)))    
                        driver.find_element_by_xpath(TVA_path).click()
                    
                    nl_names.append('')
                    nl_desc.append('')
                
                except NoSuchElementException as e:
                    print('Search menu not found.', e)
                    driver.quit()
                    driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")
                    nl_desc.append('')
                    nl_names.append('')

                
                except:
                    driver.quit()
                    driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")    
                    nl_desc.append('')
                    nl_names.append('')

        
        
        except TimeoutException as e:
            print(e)
            driver.quit()
            driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")
            nl_desc.append('')
            nl_names.append('')

        
    
    #in case the row has no id:
    else:
        nl_desc.append('')
        nl_names.append('')

driver.quit()

df['title_nl'] = nl_names
df['text_nl'] = nl_desc

df.to_csv('boels.csv', sep=';', index=False)