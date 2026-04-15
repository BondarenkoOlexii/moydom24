from ninja import NinjaAPI, Schema
from src.houses.models import House, Section, Storey, Apartment
from typing import Optional
from django.db.models import F

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
