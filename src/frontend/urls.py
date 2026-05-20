from django.urls import path

from .views import ContactView, AboutView, ServiceView, MainView, UpdateUserCabinet, ListCabinetUser



urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('about', AboutView.as_view(), name='about'),
    path('services', ServiceView.as_view(), name='services'),
    path('contact', ContactView.as_view(), name='contact'),

    path('cabinet/user/view', ListCabinetUser.as_view(), name='view_user_cabinet'),
]