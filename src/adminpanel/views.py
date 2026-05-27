from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.users.models import User

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard.html')

