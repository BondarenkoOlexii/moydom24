from django.urls import path
from django.views.generic import TemplateView
from src.adminpanel.api import api

from .views import dashboard

from src.houses.views import ListHouse, HouseDatatableView, DetailHouse, CreateHouse, DeleteHouse, UpdateHouse, ApartmentList, ApartmentDatatableView, CreateApartment,\
    UpdateApartment, DeleteApartmnent, DetailApartment, ListMasterRequest, NewMasterRequest, DeleteMasterRequest, UpdateMasterRequest

from src.users.views import ListUser, UserDatatableView, CreateUser, DeleteUser, UpdateUser, CreateMessage, EmailInvite, ListMessage,\
    SpecificMessage, DeleteMessage, MasterList, MasterDatatableView, CreateMaster, UpdateMaster, DeleteMaster

from src.settings.views import PaymentInfoCreate, TransactionProposeList, TransactionProposeCreate, TransactionProposeUpdate,\
    TransactionProposeDelete, ServiceView, TariffList, CreateTariff, UpdateTariff, DeleteTariff, RoleView, ListCounter, \
    CreateCounter, DetailListCounter, UpdateCounter, DeleteCounter

from src.site_control.views import CreateMainPageView, CreateAboutPageView, CreateContactPageView, CreateServicePageView

from src.finance.views import AccountList, CreateAccount, UpdateAccount, DeleteAccount, AccountDetail, ListInvoice, \
    CreateInvoice, InvoiceDatatableView, UpdateInvoice, DeleteInvoice, DetailInvoice

urlpatterns = [
    path('', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),

    path('api/datatable/house', HouseDatatableView.as_view(), name='house_datatable'),
    path('api/datatable/apartment', ApartmentDatatableView.as_view(), name='apartment_datatable'),
    path('api/datatable/user', UserDatatableView.as_view(), name='user_datatable'),
    path('api/datatable/master', MasterDatatableView.as_view(), name='master_datatable'),
    path('api/datatable/invoice', InvoiceDatatableView.as_view(), name='invoice_datatable'),

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
    path('master-request/create', NewMasterRequest.as_view(), name='request-master-create'),
    path('master-request/update/<int:pk>', UpdateMasterRequest.as_view(), name='request-master-update'),
    path('master-request/delete/<int:pk>', DeleteMasterRequest.as_view(), name='request-master-delete'),


    path('master-list', MasterList.as_view(), name='master-list'),
    path('master-list/create', CreateMaster.as_view(), name='master-list-create'),
    path('master-list/update/<int:pk>', UpdateMaster.as_view(), name='master-list-update'),
    path('master-list/delete/<int:pk>', DeleteMaster.as_view(), name='master-list-delete'),

    path('pay-company', PaymentInfoCreate.as_view(), name='pay-company'),
    path('transaction-purpose', TransactionProposeList.as_view(), name='transaction-purpose'),
    path('transaction-purpose/create', TransactionProposeCreate.as_view(), name='transaction-purpose_create'),
    path('transaction-purpose/update/<int:pk>', TransactionProposeUpdate.as_view(), name='transaction-purpose_update'),
    path('transaction-purpose/delete/<int:pk>', TransactionProposeDelete.as_view(), name='transaction-purpose_delete'),

    path('service', ServiceView.as_view(), name='service'),
    path('tariff', TariffList.as_view(), name='tariff'),
    path('tariff/create', CreateTariff.as_view(), name='create_tariff'),
    path('tariff/update/<int:pk>', UpdateTariff.as_view(), name='update_tariff'),
    path('tariff/delete/<int:pk>', DeleteTariff.as_view(), name='delete_tariff'),

    path('role', RoleView.as_view(), name='role'),

    path('website/main', CreateMainPageView.as_view(), name='website-main'),
    path('website/about', CreateAboutPageView.as_view(), name='website-about'),
    path('website/contact', CreateContactPageView.as_view(), name='website-contact'),
    path('website/service', CreateServicePageView.as_view(), name='website-service'),

    path('account', AccountList.as_view(), name='account'),
    path('account/<int:pk>', AccountDetail.as_view(), name='show_account'),
    path('account/create', CreateAccount.as_view(), name='account_create'),
    path('account/update/<int:pk>', UpdateAccount.as_view(), name='account_update'),
    path('account/delete/<int:pk>', DeleteAccount.as_view(), name='account_delete'),

    path('counter', ListCounter.as_view(), name='counter'),
    path('counter/counter-list', DetailListCounter.as_view(), name='counter-list'),
    path('counter/create', CreateCounter.as_view(), name='counter_create'),
    path('counter/update/<int:pk>', UpdateCounter.as_view(), name='counter_update'),
    path('counter/delete/<int:pk>', DeleteCounter.as_view(), name='counter_delete'),

    path('invoice', ListInvoice.as_view(), name='invoice'),
    path('invoice/<int:pk>', DetailInvoice.as_view(), name='invoice_detail'),
    path('invoice/create', CreateInvoice.as_view(), name='invoice_create'),
    path('invoice/update/<int:pk>', UpdateInvoice.as_view(), name='invoice_update'),
    path('invoice/delete/<int:pk>', DeleteInvoice.as_view(), name='invoice_delete')


]