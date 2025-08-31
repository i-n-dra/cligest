from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Client(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
    )
    last_name_1 = models.CharField(
        max_length=50,
        verbose_name='Apellido Paterno',
    )
    last_name_2 = models.CharField(
        max_length=50,
        verbose_name='Apellido Materno',
    )
    run = models.CharField(
        max_length=12,
        verbose_name='RUN',
        help_text='Ejemplo: 12345678-9',
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}-[\dkK]$',
            )
        ]
    )
    email = models.EmailField(
        max_length=100,
        verbose_name='Correo electrónico',
        help_text=' Ejemplo: correo@ejemplo.com'
    )
    phone_number = models.CharField(
        max_length=11,
        verbose_name='Teléfono/Celular',
        help_text='Ejemplo: +56912345678',
        validators=[
            RegexValidator(
                regex=r'^\+1?\d{9,15}$',  # Example regex for international phone numbers
            )
        ]
    )
    address = models.CharField(
        max_length=200,
        verbose_name='Dirección',
        help_text='Ingrese una dirección, máximo de 200 caracteres'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    class Meta: # https://youtu.be/AR5hjQ8nla0?si=-o-ipQxpwiqOeJJK&t=909
        permissions = [
            ('export_client', 'Puede exportar clientes'),
        ]

    def __str__(self):
        return f'{self.name} - {self.email}'
    