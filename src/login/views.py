from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from .models import Profile, Role
from .forms import (
    ProfileForm,
    ProfileCreateForm,
    UserForm
    )
from django.contrib.auth.models import Permission, User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.decorators.cache import never_cache #se podría usar, en la app la sesión queda abierta al abrir de nuevo el exe

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
    def get_form(self, form_class = None):
        form = super(SignUpView, self).get_form()

        form.fields['username'].widget = forms.TextInput(
            attrs={'class': 'input'}
        )
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'input'}
        )
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'input'}
        )
        
        return form    

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('profile')

@method_decorator(permission_required('auth.add_profile', raise_exception=True), name='dispatch')
class ProfileCreateView(CreateView):
    form_class = ProfileCreateForm
    success_url = reverse_lazy('profile')
    template_name = 'profile/profile_create.html'

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'profile/ver_profile.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user = self.request.user)
        return profile

class RolePermissionListView(ListView):
    @method_decorator(login_required)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        roles = Group.objects.all()
        permisos = Permission.objects.all()
        context = {
            'roles': roles,
            'permisos': permisos
        }
        return render(request, 'roles_permisos/listar.html', context)