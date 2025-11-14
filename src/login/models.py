from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.validators import RegexValidator
from django.utils.timezone import now

# Create your models here.
class Role(models.Model):
    name = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        max_length=40,
        verbose_name='Rol',
        default='Sin rol'
    )
    permissions = models.ManyToManyField(Permission, verbose_name='Permisos')

    def __str__(self):
        return f'{self.name}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    role = models.ForeignKey(Group, on_delete=models.RESTRICT, null=True, blank=True)
    run = models.CharField(
        max_length=12,
        verbose_name='RUN',
        help_text='Ejemplo: 12345678-9',
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}-[\dkK]$',
            )
        ],
        error_messages={
            'invalid': 'El formato de RUN es incorrecto'
        },
        blank=True
    )
    date_of_birth = models.DateField(
        verbose_name='Fecha de nacimiento',
        help_text='Ejemplo: 01/01/1990',
        blank=True,
        default=now
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name='Teléfono/Celular',
        help_text='Ejemplo: +56912345678',
        validators=[
            RegexValidator(
                regex=r'^\+569\d{8}$',  # Example regex for international phone numbers
            )
        ],
        blank=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        verbose_name='Foto de perfil',
        help_text='Opcional',
        default='profile_pictures/default_pfp.jpg'
    )

    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'
