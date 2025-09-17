from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Region(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Región'
    )

    def __str__(self):
        return self.name

class Comuna(models.Model):
    name = models.CharField(
        max_length=70,
        verbose_name='Comuna'
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.RESTRICT,
        verbose_name='Región'
    )

    def __str__(self):
        return self.name
    
class CodigoSII(models.Model):
    code = models.IntegerField(
        verbose_name='Código Actividad S.I.I.',
    )
    activity = models.CharField(
        max_length=100,
        verbose_name='Actividad Económica'
    )

    def __str__(self):
        return str(self.code)

class RegTributario(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Régimen Tributario'
    )

    def __str__(self):
        return self.name

class TipoContabilidad(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Tipo de Contabilidad'
    )

    def __str__(self):
        return self.name
    
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

class Claves(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Cliente'
    )

    sii = models.CharField(
        max_length=70,
        verbose_name='Clave S.I.I.'
    )
    factura_electronica = models.CharField(
        max_length=70,
        verbose_name='Clave Factura Electrónica'
    )
    dir_trabajo = models.CharField(
        max_length=70,
        verbose_name='Clave Dirección de Trabajo'
    )
    unica = models.CharField(
        max_length=70,
        verbose_name='Clave Única'
    )

    def __str__(self):
        return f'Claves de {self.client.name} {self.client.last_name_1} {self.client.last_name_2} - RUN: {self.client.run}'

