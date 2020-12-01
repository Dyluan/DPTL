from django import forms
from .models import Appartement

class ContactForm(forms.ModelForm):

    class Meta:
        model = Appartement
        fields = ('taille', 'prix', 'nb_chambres', 'commune', 'lien', 'generalID') 

    '''name = forms.CharField()
    email = forms.CharField(max_length=100)
    password = forms.CharField()'''