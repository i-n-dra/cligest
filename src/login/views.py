from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from .models import Profile
from .forms import (
    ProfileForm,
    ProfileCreateForm,
    UserForm,
    UserGroupForm
    )
from django.contrib.auth.models import Permission, User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
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

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('profile')

@method_decorator([login_required, permission_required('auth.delete_user', raise_exception=True)], name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = "usuarios_perfiles/delete.html"
    success_url = reverse_lazy('list_u_p')

@method_decorator([login_required, permission_required('auth.change_user', raise_exception=True)], name='dispatch')
class UserGroupUpdateView(UpdateView):
    model = User
    form_class = UserGroupForm
    template_name = 'usuarios_perfiles/update.html'
    success_url = reverse_lazy('list_u_p')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Cambiar grupos de {self.object.username}"
        return context
    def form_valid(self, form):
        user = self.get_object()
        user.groups.set(form.cleaned_data['groups'])
        user.save()
        return redirect(self.success_url)

@method_decorator(login_required, name='dispatch')
class ProfileCreateView(CreateView):
    form_class = ProfileCreateForm
    success_url = reverse_lazy('profile')
    template_name = 'profile/profile_create.html'

@method_decorator([login_required, permission_required(["auth.view_user"], raise_exception=True)], name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'usuarios_perfiles/detail.html'
    context_object_name = 'p'

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'profile/ver_profile.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user = self.request.user)
        return profile
    
class UsersProfilesListView(ListView):
    @method_decorator(login_required)
    @method_decorator(never_cache)
    @method_decorator(permission_required(["auth.view_user"]))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        profiles = Profile.objects.all()
        context = {
            'usuarios': users,
            'perfiles': profiles
        }
        return render(request, 'usuarios_perfiles/list.html', context)