from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

driver.get('https://boels-fr.brico.be/')
driver.implicitly_wait(5)

#df stands for DataFrame
df = pd.read_csv('boelsBrico.csv', sep=';')

magasin = {'id':[], 'nom':[], 'adresse':[], 'commune':[], 'telephone':[]}

for ind in df.index:
    
    #gets the link of each product in the Url column.
    link = df[' Url'][ind]

    driver.get(link)
    driver.implicitly_wait(5)

    try:
        location_menu_path = '//*[@id="pac_input"]'
        location_menu = driver.find_element_by_xpath(location_menu_path)

        #allows to select the location field and to enter '1000' (Bxl zipcode)
        location_menu.send_keys('1000')
        location_menu.send_keys(Keys.ENTER)
        
        #allows the driver to wait until the dealers are loaded on the webpage.
        #WARNING
        #THIS DOES NOT HANDLE THE CASE WHERE THERE ARE NO DEALERS IN BELGIUM
        pageReadiness = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/form/div/div[3]/div[1]/div[3]/div[1]/ul/li[4]/button[1]')))
        
        number_of_items = driver.find_elements_by_class_name('hirepoint')

        for item in number_of_items:

            temp = item.text.split('\n')
            if len(temp) == 6:

                name_raw = ''.join([i for i in temp[0] if not i.isdigit()]) 
                name = name_raw[2:]
                print('nom:', name)

                addr = temp[2]
                print('adresse:', addr)

                zipcode = temp[3]
                print('code postal:', zipcode)

                phone = temp[4][6:]
                print('téléphone:', phone)
                
                print('----------\n')

                magasin['id'].append(df[' ID'][ind])
                magasin['nom'].append(name)
                magasin['adresse'].append(addr)
                magasin['commune'].append(zipcode)
                magasin['telephone'].append(phone)

    except NoSuchElementException as e:
        print(e)

    except Exception as e:
        print(e)
        driver.quit()
        driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")
        #driver needs to go to that url first because of session.
        driver.get('https://boels-fr.brico.be/')
        
nf = pd.DataFrame.from_dict(magasin)
nf.to_csv('liste_magasins.csv', sep=';')

driver.quit()