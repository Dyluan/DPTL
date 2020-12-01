from django.shortcuts import render
from django.views import generic

from .forms import ContactForm
from .filters import AppartementFilter
from .models import Appartement

class FormView(generic.FormView):
    template_name = 'appartements/loginIndex.html'
    form_class = ContactForm


#class IndexView(generic.TemplateView):
class IndexView(generic.ListView):
    model = Appartement
    template_name = 'appartements/index.html'
    paginate_by = 15
    queryset = Appartement.objects.all().order_by('prix', '-taille')
    context_object_name = 'latest_appartements'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        myFilter = AppartementFilter(data=self.request.GET)

        #filter is the name of the filter being called in the html
        context['filter'] = myFilter

        return context

    #the queryset above informs django the queryset to perform. This is equal to this funtion.
    #BUT this is needed here as I use the a django-filter to filter the results.
    def get_queryset(self):
        qs = self.model.objects.all().order_by('prix', '-taille')
        Appartement_filtered_list = AppartementFilter(self.request.GET, queryset=qs)

        return Appartement_filtered_list.qs


class DetailView(generic.DetailView):
    model = Appartement
    template_name = 'appartements/detail.html'

    #It looks like informating model = Appartement equals to that get_queryset function.
    #def get_queryset(self):
    #    return Appartement.objects.all()
