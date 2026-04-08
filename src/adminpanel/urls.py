from django.urls import path
from .views import dashboard
from src.houses.views import ListHouse, CreateHouse, DeleteHouse, UpdateHouse, ApartmentList, CreateApartment
from src.users.views import ListUser, CreateUser, DeleteUser, UpdateUser
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
    path('house', ListHouse.as_view(template_name="house.html"), name='house'),
    path('house/create_house', CreateHouse.as_view(template_name="create_house.html"), name='create_house'),
    path('house/update/<int:pk>', UpdateHouse.as_view(template_name="update_house.html"), name='update_house'),
    path('house/delete/<int:pk>', DeleteHouse.as_view(), name='delete_house'),

    path('user', ListUser.as_view(template_name="user.html"), name='user'),
    path('user/create', CreateUser.as_view(template_name="create_user.html"), name='create_user'),
    path('user/update/<int:pk>', UpdateUser.as_view(template_name="create_user.html"), name='update_user'),
    path('user/delete/<int:pk>', DeleteUser.as_view, name='delete_user'),

    path('apartment', ApartmentList.as_view(), name='apartment'),
    path('create_apartment', CreateApartment.as_view(), name='create_apartment'),

]