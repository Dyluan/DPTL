from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

driver.get('https://www.loxam.fr/c/location/transport-et-manutention/vehicule-leger/430')
driver.implicitly_wait(5)

try:
    #in case there is an ad the browser needs to close
    continue_button_path = '/html/body/div[1]/div/div/div[2]/p/button/div/span'
    driver.find_element_by_xpath(continue_button_path).click()

except NoSuchElementException:
    print(NoSuchElementException)

try:
    #choice particuler/ professionnel
    select_job_path = '/html/body/main/footer/div[4]/div[1]'
    driver.find_element_by_xpath(select_job_path).click()

except NoSuchElementException:
    print(NoSuchElementException)

try:
    #accessing the Renting Menu
    renting_button_path = '/html/body/main/header/div[3]/div/nav/ul/li[1]/div/div'
    driver.find_element_by_xpath(renting_button_path).click()

    ############NEEDED############
    ##HARDCODE THE SUBMENU LINKS##
    ##############################
    
except NoSuchElementException:
    print(NoSuchElementException)
    driver.quit()

#once on a specific webpage::
try:
    nb_items = driver.find_elements_by_class_name('ProductList-item')
    
    for i in range(1, len(nb_items)+1):
        try:
            price_path = '/html/body/main/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div['+str(i)+']/div[2]/div/span'
            price = driver.find_element_by_xpath(price_path).text

            print('Price:', price)

        except NoSuchElementException:
            print('Price:', NoSuchElementException)
        
        try:
            name_path = '/html/body/main/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div['+str(i)+']/div[1]/a[1]/h2'
            name = driver.find_element_by_xpath(name_path).text

            print('Name:', name)

        except NoSuchElementException:
            print('Name:', NoSuchElementException)
        
        try:
            url_path = '/html/body/main/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div['+str(i)+']/div[1]/a[1]'
            url = driver.find_element_by_xpath(url_path).get_attribute('href')

            print('Link:', url)

        except NoSuchElementException:
            print('Link:', NoSuchElementException)


except NoSuchElementException:
    print('This category of products is empty.')

driver.quit()