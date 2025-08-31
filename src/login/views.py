from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileForm
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
    form_class = UserChangeForm
    success_url = reverse_lazy('profile')
    

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'profile.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user = self.request.user)
        return profile