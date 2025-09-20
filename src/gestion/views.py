from django.shortcuts import render
import time
from django.contrib.auth.models import User
from login.models import Profile
from .models import (
    Client,
    Claves
)
from .forms import (
    ClientForm,
    ClaveForm
)
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
# Importación de encriptación AES 
from .static.py.aes import AES
import os

# Create your views here.
def home(request):
    return render(request, 'index.html')

### Mensaje dia/tarde ###
def horario_am():
    hora = time.localtime().index(3) # index 3 -> tm_hour
    if hora > 12: 
        return False
    elif hora < 12:
        return True

def request_user_role(username):
    profile = Profile.objects.filter(user__username=username).first()
    if profile and profile.role:
        role = profile.role.name
    else:
        role = 'Sin cargo'
    return role

### Clientes Views ###

class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    ordering = ['last_name_1_rep_legal']

class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/detail.html'
    context_object_name = 'c'

class ClientCreateView(CreateView):
    model = Client
    template_name = 'clients/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('create_claves')

    def form_valid(self, form):
        form.save()
        global client_id
        client_id = form.instance.id
        return super().form_valid(form)

### Claves Views ###

class ClavesCreateView(CreateView):
    model = Claves
    template_name = 'claves/create.html'
    form_class = ClaveForm
    success_url = reverse_lazy('list_clients')

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        try:
            form.fields['client'].initial = client_id
        except NameError:
            form.fields['client'].initial = None # podría cambiarse a raise error (cligest/templates/errors/)
        return form
    
    def form_valid(self, form):
        # revisar static/py/ para ver ejemplos y source code
        global key
        global iv
        # cambiar a: contraseña de request.user | secret_key de settings | variable de entorno
        # actualmente solo funciona con el ultimo obj de claves creado
        key = os.urandom(16)
        iv = os.urandom(16)

        clave1 = str(form.instance.unica)
        clave1 = clave1.encode('utf-8')
        clave2 = str(form.instance.sii)
        clave2 = clave2.encode('utf-8')
        clave3 = str(form.instance.factura_electronica)
        clave3 = clave3.encode('utf-8')
        clave4 = str(form.instance.dir_trabajo)
        clave4 = clave4.encode('utf-8')

        clave1_encrypted = AES(key).encrypt_cbc(clave1, iv)
        clave2_encrypted = AES(key).encrypt_cbc(clave2, iv)
        clave3_encrypted = AES(key).encrypt_cbc(clave3, iv)
        clave4_encrypted = AES(key).encrypt_cbc(clave4, iv)

        form.instance.unica = str(clave1_encrypted)
        form.instance.sii = str(clave2_encrypted)
        form.instance.factura_electronica = str(clave3_encrypted)
        form.instance.dir_trabajo = str(clave4_encrypted)

        print(f'unica: {form.instance.unica}, sii: {form.instance.sii}, factura: {form.instance.factura_electronica}')

        form.save()
        return super().form_valid(form)

class TestView(ListView): # no funciona aún :[
    model = Claves
    template_name = 'claves/test.html'
    context_object_name = 'claves'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the first Claves object (or adjust as needed)
        clave_obj = Claves.objects.all()
        if clave_obj:
            clave_obj = clave_obj.last()
            try:
                decrypted = AES(key).decrypt_cbc(clave_obj.unica.encode('utf-8'), iv).decode('utf-8')
            except Exception:
                decrypted = None
        else:
            decrypted = None
        context['decrypted_unica'] = decrypted
        context['clave_obj'] = clave_obj
        return context

def ClavesExportar():
    claves = Claves.objects.all()

    for c in claves:
        c.unica = c.unica.encode('utf-8')

        print(f'decrypted: {AES(key).decrypt_cbc(c.unica, iv).decode('utf-8')}')
        clave1_decrypted = AES(key).decrypt_cbc(c.unica, iv).decode('utf-8')

    if clave1_decrypted:
        return clave1_decrypted
    else:
        return "Error"