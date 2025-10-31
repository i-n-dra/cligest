from django.urls import path
from .views import (
    SignUpView,
    UserUpdateView,
    ProfileUpdate,
    ProfileCreateView,
    RolePermissionListView,
    UsersProfilesListView,
    UserGroupUpdateView,
    ProfileDetailView
    )

urlpatterns = [
    path('registration/', SignUpView.as_view(), name='registration'),
    path("update-user/<int:pk>/", UserUpdateView.as_view(), name="update-user"),
    path('profile-creation/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
    path('roles-y-permisos/', RolePermissionListView.as_view(), name='list_r_p'),
    path('usuarios-y-perfiles/', UsersProfilesListView.as_view(), name='list_u_p'),
    path('usuarios-y-perfiles/<int:pk>', ProfileDetailView.as_view(), name='detail_u_p'),
    path('usuarios-y-perfiles/<int:pk>/grupos', UserGroupUpdateView.as_view(), name='change_u_p')
]