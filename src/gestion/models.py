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
        return str(self.code)

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
            ('p_natural', 'Persona Natural'),
            ('p_juridica', 'Persona Jurídica')
        ]
    )
    giro_rubro = models.CharField(
        max_length=100,
        verbose_name='Giro / Rubro',
        choices=[
            ('agricultura', 'Agricultura, Ganadería, Silvicultura Y Pesca'),
            ('explotacion_minas', 'Explotación De Minas Y Canteras'),
            ('i_manufacturera', 'Industria Manufacturera'),
            ('sum_electricidad', 'Suministro De Electricidad, Gas, Vapor Y Aire Acondicionado'),
            ('sum_agua', 'Suministro De Agua; Evacuación De Aguas Residuales, Gestión De Desechos Y Descontaminación'),
            ('construccion', 'Construcción'),
            ('comercio_reparacion', 'Comercio Al Por Mayor Y Al Por Menor; Reparación De Vehiculos Automotores Y Motocicletas'),
            ('transporte_almacenamiento', 'Transporte Y Almacenamiento'),
            ('act_alojamiento', 'Actividades De Alojamiento Y De Servicio De Comidas'),
            ('info_com', 'Información Y Comunicaciones'),
            ('act_financieras', 'Actividades Financieras Y De Seguros'),
            ('act_inmobiliarias', 'Actividades Inmobiliarias'),
            ('act_profesionales', 'Actividades Profesionales, Cientificas Y Técnicas'),
            ('act_administrativos', 'Actividades De Servicios Administrativos Y De Apoyo'),
            ('admin_publica', 'Administración Pública Y Defensa; Planes De Seguridad Social De Afiliación Obligatoria'),
            ('ensenianza', 'Enseñanza'),
            ('act_atención_salud', 'Actividades De Atención De La Salud Humana Y De Asistencia Social'),
            ('act_artisticas', 'Actividades Artísticas, De Entretenimiento Y Recreativas'),
            ('otras_act_servicios', 'Otras Actividades De Servicios'),
            ('act_hogares', 'Actividades De Los Hogares Como Empleadores; Actividades No Diferenciadas De Los Hogares'),
            ('act_organizaciones', 'Actividades De Organizaciones Y Órganos Extraterritoriales'),
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
        max_length=11,
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
    cuenta_corriente = models.CharField(
        max_length=30,
        verbose_name='Cuenta Corriente',
        choices=[
            ('bice', 'Banco Bice'),
            ('consorcio', 'Banco Consorcio'),
            ('chile', 'Banco De Chile'),
            ('estado', 'Banco Del Estado De Chile'),
            ('falabella', 'Banco Falabella'),
            ('internacional', 'Banco Internacional'),
            ('itau', 'Banco Itaú Chile'),
            ('ripley', 'Banco Ripley'),
            ('santander Chile', 'Banco Santander Chile'),
            ('security', 'Banco Security'),
            ('bci', 'Banco Bci'),
            ('scotiabank', 'Scotiabank Chile'),
            ('btg_pactual', 'Btg Pactual Chile')
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

