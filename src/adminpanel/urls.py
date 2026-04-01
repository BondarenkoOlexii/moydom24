from django.urls import path
from .views import dashboard
from src.houses.views import ListHouse, CreateHouse
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
    path('house', ListHouse.as_view(template_name="house.html"), name='house'),
    path('house/create_house', CreateHouse.as_view(template_name="create_house.html"), name='create_house')
]