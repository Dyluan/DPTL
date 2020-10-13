from django.test import TestCase

# Create your tests here.
from appartements.models import Appartement

class DuplicateTestCase(TestCase):
    def test_duplicate_dont_add_to_bdd(self):
        '''test the unique property of the 'lien' field.
        Adding an already existing lien to the database should not work'''
        temp = Appartement.objects.all()
        initSize = len(temp)
        temp_object = Appartement.objects.get(pk=1)
        print(temp_object)
        Appartement.objects.create(
            taille = temp_object.taille,
            prix = temp_object.prix,
            nb_chambres = temp_object.nb_chambres,
            commune = temp_object.commune,
            lien = temp_object.lien
        )
        temp2 = Appartement.objects.all()
        finalSize = len(temp2)

        self.assertEqual(initSize, finalSize)