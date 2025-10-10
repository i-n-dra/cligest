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
            'run_empresa': forms.TextInput(attrs={"onchange": "run_validacion()"}),
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
            'a_pagar'
        ]