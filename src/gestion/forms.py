from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'nombre_rep_legal',
            'last_name_1_rep_legal',
            'last_name_2_rep_legal',
            'razon_social',
            'nombre_fantasia',
            'run_rep_legal',
            'run_empresa',
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
            'tipo_empresa' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'reg_tributario': forms.Select(attrs={"class": "js-example-basic-single"}),
            'giro_rubro' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'codigo_sii': forms.Select(attrs={"class": "js-example-basic-single"}),
            'tipo_contabilidad' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'cuenta_corriente' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'region' : forms.Select(attrs={"class": "js-example-basic-single"}),
            'comuna' : forms.Select(attrs={"class": "js-example-basic-single"}),
        }