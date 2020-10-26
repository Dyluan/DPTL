import requests
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from appartements.models import Appartement

from django.core.management.base import BaseCommand


'''from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "normal"  #  complete
#caps["pageLoadStrategy"] = "eager"  #  interactive
#caps["pageLoadStrategy"] = "none"
driver = webdriver.Firefox(desired_capabilities=caps, executable_path=r'C:\path\to\geckodriver.exe')
driver.get("http://google.com")'''

#https://stackoverflow.com/questions/31876672/stop-infinite-page-load-in-selenium-webdriver-python
class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "none"  

        driver = webdriver.Firefox(desired_capabilities=caps, executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

        #WARNING: ImmoID doesnt exist anymore. Has been replaced by GeneralID, a String.

        #gets the list of all the appartements in the database which GeneralID is empty
        listedAppartements = Appartement.objects.filter(generalID='empty')

        IDPath = '/html/body/div[1]/div[2]/div/div/main/div[1]/div[2]/div/div/div[1]/div/div[2]/div[3]'

        for elem in listedAppartements:

            if elem.immoID == 0:

                url = elem.lien

                try:

                    driver.get(url)

                    try:

                        driver.implicitly_wait(1)

                        IDBrut = driver.find_element_by_xpath(IDPath)

                        IDBrutList = re.findall(r'\d+', IDBrut.text)
                        #maybe fix that part
                        finalID = 'IMM' + IDBrutList[0]

                        try:
                            print('----',finalID, '----')
                            #maybe fix
                            elem.generalID = finalID
                            elem.save()
                            print('ID updated')

                        except Exception as e:
                            print('New ID not working properly. Exception raised.', e)

                    except TimeoutException:
                        print('Loading took too much time.')
                        driver.close()
                        driver = webdriver.Firefox(desired_capabilities=caps, executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")
                        driver.get(url)

                    

                except:
                    print('404 exception raised.')
            
            else:
                print('No need to assign a new ID')
        
        driver.close()