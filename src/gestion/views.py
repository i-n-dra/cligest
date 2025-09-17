from django.shortcuts import render
import time
from django.contrib.auth.models import User
from login.models import Profile

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