from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

def cuenta_corriente_validator(value):
    if not re.match(r'^(\d{9,15}|\d{1,4}(?:-\d{1,4})+|\d{1,4}(?: \d{1,4})+)$', value):
        raise ValidationError('Formato inválido.')
    digits = re.sub(r'\D', '', value)
    if len(digits) < 9:
        raise ValidationError('Debe contener al menos 9 dígitos.')

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
    nombre_rep_legal = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
            )
        ]
    )
    last_name_1_rep_legal = models.CharField(
        max_length=50,
        verbose_name='Apellido Paterno',
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
            )
        ]
    )
    last_name_2_rep_legal = models.CharField(
        max_length=50,
        verbose_name='Apellido Materno',
        validators=[
            RegexValidator(
                regex=r'\D[a-zA-Z]{2,}+',
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
            )
        ]
    )
    run_empresa = models.CharField(
        max_length=12,
        verbose_name='RUN (Empresa)',
        help_text='Ejemplo: 12345678-9',
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}-[\dkK]$',
            )
        ]
    )
    tipo_empresa = models.CharField(
        max_length=20,
        verbose_name='Tipo de empresa',
        choices=[
            ('Persona Natural', 'Persona Natural'),
            ('Persona Jurídica', 'Persona Jurídica')
        ]
    )
    giro_rubro = models.CharField(
        max_length=100,
        verbose_name='Giro / Rubro',
        choices=[
            (
                'Agricultura, Ganadería, Silvicultura Y Pesca',
                'Agricultura, Ganadería, Silvicultura Y Pesca'
            ),
            (
                'Explotación De Minas Y Canteras',
                'Explotación De Minas Y Canteras'
            ),
            (
                'Industria Manufacturera',
                'Industria Manufacturera'
            ),
            (
                'Suministro De Electricidad, Gas, Vapor Y Aire Acondicionado',
                'Suministro De Electricidad, Gas, Vapor Y Aire Acondicionado'
            ),
            (
                'Suministro De Agua; Evacuación De Aguas Residuales, Gestión De Desechos Y Descontaminación',
                'Suministro De Agua; Evacuación De Aguas Residuales, Gestión De Desechos Y Descontaminación'
            ),
            (   'Construcción',
                'Construcción'
            ),
            (   'Comercio Al Por Mayor Y Al Por Menor; Reparación De Vehiculos Automotores Y Motocicletas',
                'Comercio Al Por Mayor Y Al Por Menor; Reparación De Vehiculos Automotores Y Motocicletas'
            ),
            (   'Transporte Y Almacenamiento',
                'Transporte Y Almacenamiento'
            ),
            (   'Actividades De Alojamiento Y De Servicio De Comidas',
                'Actividades De Alojamiento Y De Servicio De Comidas'
            ),
            (   'Información Y Comunicaciones',
                'Información Y Comunicaciones'
            ),
            (   'Actividades Financieras Y De Seguros',
                'Actividades Financieras Y De Seguros'
            ),
            (   'Actividades Inmobiliarias',
                'Actividades Inmobiliarias'
            ),
            (   'Actividades Profesionales, Cientificas Y Técnicas',
                'Actividades Profesionales, Cientificas Y Técnicas'
            ),
            (   'Actividades De Servicios Administrativos Y De Apoyo',
                'Actividades De Servicios Administrativos Y De Apoyo'
            ),
            (   'Administración Pública Y Defensa; Planes De Seguridad Social De Afiliación Obligatoria',
                'Administración Pública Y Defensa; Planes De Seguridad Social De Afiliación Obligatoria'
            ),
            (   'Enseñanza',
                'Enseñanza'
            ),
            (   'Actividades De Atención De La Salud Humana Y De Asistencia Social',
                'Actividades De Atención De La Salud Humana Y De Asistencia Social'
            ),
            (   'Actividades Artísticas, De Entretenimiento Y Recreativas',
                'Actividades Artísticas, De Entretenimiento Y Recreativas'
            ),
            (   'Otras Actividades De Servicios',
                'Otras Actividades De Servicios'
            ),
            (   'Actividades De Los Hogares Como Empleadores; Actividades No Diferenciadas De Los Hogares',
                'Actividades De Los Hogares Como Empleadores; Actividades No Diferenciadas De Los Hogares'
            ),
            (   'Actividades De Organizaciones Y Órganos Extraterritoriales',
                'Actividades De Organizaciones Y Órganos Extraterritoriales'
            ),
        ]
    )
    codigo_sii = models.ForeignKey(
        CodigoSII,
        on_delete=models.RESTRICT,
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
            )
        ]
    )
    tipo_contabilidad = models.ForeignKey(
        TipoContabilidad,
        verbose_name='Tipo de Contabilidad',
        on_delete=models.RESTRICT
    )
    reg_tributario = models.ForeignKey(
        RegTributario,
        verbose_name='Régimen Tributario',
        on_delete=models.RESTRICT
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
        validators=[cuenta_corriente_validator],
        error_messages={
            'invalid': 'Solo se permiten dígitos y espacios o guiones (-)'
        }
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
        return f'{self.nombre_rep_legal} {self.last_name_1_rep_legal} {self.last_name_2_rep_legal} - {self.run_rep_legal}'

class Claves(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Cliente'
    )

    sii = models.CharField(
        max_length=130,
        verbose_name='Clave S.I.I.'
    )
    factura_electronica = models.CharField(
        max_length=130,
        verbose_name='Clave Factura Electrónica'
    )
    dir_trabajo = models.CharField(
        max_length=130,
        verbose_name='Clave Dirección de Trabajo'
    )
    unica = models.CharField(
        max_length=130,
        verbose_name='Clave Única'
    )

    def __str__(self):
        return f'Claves de {self.client.nombre_rep_legal} {self.client.last_name_1_rep_legal} {self.client.last_name_2_rep_legal} - RUN: {self.client.run_rep_legal}'

