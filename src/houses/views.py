from django.shortcuts import render
from django.views.generic import ListView, CreateView
from extra_views import CreateWithInlinesView

from .models import House, Section
from .forms import HouseForm, SectionFormSet
# Create your views here.


class ListHouse(ListView):
    model = House
    template_name = 'house.html'
    context_object_name = 'houses'  #кастомна назва до якої ми звертаємось в шаблоні

class CreateHouse(CreateWithInlinesView):
    print("Працює")
    model = House
    inlines = [SectionFormSet]
    form_class = HouseForm
    template_name = 'create_house.html'


    def form_valid(self, form):
        print("Дані валідні")
        
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)

        return super().form_invalid(form)