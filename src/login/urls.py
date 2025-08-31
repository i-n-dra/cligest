from django.urls import path
from .views import (
    SignUpView,
    ProfileUpdate,
    ProfileCreateView
    )

urlpatterns = [
    path('registration/', SignUpView.as_view(), name='registration'),
    path('profile-creation/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
]