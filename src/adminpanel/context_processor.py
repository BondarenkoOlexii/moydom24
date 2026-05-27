from django.http import response

from src.houses.models import Apartment
from src.finance.models import Invoice

def aside_bar(request):
    if request.user.is_authenticated:
        user = request.user

        apartments = Apartment.objects.filter(owner=user)
        return {'apartments': apartments}
    return {'': ''}
