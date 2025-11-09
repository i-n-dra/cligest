from django import forms
from .models import (
    Client,
    Claves,
    PagosCliente
)

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'run_rep_legal',
            'run_empresa',
            'nombre_rep_legal',
            'last_name_1_rep_legal',
            'last_name_2_rep_legal',
            'razon_social',
            'nombre_fantasia',
            'tipo_empresa',
            'reg_tributario',
            'giro_rubro',
            'codigo_sii',
            'n_trabajadores',

            'tipo_contabilidad',
            'cuenta_corriente',
            'n_cuenta_corriente',

            'email',
            'phone_number',
            'region',
            'comuna',
            'address',
        ]
        widgets = {
            'run_rep_legal': forms.TextInput(attrs={"onchange": "run_validacion()"}),
            'run_empresa': forms.TextInput(attrs={"onchange": "rut_validacion()"}),
            'tipo_empresa' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'reg_tributario': forms.SelectMultiple(attrs={"class": "my-select2-multiple"}),
            'giro_rubro' : forms.SelectMultiple(attrs={"class": "my-select2-multiple"}),
            'codigo_sii': forms.SelectMultiple(attrs={"class": "my-select2-multiple"}),
            'tipo_contabilidad' : forms.SelectMultiple(attrs={"class": "my-select2-multiple"}),
            'cuenta_corriente' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'region' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'comuna' : forms.Select(attrs={"class": "js-example-basic-single"}),
        }

class ClaveForm(forms.ModelForm):
    class Meta:
        model = Claves
        fields = [
            'client',
            'unica',
            'sii',
            'factura_electronica',
            'dir_trabajo'
        ]
        widgets = {
            'client' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'unica' : forms.PasswordInput(),
            'sii' : forms.PasswordInput(),
            'factura_electronica' : forms.PasswordInput(),
            'dir_trabajo' : forms.PasswordInput()
        }

class UpdateClaveForm(forms.ModelForm):
    class Meta:
        model = Claves
        fields = [
            'unica',
            'sii',
            'factura_electronica',
            'dir_trabajo'
        ]
        widgets = {
            'unica' : forms.PasswordInput(),
            'sii' : forms.PasswordInput(),
            'factura_electronica' : forms.PasswordInput(),
            'dir_trabajo' : forms.PasswordInput()
        }
        
class ExportClavesForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}),
        label="Contraseña"
    )

class PagosClienteForm(forms.ModelForm):
    class Meta:
        model = PagosCliente
        fields = [
            'client',
            'iva_a_pagar',
            'iva_anticipado',
            'ppm_vehiculo',
            'ppm_ventas',
            'honorarios',
            'f301',
            'imposiciones',
            'otros',
            'total',
            'a_pagar',
        ]
        widgets = {
            'client': forms.Select(attrs={"class": "js-example-basic-single"}),
            'iva_a_pagar': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'iva_anticipado': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'ppm_vehiculo': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'ppm_ventas': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'honorarios': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'f301': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'imposiciones': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'otros': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'total': forms.NumberInput(attrs={"onchange": "suma_pagos()", "readonly": "true", "class":"num-read-only"}),
            'a_pagar': forms.NumberInput(attrs={"onchange": "suma_pagos()", "readonly": "true", "class":"num-read-only"}),
        }

class PagosClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = PagosCliente
        fields = [
            'iva_a_pagar',
            'iva_anticipado',
            'ppm_vehiculo',
            'ppm_ventas',
            'honorarios',
            'f301',
            'imposiciones',
            'otros',
            'total',
            'a_pagar'
        ]
        widgets = {
            'iva_a_pagar': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'iva_anticipado': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'ppm_vehiculo': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'ppm_ventas': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'honorarios': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'f301': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'imposiciones': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'otros': forms.NumberInput(attrs={"onchange": "suma_pagos()"}),
            'total': forms.NumberInput(attrs={"onchange": "suma_pagos()", "readonly": "true", "class":"num-read-only"}),
            'a_pagar': forms.NumberInput(attrs={"onchange": "suma_pagos()", "readonly": "true", "class":"num-read-only"}),
        }

class PagosExportSelectForm(forms.Form):
    choices = [
        ('mes', 'Deudas del mes'),
        ('historica', 'Deudas históricas')
    ]
    mes = forms.ChoiceField(
        choices=choices,
        widget=forms.RadioSelect,
        label='Seleccione el tipo de exportación:'
    )