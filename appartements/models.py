from django.db import models

# I better be adding the Immoweb ID to the model as well as some appartements are uploaded 
# multiple times on the website

#https://docs.djangoproject.com/fr/3.1/ref/models/fields/#enumeration-types

#TO DO:: make the immoID unique after giving a value to each
class Appartement(models.Model):
    LOW = 300
    LOW_TO_MID = 450
    MID = 600
    MID_TO_HIGH = 900
    HIGH_TO_VHIGH = 1400
    HIGH = 1800
    
    PRIX_CHOICES = [
        (LOW, '< 300€'),
        (LOW_TO_MID, '< 450€'),
        (MID, '< 600€'),
        (MID_TO_HIGH, '< 900€'),
        (HIGH_TO_VHIGH, '< 1400€'),
        (HIGH, '< 1800€'),
    ]


    taille = models.IntegerField()
    prix = models.IntegerField(choices=PRIX_CHOICES)
    nb_chambres = models.IntegerField()
    commune = models.CharField(max_length=100)
    lien = models.CharField(max_length=300, unique=True)
    immoID = models.IntegerField(default=0)

    def dans_mes_moyens(self):
        return self.cout_par_chambre <= 600

    def cout_par_chambre(self):
        return self.prix // self.nb_chambres
    
    def cout_par_metre(self):
        return self.prix // self.taille
    
    def __str__(self):
        return str(self.prix) + '€ ' + self.commune

#allows to delete all the duplicates 'immoID' in the database
#for immoID in Appartement.objects.values_list('immoID', flat=True).distinct(): 
#   Appartement.objects.filter(pk__in=Appartement.objects.filter(immoID=immoID).values_list('id', flat=True)[1:]).delete()