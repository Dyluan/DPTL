from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import re

#selenium required
#geckodriver required as well

url = 'https://boels-fr.brico.be/'

fichier = 'boelsBrico.csv'
f = open(fichier, 'w', encoding='utf-8')

titres = 'Title; Text-fr; Prix demi-jour; Prix jour; Prix weekend; Prix Semaine; Garantie; Url; ID; IMG\n'
f.write(titres)

#change that path with the actual path of the geckoDriver.
driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

driver.get(url)

links = []
all_items_link = []

#fetching the categories link.
#ex: '1.Forer et Casser':'https://boels-fr.brico.be/Products/Products?onlineGroupId=f5656e18-c514-e811-a2bd-00155d14203f&homePage=1'
for i in range(1, 9):

    #for viewing purposes
    try:
        cat_path = '/html/body/main/div[3]/div/div['+str(i)+']/a[2]/h3/span'
        #Should apply a text treatment as it is raw text.
        categorie = driver.find_element_by_xpath(cat_path).text
        print('\n----------', categorie, '----------\n')
    
    except NoSuchElementException:
        print(i, 'Category not found.')
        categorie = ''
    
    try:
        link_path = '/html/body/main/div[3]/div/div['+str(i)+']/a[2]'
        link = driver.find_element_by_xpath(link_path).get_attribute('href')
        print(link)
        links.append(link)
    
    except NoSuchElementException:
        print(i, 'link not found.')

#browsing all the categories links.
for l in links:
    driver.get(l)
    driver.implicitly_wait(5)

    print('\n\n', l, '\n')

    container_path = '/html/body/main/div/div'
    container = driver.find_element_by_xpath(container_path).text
    #getting the number of items displayed on the webpage.
    temp = container.split('\n')
    itemsOnPage = len(temp)//3
    
    
    for i in range(1, itemsOnPage+1):
        #getting the link of each item displayed on the webpage
        try:
            item_link_path = '/html/body/main/div/div/div['+str(i)+']/div/div/div[2]/div/a'
            item_link = driver.find_element_by_xpath(item_link_path).get_attribute('href')

            print(item_link)
            all_items_link.append(item_link)
        
        except NoSuchElementException:
            print(i, 'item link not found.')

        #getting the name of each item displayed on the webpage
        try:
            item_name_path = '/html/body/main/div/div/div['+str(i)+']/div/div/div[2]/div/h4'
            item_name = driver.find_element_by_xpath(item_name_path).text

            print(item_name)
        
        except NoSuchElementException:
            print(i, 'item name not found.')
        
        print('-----')

#now that we have all the links items stored in our list, we can iterate though it and
#scrape what we need. (title, description, location, prices, caution,..)
for l in all_items_link:
    try:
        driver.get(l)
        driver.implicitly_wait(5)

        try:
            item_name_path = '/html/body/main/form/div/div[1]/div[3]/h1'
            item_name = driver.find_element_by_xpath(item_name_path).text

            print(item_name)
        
        except NoSuchElementException:
            print('item name not found.\n')
            item_name = 'None'

        try:
            item_description_path = '/html/body/main/form/div/div[1]/div[3]/p'
            item_description_brut = driver.find_element_by_xpath(item_description_path).text

            item_description = item_description_brut.replace(';', ',')

            print(item_description)
        
        except NoSuchElementException:
            print('description not found.\n')
            item_description = 'None'
        
        try:
            half_day_path = '/html/body/main/form/div/div[1]/div[2]/table/tbody/tr[2]/td[2]'
            half_day_price_brut = driver.find_element_by_xpath(half_day_path).text
            temp = re.findall(r'\d+', half_day_price_brut)

            half_day_price = '.'.join(temp)
            print('4h:', half_day_price)
        
        except NoSuchElementException:
            print('half day price not found.\n')
            half_day_price = 'None'

        try:
            day_path = '/html/body/main/form/div/div[1]/div[2]/table/tbody/tr[3]/td[2]'
            day_price_brut = driver.find_element_by_xpath(day_path).text
            temp = re.findall(r'\d+', day_price_brut)

            day_price = '.'.join(temp)
            print('24h:', day_price)

        except NoSuchElementException:
            print('day price not found.\n')
            day_price = 'None'

        try:
            weekend_path = '/html/body/main/form/div/div[1]/div[2]/table/tbody/tr[4]/td[2]'
            weekend_price_brut = driver.find_element_by_xpath(weekend_path).text
            temp = re.findall(r'\d+', weekend_price_brut)

            weekend_price = '.'.join(temp)
            print('weekend:', weekend_price)

        except NoSuchElementException:
            print('weekend price not found.\n')
            weekend_price = 'None'

        try:
            week_path = '/html/body/main/form/div/div[1]/div[2]/table/tbody/tr[5]/td[2]'
            week_price_brut = driver.find_element_by_xpath(week_path).text
            temp = re.findall(r'\d+', week_price_brut)

            week_price = '.'.join(temp)

            print('week:', week_price)

        except NoSuchElementException:
            print('week price not found.\n')
            week_price = 'None'
        
        try:
            caution_path = '/html/body/main/form/div/div[1]/div[2]/table/tbody/tr[6]/td'
            caution_brut = driver.find_element_by_xpath(caution_path).text
            temp = re.findall(r'\d+', caution_brut)
            #temp ex: ['105','00']
            caution = '.'.join(temp)

            print('caution:', caution)
        
        except NoSuchElementException:
            print('caution not found.\n')
            caution = 0
        
        try:
            temp1 = l.split('&')
            temp2 = temp1[0].split('=')
            product_id = temp2[-1]

            print('id:', product_id)
        
        except:
            print('ID not found.')
            product_id = 'None'
        
        try:
            #getting the img link to download it
            img_path = '/html/body/main/form/div/div[1]/div[1]/img'
            img = driver.find_element_by_xpath(img_path).get_attribute('src')
        
            print('image:', img)
        except Exception as e:
            print(e)
            img = 'None'
            

        print(l)
        
        print('------\n')

        f.write(item_name + ';' + item_description + ';' + half_day_price + ';' + day_price + ';' + weekend_price + ';' + week_price + ';' + caution + ';' + l + ';' + product_id + ';' + img + '\n')
    
    except:
        print('An error happened. Rebooting...')
        driver.quit()
        driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

f.close()
driver.quit()