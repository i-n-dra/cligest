from django.urls import path
from .views import SignUpView, ProfileUpdate

urlpatterns = [
    path('registration/', SignUpView.as_view(), name='registration'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
]