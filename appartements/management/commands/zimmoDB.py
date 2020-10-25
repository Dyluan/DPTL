from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from django.core.management.base import BaseCommand

from appartements.models import Appartement
import re
import math


class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

		#first, we need to go to the first search page to fetch the number of pages available.
		url = 'https://www.zimmo.be/fr/biens/?status=2&type%5B0%5D=5&type%5B1%5D=1&type%5B2%5D=6&hash=26b58fc8b088a7a5aa4254238b31bd22&priceMax=1800&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=0&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=0&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&excludedEstates%5B0%5D=JPE0S&excludedEstates%5B1%5D=JPP2A&excludedEstates%5B2%5D=JPTPG&excludedEstates%5B3%5D=JQ7OO&region=list&district=MzSEAAMDQxgAAA%253D%253D&pagina=1#gallery'
		
		driver.get(url)
		
		#I should probably go another way.
		#instead of trying to grab all the information available on the Index page
		#I should instead just grab all the links, then get the browser to visit all these links
		#and just THEN, grab all the wanted information: room, price, locality, size
		'''
			surface: /html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[2]/div[1]/ul/li[4]/span
			surface: .main-features > li:nth-child(4) > span:nth-child(2)

			chambres: /html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[2]/div[1]/ul/li[5]/span
			chambres: .main-features > li:nth-child(5) > span:nth-child(2)

			prix: /html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[1]/div[2]/div/span
			prix: .price-value > span:nth-child(2)

			Rue, commune: /html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[1]/div[1]/h2
			Rue, commune: h2.section-title
		'''

		try:
			#the webdriver should first click the Cookies button in order to cath the nb_pages path.
			button_path = '/html/body/div[1]/div/div/div/div/div/div[3]/button[2]/span'
			button = driver.find_element_by_xpath(button_path)

			button.click()
			
			nb_pages_path = '/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul/li[13]/a/span'
			nb_pagesBrut = driver.find_element_by_xpath(nb_pages_path)
			nb_pages = int(nb_pagesBrut.text)

		except:
			print('nombre de pages non spécifié\n')
			driver.quit()
		
		if nb_pages:
			for i in range(1, nb_pages+1):
				url = 'https://www.zimmo.be/fr/biens/?status=2&type%5B0%5D=5&type%5B1%5D=1&type%5B2%5D=6&hash=26b58fc8b088a7a5aa4254238b31bd22&priceMax=1800&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=0&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=0&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&excludedEstates%5B0%5D=JPE0S&excludedEstates%5B1%5D=JPP2A&excludedEstates%5B2%5D=JPTPG&excludedEstates%5B3%5D=JQ7OO&region=list&district=MzSEAAMDQxgAAA%253D%253D&pagina='+str(i)+'#gallery'

				driver.get(url)
				try:
					driver.implicitly_wait(5)
					#pageReadiness = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span:nth-child(3)')))
					pageReadiness = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]')))
					print('Page is ready.')

					print('\n\n----------PAGE', i, '/', nb_pages+1, '----------\n\n')

					#since the divs surrounding the number of rooms/item are not stable, this is a way of retrieving the rooms of each item.
					number_of_rooms_list = driver.find_elements_by_css_selector('span:nth-child(3)')

					#divs surrounding the size of each item not stable. Some undesired elems are selected as well, hence the filtering
					size_list_raw = driver.find_elements_by_css_selector('span:nth-child(2)')
					size_list = []
					#keeping every 'm²' values only, converting them to int and storing them into size_list
					for s in size_list_raw:
						if ('m²' in s.text and s.text != ''):
							try:
								size_list.append(int(s.text[:-2]))
							except ValueError:
								size_list.append(int(math.floor(float(s.text[:-2]))))

					#hardcoded. There are 21 results per page.
					for j in range(1, 22):
						
						incr = 0

						try:
							new_appart_label_path = '/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div['+str(j)+']/div[4]'
							new_appart_label = driver.find_element_by_xpath(new_appart_label_path).text

							if new_appart_label == 'Nouveau':
								#if a record has the 'New' label, then each div is incremented by one.
								#this is ugly but since we are working with xpath, the div n° should be exact.
								incr = 1

							try:
								#this MUST be adjusted as we are getting the full address and we only want the zipcode.
								location_path = '/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div['+str(j)+']/div['+str(6+incr)+']'
								location_text = driver.find_element_by_xpath(location_path).text

								print(location_text)
							
							#exception related to the location_text of each item.
							except :
								print('Location not found.')

							try:
								link_path = '/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div['+str(j)+']/div['+str(4+incr)+']/a'
								link_text = driver.find_element_by_xpath(link_path).get_attribute('href')

								print(link_text)
							
							#exception related to the link_text of each item.
							except:
								print('Link not found.')

							try:
								#size_path = '/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div['+str(j)+']/div['+str(7+incr)+']/span[2]'
								#size_text = driver.find_element_by_xpath(size_path).text

								finalSize = size_list[j-1]
								
								print(finalSize, 'm²')
							
							#exception related to the size of each item.
							except:
								print('Size not found.')
							
							try:
								finalRooms = int(number_of_rooms_list[j-1].text)
								print(finalRooms, 'room(s)')

							#exception related to the rooms of each item. fetched with var: number_of_rooms_list
							except:
								print('Rooms not found.')
							
							try:
								prize_path = '/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div['+str(j)+']/div[1]'
								temp_prize = driver.find_element_by_xpath(prize_path).text
								temp_prize_list = re.findall(r'\d', temp_prize)

								prize = int(''.join(temp_prize_list))

								print(prize, '€\n\n\n')

							#exception related to the cost of each item. temp_prize
							except:
								print('Prize not found.') 

						#exception related to new_appart_label. The famous 'Nouveau' labelled on items.
						except NoSuchElementException:
							print('This item is an advertisement. Nothing to see here..')


				#first exception handled. pageReadiness.
				except TimeoutException:
					print('Page took too much time to load')
					
					
		driver.quit()