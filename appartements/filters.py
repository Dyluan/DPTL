import django_filters

from .models import Appartement

class AppartementFilter(django_filters.FilterSet):

    #prix_lt = django_filters.NumberFilter(field_name='prix', lookup_expr='lte')
    prix_liste = django_filters.ChoiceFilter(field_name='prix', choices=Appartement.PRIX_CHOICES, lookup_expr='lte')

    class Meta:
        model = Appartement
        fields = ['prix', 'nb_chambres']
        