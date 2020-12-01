from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from django.core.management.base import BaseCommand
import math
import re

from appartements.models import Appartement


class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		res = get_links()
		get_elements(res)

#TO DO: 
#Check Before anything that the links are not in the database. Only do the job if not. Save some time.
#Handle the possible webdriver connections errors.
#Handle the Captchas. IMPORTANT

''' Bot Captcha
click_path = '/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]'
url = 'http://validate.perfdrive.com/21240cc12f281084e3ed3f9d063dd905/?ssa=c4216176-bda6-4e05-8956-8bd17f617201&ssb=06222218949&ssc=https%3A%2F%2Fwww.zimmo.be%2Ffr%2Fixelles-1050%2Fa-louer%2Fappartement%2FJPD9I%2F%3Fsearch%3D26b58fc8b088a7a5aa4254238b31bd22&ssi=503e4b72-a26d-427d-bc7e-e6c35e9e78ad&ssk=helpdesk@zimmo.be&ssm=9992375920827112623410077088704592&ssn=1fa57f6f1b7c9f7a31083d9356348b7c845352f10c88-6268-4835-ac2e66&sso=5cdd025c-dc36f464f71bd85b460fcd2da3d5b12ffadd219ae286bbd8&ssp=77986054191603707457160378387186880&ssq=41146443702891681688734317694492271226055&ssr=ODEuMTY0Ljk4LjEyOQ==&sst=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64;%20rv:82.0)%20Gecko/20100101%20Firefox/82.0&ssv=&ssw=BGQDbwMwVWkDKld2B25VZVdjB29UIwIlBWYII1QlBzgGOVYxClFRO1I3UiZRbQh9BGwAYVEwUWoCJFUzXDoANQs8XDxXNwdjV2YAbQAxADcEPQNjAzFVYANoVzMHZFVjVzUHMVQyAjcFNAhoVDcHaQZnVmYKPFFqUmtSJlFtCH0EbABjUTJRagIkVW5ceQALC2xcYFcxByNXYgB6AHcAIQQ%2BAyYDPlViA2FXPwd2VWVXYAdjVDgCYQUxCGdUYAdgBmFWfQo1USFSaVI1UWYINAR0ACdRcVE1AnRVWFxoADMLaFxqVyEHc1c8AHoAPgA2BDUDbwMmVR4DPld%2FBz1VOFc%2FBzRULgJjBS0IYFR2B3kGAVY2CmBRNlI8UnNRJQguBBgABlEiUWECNlUpXDkAbwstXFNXPAc%2FVzEAPQA%2FACMEfQNjAzBVaANxV3cHIlVuV2sHZ1QvAmYFKghyVG0HIgZsVm4KPVFoUnFSaFE3CH0EIgANUWNRMwJyVW5cfwA9C3lcfVd3B2pXdAAzADUAMwQ%2FA3cDNVVlA2FXNgdjVWdXZwdmVDACYQUhCGtUKw%3D%3D'
'''


def get_links():

	database_qs = Appartement.objects.all()
	database_urls = []
	#getting all the urls already present in the database
	for elem in database_qs:
		database_urls.append(elem.lien)

	driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")
	url = 'https://www.zimmo.be/fr/biens/?status=2&type%5B0%5D=5&type%5B1%5D=1&type%5B2%5D=6&hash=26b58fc8b088a7a5aa4254238b31bd22&priceMax=1800&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=0&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=0&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&excludedEstates%5B0%5D=JPE0S&excludedEstates%5B1%5D=JPP2A&excludedEstates%5B2%5D=JPTPG&excludedEstates%5B3%5D=JQ7OO&region=list&district=MzSEAAMDQxgAAA%253D%253D&pagina=1#gallery'
	driver.get(url)
	driver.implicitly_wait(3)

	res = []

	try:

		#the webdriver first clicks the Cookies button in order to cath the nb_pages path.
		button_path = '/html/body/div[1]/div/div/div/div/div/div[3]/button[2]/span'
		button = driver.find_element_by_xpath(button_path)

		button.click()

		nb_pages_path = '/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul/li[13]/a/span'
		nb_pagesBrut = driver.find_element_by_xpath(nb_pages_path)
		nb_pages = int(nb_pagesBrut.text)
		print('il y a', nb_pages, 'pages\n\n')

		for i in range(1, nb_pages+1):

			print('\n\n------- PAGE', i,'/', nb_pages+1, '-------\n\n')
			
			driver.implicitly_wait(3)
			url = 'https://www.zimmo.be/fr/biens/?status=2&type%5B0%5D=5&type%5B1%5D=1&type%5B2%5D=6&hash=26b58fc8b088a7a5aa4254238b31bd22&priceMax=1800&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=0&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=0&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&excludedEstates%5B0%5D=JPE0S&excludedEstates%5B1%5D=JPP2A&excludedEstates%5B2%5D=JPTPG&excludedEstates%5B3%5D=JQ7OO&region=list&district=MzSEAAMDQxgAAA%253D%253D&pagina='+str(i)+'#gallery'
			driver.get(url)
			driver.implicitly_wait(3)

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
						link_path = '/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div['+str(j)+']/div['+str(4+incr)+']/a'
						link_text = driver.find_element_by_xpath(link_path).get_attribute('href')

						if link_text not in database_urls:
							res.append(link_text)
							print(link_text)
						
						else:
							print('Link already present in the database')
							
					#exception related to the link_text of each item.
					except:
						print('Link not found.')

				except NoSuchElementException:
					print('This is an AD. Nothing to see here..')
				

	except:
		print('nombre de pages non spécifié\n')
	
	finally:
		driver.quit()
		return res

def get_elements(url_list):
	driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")
	for url in url_list:
		driver.get(url)
		
		try:
			button_path = '/html/body/div[1]/div/div/div/div/div/div[3]/button[2]/span'
			button = driver.find_element_by_xpath(button_path)
			button.click()
		
		except NoSuchElementException:
			pass

		driver.implicitly_wait(3)

		try:
			floor_surface_path = '/html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[2]/div[1]/ul/li[4]/span'
			floor_surface_text = driver.find_element_by_xpath(floor_surface_path).text
			floor_surface = int(math.floor(float(floor_surface_text[:-2])))
			print(floor_surface, 'm²')

		except:
			print('Floor surface not found')
			floor_surface = 0
		
		try:
			nb_rooms_path = '/html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[2]/div[1]/ul/li[5]/span'
			nb_rooms_text = driver.find_element_by_xpath(nb_rooms_path).text
			nb_rooms = int(nb_rooms_text)
			print(nb_rooms, 'rooms available')
		
		except:
			print('Number of rooms not available.')
			nb_rooms = 0
		
		try:
			price_path = '/html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[1]/div[2]/div/span'
			price_path_text = driver.find_element_by_xpath(price_path).text
			#formating the price to make it an int. '€ x.xxx' by default.
			price = int(''.join(re.findall(r'\d+', price_path_text)))
			print(price, '€')
		
		except:
			print('Price not available.')
			price = 0
		
		try:
			#if the full address is not communicated on the webpage.
			location_path = '/html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[1]/div[1]/h2/span[2]'
			location_text = driver.find_element_by_xpath(location_path)
			location = location_text.text
		
		except NoSuchElementException:
			#if the full address is communicated on the webpage.
			#I should then get rid of the street and only keep the locality.
			location_path = '/html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[1]/div[1]/h2/span'
			location_text = driver.find_element_by_xpath(location_path).text
			location = location_text.split(',')[-1]
			location = location[1:]
		
		except:
			location = ''
		
		finally:
			print(location)
		
		try:
			ID_path = '/html/body/div[3]/div[3]/section[1]/div[2]/div/section[2]/div/div[1]/p'
			ID_brut = driver.find_element_by_xpath(ID_path).text
			#formatting because ID_brut == 'Code Zimmo: IDIDIDIDID'
			ID_str = ID_brut.split(':')[-1]
			ID = 'ZIM' + ID_str[1:]
			print(ID)
		
		except:
			print('Unable to locate ID')
			ID = 'empty'
		
		link = url
		print(link, '\n\n')

		#I should first make a system to get an UNIVERSAL ID to all the items in the database
		if floor_surface != 0 and nb_rooms != 0 and price != 0 and location != '' and ID != 'empty':
			try:
				Appartement.objects.create(
					taille = floor_surface,
					prix = price,
					nb_chambres = nb_rooms,
					commune = location,
					lien = url,
					generalID=ID
				)
		
				print(ID, 'Added\n\n')

			except:
				print(ID, 'Already in the database.')
		
	
	driver.quit()