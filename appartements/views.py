from django.shortcuts import render
from django.views import generic

from .filters import AppartementFilter
from .models import Appartement

#class IndexView(generic.TemplateView):
class IndexView(generic.ListView):
    model = Appartement
    template_name = 'appartements/index.html'
    paginate_by = 15
    queryset = Appartement.objects.all().order_by('prix')
    context_object_name = 'latest_appartements'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        myFilter = AppartementFilter(data=self.request.GET)

        #filter is the name of the filter being called in the html
        context['filter'] = myFilter

        return context

    #allows to filter the view depending on the form
    def get_queryset(self):
        qs = self.model.objects.all().order_by('prix')
        Appartement_filtered_list = AppartementFilter(self.request.GET, queryset=qs)

        return Appartement_filtered_list.qs


class DetailView(generic.DetailView):
    model = Appartement
    template_name = 'appartements/detail.html'

    def get_queryset(self):
        return Appartement.objects.all()
