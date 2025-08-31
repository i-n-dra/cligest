from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture',
            'phone_number',
        ]
        labels = {
            'profile_picture': 'Foto de perfil',
            'phone_number': 'Teléfono/Celular',
        }
        widgets = {
            'profile_picture': forms.FileInput(),
        }

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'run',
            'date_of_birth',
            'phone_number',
            'profile_picture',
        ]
        labels = {
            'profile_picture': 'Foto de perfil',
            'phone_number': 'Teléfono/Celular',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.FileInput(),
        }
