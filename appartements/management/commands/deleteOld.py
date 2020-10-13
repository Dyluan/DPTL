import requests

from django.core.management.base import BaseCommand

from appartements.models import Appartement

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        '''deletes all the objects whose pages lead to a 404 error'''
        listedAppartements = Appartement.objects.all()

        i = 0
        while i < len(listedAppartements):
            temp = requests.get(listedAppartements[i].lien)
            if temp.status_code == 404:
                listedAppartements[i].delete()
            
            if i%10 == 0:
                print('..', i, '..')
            
            i+=1
        
        self.stdout('job complete')