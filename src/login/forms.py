from django import forms
from .models import Profile, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            if self.instance and not self.instance.has_usable_password():
                password.help_text = '''Enable password-based authentication for this user by setting a "
                    "password.'''

class UserGroupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['groups']
        widgets = {
            'groups' : forms.SelectMultiple(attrs={'class': 'my-select2-multiple'})
        }

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
