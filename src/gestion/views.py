from django.shortcuts import render
import time, os, ast
from django.contrib.auth.models import User
from django.contrib.auth.hashers import PBKDF2PasswordHasher
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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Importación de encriptación AES 
from .static.py.aes import AES

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

# class para pedir la pass e igualarla con la hash de la key

### Clientes Views ###

class ClientExport(ListView):
    model = Client
    def get_queryset(self):
        return super().get_queryset()


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

class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'clients/update.html'
    form_class = ClientForm
    success_url = reverse_lazy('list_clients')

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

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/delete.html'
    success_url = reverse_lazy('list_clients')

### Claves Views ### wip nada funciona

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
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        #unica = request.POST.get('unica')
        #unica = unica.encode('utf-8')
#
        #sii = request.POST.get('sii')
        #sii = sii.encode('utf-8')
#
        #factura_electronica = request.POST.get('factura_electronica')
        #factura_electronica = factura_electronica.encode('utf-8')
#
        #dir_trabajo = request.POST.get('dir_trabajo')
        #dir_trabajo = dir_trabajo.encode('utf-8')

        form = self.get_form()
        if form.is_valid():
            # revisar static/py/ para ver ejemplos y source code
            # cambiar a contraseña de request.user
            key = b'passw0rdpassw0rd'
            # key = 'passw0rd'
            # key_bytes = key.encode('utf-8')
            # key = key_bytes.ljust(16, b'\0')[:16]
            iv = os.urandom(16)

            clave1 = str(form.instance.unica)
            clave1 = clave1.encode('utf-8')
            clave2 = str(form.instance.sii)
            clave2 = clave2.encode('utf-8')
            clave3 = str(form.instance.factura_electronica)
            clave3 = clave3.encode('utf-8')
            clave4 = str(form.instance.dir_trabajo)
            clave4 = clave4.encode('utf-8')
            clave1_encrypted = AES(key).encrypt_cfb(clave1, iv)
            clave2_encrypted = AES(key).encrypt_cfb(clave2, iv)
            clave3_encrypted = AES(key).encrypt_cfb(clave3, iv)
            clave4_encrypted = AES(key).encrypt_cfb(clave4, iv)

            # clave1_encrypted = AES(key).encrypt_cbc(unica, iv)
            # clave2_encrypted = AES(key).encrypt_cbc(sii, iv)
            # clave3_encrypted = AES(key).encrypt_cbc(factura_electronica, iv)
            # clave4_encrypted = AES(key).encrypt_cbc(dir_trabajo, iv)

            form.instance.unica = clave1_encrypted
            form.instance.sii = clave2_encrypted
            form.instance.factura_electronica = clave3_encrypted
            form.instance.dir_trabajo = clave4_encrypted
            form.instance.iv = iv

            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TestView(DetailView): 
    model = Claves
    template_name = 'claves/test.html'
    context_object_name = 'claves'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clave = self.get_object()
        decrypted_u = None
        decrypted_s = None
        decrypted_fe = None
        decrypted_dt = None

        # key = auth.user.request password, theres going to be a request for input,
        # then the hashed result compared to the password in the database
        key = b'passw0rdpassw0rd'

        if clave and bytes(key):
            iv = clave.iv
            print('clave.unica:', clave.unica, type(clave.unica))
            try:
                encrypted_u = ast.literal_eval(clave.unica)
                print('encrypted_u:', encrypted_u, type(encrypted_u),'\niv:',clave.iv, type(clave.iv))
                decrypted_u = AES(key).decrypt_cfb(encrypted_u, iv).decode('utf-8', 'replace')
                print('decrypted_u:', decrypted_u)
                
                encrypted_s = ast.literal_eval(clave.sii) if isinstance(clave.sii, str) else clave.sii
                decrypted_s = AES(key).decrypt_cfb(encrypted_s, iv).decode('utf-8')

                encrypted_fe = ast.literal_eval(clave.factura_electronica) if isinstance(clave.factura_electronica, str) else clave.factura_electronica
                decrypted_fe = AES(key).decrypt_cfb(encrypted_fe, iv).decode('utf-8')

                encrypted_dt = ast.literal_eval(clave.dir_trabajo) if isinstance(clave.dir_trabajo, str) else clave.dir_trabajo
                decrypted_dt = AES(key).decrypt_cfb(encrypted_dt, iv).decode('utf-8')
            except Exception:
                raise
                None

        else:
            print('no clave_obj')
            decrypted_u = None

        context['decrypted_unica'] = decrypted_u
        context['decrypted_sii'] = decrypted_s
        context['decrypted_factura_electronica'] = decrypted_fe
        context['decrypted_dir_trabajo'] = decrypted_dt
        context['clave'] = clave
        return context

def ClavesExportar():
    claves = Claves.objects.all()
    key = None
    iv = None

    for c in claves:
        c.unica = c.unica.encode('utf-8')

        print(f'decrypted: {AES(key).decrypt_cfb(c.unica, iv).decode('utf-8')}')
        clave1_decrypted = AES(key).decrypt_cfb(c.unica, iv).decode('utf-8')

    if clave1_decrypted:
        return clave1_decrypted
    else:
        return "Error"