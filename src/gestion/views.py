from django.shortcuts import render
import time
from django.contrib.auth.models import User
from login.models import Profile

# Create your views here.
def home(request):
    return render(request, 'index.html')

# mensaje dia/tarde
def horario_am():
    if time.localtime().index(3) > 12: # index 3 -> tm_hour
        return False
    else:
        return True

def request_user_role(username):
    profile = Profile.objects.filter(user__username=username).first()
    if profile and profile.role:
        role = profile.role.name
    else:
        role = 'Sin cargo'
    return role