from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from django.core.management.base import BaseCommand

from appartements.models import Appartement
import re


class Command(BaseCommand):

	def handle(self, *args, **kwargs):

		driver = webdriver.Firefox(executable_path = "C:\\Users\\Dylan\\Documents\\python\\geckodriver-v0.26.0-win64\\geckodriver.exe")

		url = 'https://www.immoweb.be/fr/recherche/maison-et-appartement/a-louer/bruxelles/arrondissement?countries=BE&maxPrice=1400&page=1&orderBy=relevance'

		driver.get(url)
		driver.implicitly_wait(3)
		#maybe fix
		myBdd_qs = Appartement.objects.filter(generalID='empty')
		my_lien_list = []

		for elem in myBdd_qs:
			my_lien_list.append(elem.lien)

		try:
			nb_pages_path = '/html/body/div[1]/div[2]/div/main/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/nav/ul/li[4]/a/span[2]'
			nb_pagesBrut = driver.find_element_by_xpath(nb_pages_path)
			nb_pages = int(nb_pagesBrut.text)
			print('il y a', nb_pages, 'pages\n\n')
		except:
			print('nombre de pages non spécifié\n')


		if nb_pages:
			#si le nb de pages est précisé, on boucle le programme sur le nombre de pages total
			for i in range(1, nb_pages+1):
				url = 'https://www.immoweb.be/fr/recherche/maison-et-appartement/a-louer/bruxelles/arrondissement?countries=BE&maxPrice=1800&page='+str(i)+'&orderBy=relevance'

				try:
					driver.get(url)
					driver.implicitly_wait(3)

					print('\n\n----------PAGE', i, '----------\n\n')

					apparts = driver.find_elements_by_css_selector('#main-content li')
					for i in range(1, len(apparts)+1):
						
						try:
							lien_path = '/html/body/div[1]/div[2]/div/main/div/div[2]/div/div[3]/div/div/div[1]/div/ul/li['+str(i)+']/article/div[1]/h2/a'
							lien_text = driver.find_element_by_xpath(lien_path).get_attribute('href')

							if lien_text not in my_lien_list:
								
								try:
									prix_path = '/html/body/div[1]/div[2]/div/main/div/div[2]/div/div[3]/div/div/div[1]/div/ul/li['+str(i)+']/article/div[1]/p/span/span[2]'
									prix = driver.find_element_by_xpath(prix_path)

									temp = re.findall(r'\d+', prix.text)

									prixNet = int(temp[0])
									chargesNet = int(temp[1])

									print(prixNet, '€ +', chargesNet, '€ de charges')
									
								except:
									print('prix non affiché', i)

								try:
									comm_path = '/html/body/div[1]/div[2]/div/main/div/div[2]/div/div[3]/div/div/div[1]/div/ul/li['+str(i)+']/article/div[1]/div[1]/p[2]'
									commune = driver.find_element_by_xpath(comm_path)

									communeNet = commune.text

									print(communeNet)
								except:
									print('commune non précisée', i)

								try:
									tailleEtchpath = '/html/body/div[1]/div[2]/div/main/div/div[2]/div/div[3]/div/div/div[1]/div/ul/li['+str(i)+']/article/div[1]/div[1]/p[1]'
									tailleEtch = driver.find_element_by_xpath(tailleEtchpath)

									#tailleEtch est au format [1, 1, 65], le nb de chambres étant répété 2 fois au début.
									exp = re.findall(r'\d+', tailleEtch.text)

									if len(exp) == 1:
										nb_ch = 1
									else:
										nb_ch = int(exp[0])

									taille = int(exp[-1])

									print(nb_ch, 'chambres')
									print(taille, 'm²')

								except:
									print('taille et nb_chambres non précisé')

								print('\n-------\n')

								try:
									Appartement.objects.create(
										taille = taille,
										prix = prixNet,
										nb_chambres = nb_ch,
										commune = communeNet,
										lien = lien_text,
										generalID='empty')
									print('%s added' % (lien_text))
								except:
									print('%s already exists' % (lien_text))

							
							else:
								print('lien déjà dans la base de données.')

						except:
							print('lien non dispo')
				except TimeoutException as e:
					print(e)
					driver.get(url)
					driver.implicitly_wait(3)

					
					
		driver.close()
		self.stdout('job complete')