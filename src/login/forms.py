from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'role',
            'phone_number',
            'profile_picture'
        ]
        labels = {
            'role': 'Rol/Cargo',
            'phone_number': 'Teléfono/Celular',
            'profile_picture': 'Foto de perfil'
        }
        widgets = {
            'role': forms.Select(attrs={'class': 'input'}),
        }
