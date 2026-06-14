from ninja import NinjaAPI, Schema, Query
from typing import Optional, List
from django.db.models import F
from django.core.paginator import Paginator



from src.houses.models import House, Section, Storey, Apartment
from src.settings.models import Service, Tariff, Tarrif_Service_Price, Counters, TransactionPurpose
from src.users.models import User, Role
from src.finance.models import Payment_Account

api = NinjaAPI()

class GenericOutPoint(Schema):
    id: int
    text: str


@api.get("/house/", response=list[GenericOutPoint])
def get_house(request, q: str = None):
    house = House.objects.all().annotate(text=F('name'))

    if q:
        house = house.filter(name__icontains=q)
    return house

@api.get("/section/", response=list[GenericOutPoint])
def get_section(request, house_id: Optional[int] = None):
    print('Хаус Айди прилетів', house_id)

    if not house_id:
        return []

    section = Section.objects.filter(house_id=house_id).annotate(text=F('name'))
    return section

@api.get("/storey/", response=list[GenericOutPoint])
def get_storey(request, house_id: int):
    storey = Storey.objects.filter(house_id=house_id).annotate(text=F('name'))
    return storey

@api.get("/apartment/", response=list[GenericOutPoint])
def get_apartment(request, house_id: int, section_id: Optional[int] = None, storey_id: Optional[int] = None):
    apartment = Apartment.objects.filter(house_id=house_id).annotate(text=F('apartment_number'))
    if section_id:
        apartment = apartment.filter(section_id=section_id)
    if storey_id:
        apartment = apartment.filter(storey_id=storey_id)

    return apartment

@api.get("/tariff/", response=list[GenericOutPoint])
def get_tariff(request):
    tariff = Tariff.objects.all().annotate(text=F('name'))
    return tariff


@api.get('/bank_book_ids/', response=List[GenericOutPoint])
def get_list_bank_book(request, owner_id: int):
    apartments = Apartment.objects.filter(owner=owner_id)

    payment_account = Payment_Account.objects.filter(apartment__in=apartments).annotate(text=F('bank_book'))

    return payment_account

@api.get("/article/", response=List[GenericOutPoint])
def get_article(request):
    articles = TransactionPurpose.objects.all().annotate(text=F('name'))
    return articles

# Окрема схема яка працює трошечки по іншому через іншу схему

class PaymentOutPoint(Schema):
    id: int
    text: str
    full_name: str
    phone_number: str


@api.get("/payment_account/", response=list[PaymentOutPoint])
def get_payment_account(request, apartment_id: int):
    payment_account = Payment_Account.objects.filter(apartment_id=apartment_id).first()
    user = Apartment.objects.filter(id=apartment_id).first()
    user_info = user.owner

    full_name = ""
    phone = ""
    result = []

    if user_info:
        full_name = f"{user_info.first_name} {user_info.middle_name} {user_info.last_name}"

        phone = getattr(user_info, 'phone_number', '')



    result.append({
        "id": payment_account.id,
        "text": payment_account.bank_book,
        "full_name": full_name,
        "phone_number": phone
    })

    return result


class BankBookOutPoint(Schema):
    full_name: str
    phone_number: str


@api.get("/bank_book/", response=List[BankBookOutPoint])
def get_book_info(request, apartment_id: int):
    user = Apartment.objects.filter(id=apartment_id).first()
    user_info = user.owner

    full_name = ""
    phone = ""
    result = []

    if user_info:
        full_name = f"{user_info.first_name} {user_info.middle_name} {user_info.last_name}"

        phone = getattr(user_info, 'phone_number', '')

    result.append({
        "full_name": full_name,
        "phone_number": phone
    })
    return result




class MeasurementOut(Schema):
    unit: str


@api.get("/get-measurement/", response=MeasurementOut)
def get_measurement(request, service_id: int):
    try:
        print("Пройшов try")
        service = Service.objects.select_related('measurement').get(id=service_id)
        print(service)
        if service:
            print('service існує')
            return {'unit': str(service.measurement.unit_of_measurement)}

    except Exception as e:
        print(e)
        return {'unit': '-----'}





class InvoiceTariff(Schema):
    measurement: str
    price: int


@api.get("/get-service/", response=list[InvoiceTariff])
def get_invoice_service(request, service_id: int, tariff_id: int):
    service = Service.objects.filter(id=service_id).first()
    tariff = Tariff.objects.filter(id=tariff_id).first()
    thoughprice = Tarrif_Service_Price.objects.filter(tariff=tariff_id, service=service_id).first()

    measurement = service.measurement.unit_of_measurement
    price = thoughprice.price

    return {'measurement': measurement, 'price': price}




class TariffService(Schema):
    service_id: int
    price: int
    measurement: int


@api.get("/tariff/{tariff_id}/service", response=list[TariffService])
def get_tariff_services(request, tariff_id: int):
    tariff = Tariff.objects.filter(id=tariff_id).first()

    services = Tarrif_Service_Price.objects.filter(tariff=tariff_id)

    result = []

    for service in services:
        price = Tarrif_Service_Price.objects.filter(tariff=tariff_id, service=service.id).first()
        result.append({
            "service_id": service.service.id,
            "price": price.price,
            "measurement": service.service.measurement.id
        })

    return result


class InvoiceCounter(Schema):
    counter_id: int
    indicator: float
    service_id: int


@api.get("invoice/counters", response=list[InvoiceCounter])
def get_invoice_counter(request, apartment_id: int, service_ids: List[int] = Query([])):
    counter = Counters.objects.filter(service__in=service_ids, apartment=apartment_id)

    result = []

    for i in counter:
        result.append({
            'counter_id': i.id,
            'indicator': i.indicator,
            'service_id': i.service_id})

    return result


@api.get("cabinet/master_request", response=List[GenericOutPoint])
def apartment_for_master(request):

    if request.user.is_authenticated:
        user = request.user.id
        print(f'Юзер - {request.user.first_name} {request.user.last_name}')

        apartments = Apartment.objects.filter(owner=user).annotate(text=F('apartment_number'))
    return apartments

# class MasterRequestOut(Schema):
#     id: int
#     text: str
#
# class PaginatedServiceOut(Schema):
#     results: list[MasterRequestOut]
#     pagination: dict
#
# @api.get("/user-lazy-out/")
# def get_user_master_request(request, name: str="", page: int=1):
#     query_set = User.objects.all()
#
#     if name:
#         query_set.filter(name__icontains=name)
#
#     paginator = Paginator(query_set, 20)
#     current_page = paginator.get_page(page)
#
#     results = [{"id": obj.id, "text": obj.name} for obj in current_page.object_list]
#
#     return {
#         "results": results,
#         "pagination": {"more": current_page.has_next()}
#     }
#
# @api.get("/apartment-lazy-out/")
# def get_apartment_master_request(request, user_id: int, page: int=1):
#     apartment = Apartment.objects.filter(owner=user_id)
#
#     paginator = Paginator(apartment, 10)
#     current_page = paginator.get_page(page)
#
#     results = [{"id": obj.id, "text": obj.apartment_number} for obj in current_page.object_list]
#
#     return {
#         "results": results,
#         "pagination": {"more": current_page.has_next()}
#     }
#


