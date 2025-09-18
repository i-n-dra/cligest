from django.shortcuts import render
import time
from django.contrib.auth.models import User
from login.models import Profile
from .models import Client
from django.views.generic import DetailView, ListView

# Create your views here.
def home(request):
    return render(request, 'index.html')

# mensaje dia/tarde
def horario_am():
    hora = time.localtime().index(3) # index 3 -> tm_hour
    if hora > 12: 
        return False
    elif hora < 12:
        return True

def request_user_role(username):
    profile = Profile.objects.filter(user__username=username).first()
    if profile and profile.role:
        role = profile.role.name
    else:
        role = 'Sin cargo'
    return role

class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    ordering = ['last_name_1_rep_legal']

def ClientCreateView():
    pass