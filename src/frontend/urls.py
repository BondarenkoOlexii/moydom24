from django.urls import path

from .views import ContactView, AboutView, ServiceView, MainView, ListCabinetUser, UpdateUserCabinet,\
    ListCabinetMasterRequest, CreateCabinetMasterRequest, ListCabinetTariff, ListCabinetInvoice,\
    CabinetInvoiceDatatableView, CustomUserLogin, CabinetInvoiceView



urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('about', AboutView.as_view(), name='about'),
    path('services', ServiceView.as_view(), name='services'),
    path('contact', ContactView.as_view(), name='contact'),

    path('cabinet/login', CustomUserLogin.as_view(), name='login_user_cabinet'),
    path('cabinet/user/view', ListCabinetUser.as_view(), name='view_user_cabinet'),
    path('cabinet/user/update/<int:pk>', UpdateUserCabinet.as_view(), name='update_user_cabinet'),
    path('cabinet/master-request', ListCabinetMasterRequest.as_view(), name='list_user_master_request'),
    path('cabinet/master-request/create', CreateCabinetMasterRequest.as_view(), name='create_user_master_request'),
    path('cabinet/tariff', ListCabinetTariff.as_view(), name='list_user_tariff'),
    path('cabinet/invoice', ListCabinetInvoice.as_view(), name='list_user_invoice'),
    path('api/datatable/cabinet_invoice', CabinetInvoiceDatatableView.as_view(), name='cabinet_invoice_datatable'),
    path('cabinet/invoice/<int:pk>', CabinetInvoiceView.as_view(), name='cabinet_invoice_view'),
]