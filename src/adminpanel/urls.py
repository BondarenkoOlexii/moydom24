from django.urls import path
from .views import dashboard
from src.houses.views import ListHouse, DetailHouse, CreateHouse, DeleteHouse, UpdateHouse, ApartmentList, CreateApartment, UpdateApartment, DeleteApartmnent, DetailApartment
from src.users.views import ListUser, CreateUser, DeleteUser, UpdateUser, CreateMessage, EmailInvite, ListMessage, SpecificMessage, DeleteMessage, ListMasterRequest, MasterList, CreateMaster
from django.views.generic import TemplateView
from src.adminpanel.api import api

urlpatterns = [
    path('', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
    path('house', ListHouse.as_view(template_name="house.html"), name='house'),
    path('house/<int:pk>', DetailHouse.as_view(), name='detail_house'),
    path('house/create_house', CreateHouse.as_view(template_name="create_house.html"), name='create_house'),
    path('house/update/<int:pk>', UpdateHouse.as_view(template_name="create_house.html"), name='update_house'),
    path('house/delete/<int:pk>', DeleteHouse.as_view(), name='delete_house'),

    path('user', ListUser.as_view(template_name="user.html"), name='user'),
    path('user/create', CreateUser.as_view(template_name="create_user.html"), name='create_user'),
    path('user/update/<int:pk>', UpdateUser.as_view(template_name="create_user.html"), name='update_user'),
    path('user/delete/<int:pk>', DeleteUser.as_view, name='delete_user'),
    path('user/message', CreateMessage.as_view(template_name="new_message.html"), name='new_message'),
    path('user/invite', EmailInvite.as_view(template_name="invite_message.html"), name='invite_message'),

    path('apartment', ApartmentList.as_view(), name='apartment'),
    path('apartment/<int:pk>', DetailApartment.as_view(), name='detail_apartment'),
    path('apartment/create_apartment', CreateApartment.as_view(), name='create_apartment'),
    path('apartment/update/<int:pk>', UpdateApartment.as_view(), name='update_apartment'),
    path('apartment/delete/<int:pk>', DeleteApartmnent.as_view(), name='delete_apartment'),

    path('messages', ListMessage.as_view(), name='messages'),
    path('message/<int:pk>', SpecificMessage.as_view(), name='specific_message'),
    path('message/delete/<int:pk>', DeleteMessage.as_view(), name='delete_message'),

    path('master-request', ListMasterRequest.as_view(), name='request-master-list'),
    path('master-list', MasterList.as_view(), name='master-list'),
    path('master-list/create', CreateMaster.as_view(), name='master-list-create'),

]