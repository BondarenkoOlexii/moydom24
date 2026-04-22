from ninja import NinjaAPI, Schema
from src.houses.models import House, Section, Storey, Apartment
from src.settings.models import Service
from src.users.models import User, Role
from typing import Optional
from django.db.models import F
from django.core.paginator import Paginator


api = NinjaAPI()

class GenericOutPoint(Schema):
    id: int
    text: str



@api.get("/section/", response=list[GenericOutPoint])
def get_section(request, house_id: int):
    section = Section.objects.filter(house_id=house_id).annotate(text=F('name'))
    return section

@api.get("/storey/", response=list[GenericOutPoint])
def get_storey(request, house_id: int):
    storey = Storey.objects.filter(house_id=house_id).annotate(text=F('name'))
    return storey

@api.get("/apartment/", response=list[GenericOutPoint])
def get_apartment(request, house_id: int, section_id: Optional[str] = None, storey_id: Optional[str] = None):
    apartment = Apartment.objects.filter(house_id=house_id).annotate(text=F('apartment_number'))
    if section_id:
        apartment = apartment.filter(section_id=section_id)
    if storey_id:
        apartment = apartment.filter(storey_id=storey_id)

    return apartment



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



class MasterRequestOut(Schema):
    id: int
    text: str

class PaginatedServiceOut(Schema):
    results: list[MasterRequestOut]
    pagination: dict

@api.get("/user-lazy-out/")
def get_user_master_request(request, name: str="", page: int=1):
    query_set = User.objects.all()

    if name:
        query_set.filter(name__icontains=name)

    paginator = Paginator(query_set, 20)
    current_page = paginator.get_page(page)

    results = [{"id": obj.id, "text": obj.name} for obj in current_page.object_list]

    return {
        "results": results,
        "pagination": {"more": current_page.has_next()}
    }

@api.get("/apartment-lazy-out/")
def get_apartment_master_request(request, user_id: int, page: int=1):
    apartment = Apartment.objects.filter(owner=user_id)

    paginator = Paginator(apartment, 10)
    current_page = paginator.get_page(page)

    results = [{"id": obj.id, "text": obj.apartment_number} for obj in current_page.object_list]

    return {
        "results": results,
        "pagination": {"more": current_page.has_next()}
    }


# class MasterOut(Schema):
#     id: int
#     user_id: int
#
# @api.get("/master-lazy-out/", response=list[MasterOut])
# def get_specification_master(request, role_type: str = None):
#     print(role_type)
#     same_role = Role.objects.all()
#
#     if role_type:
#         same_role = Role.objects.filter(user=role_type)
#
#     print(same_role)
#
#     return list(same_role)
