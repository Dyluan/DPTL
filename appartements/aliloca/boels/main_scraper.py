from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

import pandas as pd


driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

driver.maximize_window()
driver.implicitly_wait(5)
driver.get('https://www.boels.be/fr/louer')
driver.implicitly_wait(5)

TVA_path = '/html/body/div[8]/div/div/div[2]/div[2]/div/a[1]'

try:
    pageReadiness = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, TVA_path)))    
    driver.find_element_by_xpath(TVA_path).click()

except TimeoutException:
    TVA_path = '/html/body/div[7]/div/div/div[2]/div[2]/div/a[1]/h3'
    
    pageReadiness = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, TVA_path)))    
    driver.find_element_by_xpath(TVA_path).click()

try:

    f = open('boels.csv', 'w', encoding='utf-8')

    titles = 'nom;id;url;daily_price;weekly_price;description;img_link;tag_list;img_id\n'
    f.write(titles)

    #gets the driver to scroll down the page to make it able to fetch our requirements.
    driver.implicitly_wait(5)
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)
    driver.implicitly_wait(5)

    #gets the MAIN categories
    categories_path = '/html/body/div[5]/div[2]/div[2]/div/div[3]/div[1]/nav[2]/div/ul'
    categories_raw = driver.find_element_by_xpath(categories_path).text

    #here is a list containing all the categories.
    categories = categories_raw.split('\n')

    category_links_list = []
    sub_category_list = []
    dico = {'category':[], 'sub_category':[]}

    all_sub_categories = []
    all_items_links = []

    try:

        for i in range(1, len(categories)+1):
            #gets the link of each category.
            #stores each link to category_links_list list
            category_link_path = '/html/body/div[5]/div[2]/div[2]/div/div[3]/div[1]/nav[2]/div/ul/li['+str(i)+']/a'
            category_link = driver.find_element_by_xpath(category_link_path).get_attribute('href')

            category_links_list.append(category_link)

            
        #looping through each link stored in the category_links_list var. 
        for i in range(len(category_links_list)):
            
            #the driver gets the link of the category and goes to that page.
            driver.get(category_links_list[i])
            driver.implicitly_wait(5)
            
            #makes the driver scrolls down to the bottom of the page to be able to fetch
            #all the subcategories.
            for k in range(4):
                body = driver.find_element_by_css_selector('body')
                body.send_keys(Keys.PAGE_DOWN)
                driver.implicitly_wait(5)
            
            try:
                #little workaround as sometimes refering to categories[i] does not work.
                #this just gets the category name.
                cat_path = '/html/body/div[5]/div[2]/div[3]/div/div/h1'
                cat_final = driver.find_element_by_xpath(cat_path).text
            
            except:
                cat_final = 'None'

            try:
                #gets each sub-category of each main category and prints it out.
                elems = driver.find_element_by_class_name('row').text
                sub_cat = elems.split('\n')

                #getting the links of each sub-category and stores it to all_sub_categories list
                # in order to loop through it and fetch all the items.
                for j in range(1, len(sub_cat)+1):
                    sub_cat_links_path = '/html/body/div[5]/div[2]/div[4]/div/div[2]/section[2]/div/div/div['+str(j)+']/a'
                    sub_cat_links = driver.find_element_by_xpath(sub_cat_links_path).get_attribute('href')
                    all_sub_categories.append(sub_cat_links)

                #print('-----\n')
            
            except NoSuchElementException as e:
                #problem accessing https://www.boels.be/fr/louer/securite/controle-dacces-1
                print('Sub-categories:', sub_cat_links, 'not found.\n', e)
        
        '''nf = pd.DataFrame.from_dict(dico)
        print(nf)
        nf.to_csv('liste_sous_categories.csv', sep=';')'''

        ####################################################
        #ALGORITHM PART II: GETTING THE LINKS OF EVERY ITEM#
        ####################################################

        #browsing through each link stored in all_sub_categories var.
        #then printing out each item associated to that specific sub-category.
        for elem in all_sub_categories:
            print('Sub-category:', elem)
            driver.get(elem)
            driver.implicitly_wait(5)

            try:
                #the only way to get the number of items displayed on each page is to search for the
                #button on the bottom of the item and to count them.
                items_on_the_page = driver.find_elements_by_class_name('product-buttons')

                #browsing thgough each item on the sub-category page
                for i in range(1, len(items_on_the_page)+1):
                            
                    try:
                        item_link_path = '/html/body/div[5]/div[2]/div[4]/div/div[2]/div[2]/div/div/a['+str(i)+']'
                        item_link = driver.find_element_by_xpath(item_link_path).get_attribute('href')

                        all_items_links.append(item_link)

                        print('Link:', item_link)

                    except NoSuchElementException as e:
                        print('Link not found.', e)
                            
                    print('----------\n')
            
            except NoSuchElementException as e:
                print('No items displayed', e)
        
        ####################################################
        #ALGORITHM PART III: GETTING THE INFO WE NEED FROM##
        ########EVERY ITEM (price, name, ID, etc..)#########
        ####################################################

        for link in all_items_links:

            try:

                driver.get(link)
                driver.implicitly_wait(5)

                list_of_tags = ''

                try:
                    container = driver.find_element_by_class_name('product-info-container')

                    total_as = container.find_elements_by_tag_name('a')

                    for a in total_as:
                        if a.get_attribute('data-original-title') != None:
                            temp = a.get_attribute('data-original-title')
                            list_of_tags+=' + ' + temp
                
                    print('List of tags:', list_of_tags)

                except NoSuchElementException as e:
                    print('List of tags:', e)
                    list_of_tags = ''
                
                try:
                    img_path = '/html/body/div[5]/div[2]/div[2]/div/section/div[1]/div[1]/div/div/div[1]/div/div[1]/div[1]/a[1]'
                    img = driver.find_element_by_xpath(img_path).get_attribute('href')

                    print('Image link:', img)

                    boels_id = img.replace(':', '@')
                    boels_id = boels_id.replace('/', '_')
                
                except NoSuchElementException as e:
                    print('Image link:', e)
                    img = ''
                    boels_id = ''

                try:
                    item_name_path = '/html/body/div[5]/div[2]/div[2]/div/header/h1'
                    item_name = driver.find_element_by_xpath(item_name_path).text

                    item_name = item_name.replace(';','')

                    print(item_name)

                except NoSuchElementException as e:
                    print('Item name:', e)
                    item_name = ''
                
                try:
                    id_path ='/html/body/div[5]/div[2]/div[2]/div/section/div[1]/div[3]/div/div/table/tbody/tr[1]/td[1]'
                    id_raw = driver.find_element_by_xpath(id_path).text

                    id = re.findall(r'\d+', id_raw)[0]

                    print('ID:', id)
                
                except Exception as e:
                    print('ID:', e)
                    id = ''
                
                try:
                    ###########
                    ##WARNING##
                    ###########
                    #this might not work as some items don't have a daily price. 
                    # see:https://www.boels.be/fr/louer/energie-eclairage/groupes-de-mats-declairage/eclairage-ballon-stationnaire-led-230-v
                    dl_and_wk_price_raw = driver.find_elements_by_class_name('product-price')

                    #checking if the item's price is present or is on demand.
                    if dl_and_wk_price_raw[0].text == 'p.s.d.':
                        print('Price On Demand.')
                        daily_price = 'p.s.d.'
                        weekly_price = 'p.s.d.'
                    
                    else:
                        try:

                            daily_price_raw = dl_and_wk_price_raw[0].text
                            #the daily price is formatted as follows: 'par jour\n€ 10,89\nTVA 21% comprise'
                            daily_price_temp = daily_price_raw.split('\n')
                            daily_price = daily_price_temp[1]

                            weekly_price_raw = dl_and_wk_price_raw[1].text
                            #the weekly price is formatted as follows: 'par semaine\n€ 10,89\nTVA 21% comprise'
                            weekly_price_temp = weekly_price_raw.split('\n')
                            weekly_price = weekly_price_temp[1]

                        except:
                            print(daily_price, '/day')
                            print(weekly_price, '/week')
                            daily_price = ''
                            weekly_price = ''
                
                except NoSuchElementException as e:
                    print('Price:', e)
                    daily_price = 'p.s.d.'
                    weekly_price = 'p.s.d.'
                
                try:
                    expand = driver.find_element_by_class_name('product-text-expand')
                    expand.click()
                
                except:
                    pass
                
                try:
                    item_desc_raw = driver.find_element_by_class_name('product-text-inner').text

                    item_desc = item_desc_raw.replace('Caractéristiques','')

                    item_desc = item_desc.replace(';',',')

                    item_desc = item_desc.replace('\n','')

                    print('Item desc:', item_desc)
                
                except NoSuchElementException as e:
                    print('Item desc:', e)
                    item_desc = ''
                
                print('----------\n')

            

            except TimeoutException as e:
                print(link, e)
                driver.refresh()
                driver.implicitly_wait(5)
                pass
            
            f.write(item_name + ';' + id + ';'+ link + ';' + daily_price + ';' + weekly_price + ';' + item_desc + ';' + img + ';' + list_of_tags + ';' + boels_id + '\n')
    
    except NoSuchElementException as e:
        print('Link:', e)

except NoSuchElementException as e:
    print('Categories:', e)

f.close()
driver.quit()