from django.urls import path
from .views import (
    SignUpView,
    UserUpdateView,
    ProfileUpdate,
    ProfileCreateView,
    RolePermissionListView
    )

urlpatterns = [
    path('registration/', SignUpView.as_view(), name='registration'),
    path("update-user/<int:pk>/", UserUpdateView.as_view(), name="update-user"),
    path('profile-creation/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
    path('roles-y-permisos/', RolePermissionListView.as_view(), name='listar-roles-permisos')
]