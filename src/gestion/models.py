from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User

def cuenta_corriente_validator(value):
    if not re.match(r'^(\d{9,15}|\d{1,4}(?:-\d{1,4})+|\d{1,4}(?: \d{1,4})+)$', value):
        raise ValidationError('Solo se permiten dígitos y espacios o guiones (-)')
    digits = re.sub(r'\D', '', value)
    if len(digits) < 9:
        raise ValidationError('Debe contener al menos 9 dígitos.')
def validate_max_trabajadores(value):
        if value > 200000:
            raise ValidationError('Este número no puede exceder 200.000')

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
        return f'{str(self.code)} - {self.activity}'

class GiroRubro(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Giro / Rubro'
    )

    def __str__(self):
        return self.name

class RegTributario(models.Model):
    name = models.CharField(
        max_length=70,
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
    active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    nombre_rep_legal = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
                message='Solo se aceptan caracteres, y un mínimo de 2',
                code='invalid'
            )
        ]
    )
    last_name_1_rep_legal = models.CharField(
        max_length=50,
        verbose_name='Apellido Paterno',
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
                message='Solo se aceptan caracteres, y un mínimo de 2',
                code='invalid'
            )
        ]
    )
    last_name_2_rep_legal = models.CharField(
        max_length=50,
        verbose_name='Apellido Materno',
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
                message='Solo se aceptan caracteres, y un mínimo de 2',
                code='invalid'
            )
        ]
    )
    razon_social = models.CharField(
        max_length=150,
        verbose_name='Razón Social',
        blank=True,
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
                message='Solo se aceptan caracteres, y un mínimo de 2',
                code='invalid'
            )
        ]
    )
    nombre_fantasia = models.CharField(
        max_length=150,
        verbose_name='Nombre de Fantasía',
        blank=True,
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
                message='Solo se aceptan caracteres, y un mínimo de 2',
                code='invalid'
            )
        ]
    )
    run_rep_legal = models.CharField(
        max_length=12,
        verbose_name='RUN (Representante legal)',
        help_text='Ejemplo: 12345678-9',
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}-[\dkK]$',
                message='Solo se aceptan dígitos y K, siga el formato 12345678-9',
                code='invalid'
            )
        ],
        unique=True
    )
    run_empresa = models.CharField(
        max_length=12,
        verbose_name='RUT/RUN (Empresa)',
        help_text='Ejemplo: 12345678-9',
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}-[\dkK]$',
                message='Solo se aceptan dígitos y K, siga el formato 12345678-9',
                code='invalid'
            )
        ],
        unique=True
    )
    tipo_empresa = models.CharField(
        max_length=20,
        verbose_name='Tipo de empresa',
        choices=[
            ('Persona Natural', 'Persona Natural'),
            ('Persona Jurídica', 'Persona Jurídica')
        ]
    )
    giro_rubro = models.ManyToManyField(
        GiroRubro,
        verbose_name='Giro / Rubro',  
    )
    codigo_sii = models.ManyToManyField(
        CodigoSII,
        verbose_name='Código Actividad S.I.I.'
    )
    email = models.EmailField(
        max_length=100,
        verbose_name='Correo electrónico',
        help_text=' Ejemplo: correo@ejemplo.com'
    )
    phone_number = models.CharField(
        max_length=18,
        verbose_name='Teléfono/Celular',
        help_text='Ejemplo: +56912345678',
        validators=[
            RegexValidator(
                regex=r'^\+1?\d{9,15}$',  # Example regex for international phone numbers
                message='Solo se aceptan dígitos y signo "+", siga el formato +56912345678',
                code='invalid'
            )
        ]
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.RESTRICT,
        verbose_name='Región'
    )
    comuna = models.ForeignKey(
        Comuna,
        on_delete=models.RESTRICT,
        verbose_name='Comuna'
    )
    address = models.CharField(
        max_length=200,
        verbose_name='Dirección',
        help_text='Ingrese una dirección, máximo de 200 caracteres',
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
                message='Solo se aceptan caracteres, y un mínimo de 2',
                code='invalid'
            )
        ]
    )
    tipo_contabilidad = models.ManyToManyField(
        TipoContabilidad,
        verbose_name='Tipo de Contabilidad',
    )
    reg_tributario = models.ManyToManyField(
        RegTributario,
        verbose_name='Régimen Tributario',
    )
    cuenta_corriente = models.CharField(
        max_length=30,
        verbose_name='Cuenta Corriente',
        choices=[
            ('Banco Bice', 'Banco Bice'),
            ('Banco Consorcio', 'Banco Consorcio'),
            ('Banco De Chile', 'Banco De Chile'),
            ('Banco Del Estado De Chile', 'Banco Del Estado De Chile'),
            ('Banco Falabella', 'Banco Falabella'),
            ('Banco Internacional', 'Banco Internacional'),
            ('Banco Itaú Chile', 'Banco Itaú Chile'),
            ('Banco Ripley', 'Banco Ripley'),
            ('Banco Santander Chile', 'Banco Santander Chile'),
            ('Banco Security', 'Banco Security'),
            ('Banco Bci', 'Banco Bci'),
            ('Scotiabank Chile', 'Scotiabank Chile'),
            ('Btg Pactual Chile', 'Btg Pactual Chile')
        ]
    )
    n_cuenta_corriente = models.CharField(
        max_length=20,
        verbose_name='N° Cuenta Corriente',
        validators=[cuenta_corriente_validator]
    )
    n_trabajadores = models.IntegerField(
        verbose_name='Trabajadores',
        validators=[validate_max_trabajadores]
    )
        
    class Meta: # https://youtu.be/AR5hjQ8nla0?si=-o-ipQxpwiqOeJJK&t=909
        permissions = [
            ('export_client', 'Puede exportar clientes'),
        ]

    def __str__(self):
        return f'{self.nombre_rep_legal} {self.last_name_1_rep_legal} {self.last_name_2_rep_legal} - {self.run_rep_legal}'

class Claves(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Cliente',
        help_text='Asegúrese de que el cliente seleccionado sea correcto'
    )

    sii = models.TextField(
        verbose_name='S.I.I.',
        blank=True
    )
    factura_electronica = models.TextField(
        verbose_name='Factura Electrónica',
        blank=True
    )
    dir_trabajo = models.TextField(
        verbose_name='Dirección de Trabajo',
        blank=True
    )
    unica = models.TextField(
        verbose_name='Clave Única',
        blank=True
    )

    iv = models.BinaryField(
        auto_created=False,
    )

    class Meta:
        permissions = [
            ('export_claves', 'Puede exportar claves'),
        ]

    def __str__(self):
        return f'Claves de {self.client.nombre_rep_legal} {self.client.last_name_1_rep_legal} {self.client.last_name_2_rep_legal} - RUN: {self.client.run_rep_legal}'

class PagosCliente(models.Model):
    client = models.ForeignKey(
        Client,
        verbose_name='Cliente',
        on_delete=models.CASCADE
    )
    iva_a_pagar = models.IntegerField(
        verbose_name="IVA a Pagar"
    )
    iva_anticipado = models.IntegerField(
        verbose_name="IVA Anticipado"
    )
    ppm_vehiculo = models.IntegerField(
        verbose_name="PPM Sobre Vehículo"
    )
    ppm_ventas = models.IntegerField(
        verbose_name="PPM Sobre las Ventas"
    )
    honorarios = models.IntegerField(
        verbose_name="Honorarios"
    )
    f301 = models.IntegerField(
        verbose_name="Certificado F30-1"
    )
    imposiciones = models.IntegerField(
        verbose_name="Imposiciones"
    )
    otros = models.IntegerField(
        verbose_name="Otros"
    )
    total = models.IntegerField(
        verbose_name="Total"
    )
    a_pagar = models.IntegerField(
        verbose_name="A Pagar"
    )

    created_at = models.DateTimeField(
        verbose_name="Fecha Creación/Actualización",
        auto_now=True,
    )

    class Meta:
        permissions = [
            ('export_pagos', 'Puede exportar pagos'),
        ]

    def __str__(self):
        return f'${self.a_pagar} - {self.created_at.month}/{self.created_at.year}'