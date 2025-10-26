from django.shortcuts import render
import time, os, ast, base64
from django.contrib.auth.models import User
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from login.models import Profile
from .models import (
    Client,
    Claves,
    PagosCliente
)
from .forms import (
    ClientForm,
    ClaveForm,
    PagosClienteForm,
    PagosClienteUpdateForm,
    ExportClavesForm
)
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .static.py.aes import AES
from .static.py.exportar_clientes import exportar_clientes_main
from .static.py.exportar_pagos import exportar_pagos_main
from .static.py.exportar_claves import exportar_claves_all, exportar_clave
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate
from django.db.models.base import Model

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

### Clientes Views ###

@permission_required('gestion.export_client', raise_exception=True, login_url="/")
def ClientExport(request):
    clientes = Client.objects.all()
    pagos = PagosCliente.objects.all()
    msg = exportar_clientes_main(clientes, pagos)
    return render(request, 'clients/msg_exportacion.html', { 'msg': msg })

class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clientes'
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
    success_url = reverse_lazy('create_clave')

    def form_valid(self, form):
        form.save()
        global client_id
        client_id = form.instance.id
        return super().form_valid(form)

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/delete.html'
    success_url = reverse_lazy('list_clients')

def check_run(request):
    run = request.GET.get("run")
    exists = Client.objects.filter(run_rep_legal=run).exists()
    return JsonResponse({"exists": exists})

def check_rut(request):
    run = request.GET.get("rut")
    exists = Client.objects.filter(run_empresa=run).exists()
    return JsonResponse({"exists": exists})

### PagosCliente Views ###

class PagosCreateView(CreateView):
    model = PagosCliente
    template_name = 'pagos/create.html'
    form_class = PagosClienteForm
    success_url = reverse_lazy('list_pagos')

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        return form
    def form_valid(self, form):
        calc_total = 0
        form_cliente = form.instance.client

        now = timezone.now()
        validation = PagosCliente.objects.filter(
            client=form_cliente,
            created_at__year = now.year,
            created_at__month = now.month
        ).exists()

        if validation:
            form.add_error('client', "El cliente seleccionado ya tiene una declaración este mes.")
            return self.form_invalid(form)
        
        iva_a_pagar = form.instance.iva_a_pagar
        iva_anticipado = form.instance.iva_anticipado
        ppm_vehiculo = form.instance.ppm_vehiculo
        ppm_ventas = form.instance.ppm_ventas
        honorarios = form.instance.honorarios
        f301 = form.instance.f301
        imposiciones = form.instance.imposiciones
        otros = form.instance.otros

        calc_total = (
            iva_a_pagar +
            iva_anticipado +
            ppm_vehiculo +
            ppm_ventas +
            honorarios +
            f301 +
            imposiciones +
            otros
        ) - iva_anticipado
        
        if calc_total == form.instance.a_pagar:
            return super().form_valid(form)
        else:
            form.add_error("a_pagar", "Ocurrió un error validando los montos, por favor intente de nuevo.")
            return self.form_invalid(form)
        
class PagosListView(ListView):
    model = PagosCliente
    template_name = "pagos/list.html"
    context_object_name = 'pagos'
    ordering = ['created_at']

class PagosDetailView(DetailView):
    model = PagosCliente
    template_name = 'pagos/detail.html'
    context_object_name = 'p'

class PagosDeleteView(DeleteView):
    model = PagosCliente
    template_name = 'pagos/delete.html'
    success_url = reverse_lazy('list_pagos')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        now = timezone.now()
        created = self.object.created_at

        if created.year != now.year or created.month != now.month:
            raise PermissionDenied("Las declaraciones históricas no se pueden eliminar.")

        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

class PagosUpdateView(UpdateView):
    model = PagosCliente
    template_name = "pagos/update.html"
    form_class = PagosClienteUpdateForm
    success_url = reverse_lazy('list_pagos')

    def get_form(self, form_class=None): # needs testing
        form = super().get_form(form_class)
        
        obj = PagosCliente.objects.filter(id=form.instance.id).order_by('-created_at').get().created_at
        now = timezone.now()

        if obj.year != now.year or obj.month != now.month:
            raise PermissionDenied("Las declaraciones históricas no se pueden eliminar.")
        return form
    
    def form_valid(self, form):
        calc_total = 0
        
        iva_a_pagar = form.instance.iva_a_pagar
        iva_anticipado = form.instance.iva_anticipado
        ppm_vehiculo = form.instance.ppm_vehiculo
        ppm_ventas = form.instance.ppm_ventas
        honorarios = form.instance.honorarios
        f301 = form.instance.f301
        imposiciones = form.instance.imposiciones
        otros = form.instance.otros

        calc_total = (
            iva_a_pagar +
            iva_anticipado +
            ppm_vehiculo +
            ppm_ventas +
            honorarios +
            f301 +
            imposiciones +
            otros
        ) - iva_anticipado
        
        if calc_total == form.instance.a_pagar:
            return super().form_valid(form)
        else:
            form.add_error("a_pagar", "Ocurrió un error validando los montos, por favor intente de nuevo.")
            return self.form_invalid(form)
    
### Claves Views ### en progreso

class ClavesExportarCliente(DetailView): # exportar un conjunto de claves
    model = Claves
    template_name = ""

    def export_clave(self, request, clave_id):
        clave = Claves.objects.get(id=clave_id)
        key = b'passw0rdpassw0rd'
        msg = exportar_clave(clave, key, clave.iv)

        print(f'decrypted: {AES(key).decrypt_cfb(clave.unica, clave.iv).decode('utf-8')}')
        unica_decrypted = AES(key).decrypt_cfb(clave.unica, clave.iv).decode('utf-8')

        if unica_decrypted:
            print("unica_decrypted: ",unica_decrypted)
            return render(request, 'clients/msg_exportacion.html', { 'msg': msg })
        else:
            return "Error"

#@permission_required('gestion.export_claves', raise_exception=True, login_url="/")
class ClavesExportar(FormView): 
    claves = Claves.objects.all()
    users = User.objects.all()
    template_name = 'claves/export.html'
    form_class = ExportClavesForm
    success_url = reverse_lazy('list_claves')

    def export(self, request, req_pass):
        user = request.user

        authenticated_user = authenticate(request, username=user.username, password=req_pass)
        if authenticated_user is None:
            print("Authentication failed")
            return render(request, 'claves/msg_exportacion.html', {'msg': "Contraseña incorrecta."})
        
        db_user = self.users.get(username=user)
        user_password = db_user.password
        key = bytes(user_password.encode())
        key = key.ljust(16, b'\0')[:16]
        # key = key.rjust(16, b'\0')[:16]
        aes = AES(key)
        msg = exportar_claves_all(self.claves, user_password, aes)

        if msg:
            return render(request, 'claves/msg_exportacion.html', {'msg': msg})
        else:
            return render(request, 'claves/msg_exportacion.html', {'msg': ["Ocurrió un error al exportar"]})    

    def form_valid(self, form):
        password = form.cleaned_data.get("password")
        return self.export(self.request, password)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

@login_required
def get_aes_key(request): # para CreateView y UpdateView
    users = User.objects.all()
    if request.user.is_authenticated:
        current_user = request.user
        db_user = users.get(username=current_user)
        user_password = db_user.password
        key = bytes(user_password.encode())
        return key

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
            form.fields['client'].initial = None
        return form
        
    def post(self, request):
        form = self.get_form()
        self.object = None
        
        # revisar static/py/aes para ver ejemplos y source code
        if form.is_valid():
            key = get_aes_key(request).ljust(16, b'\0')[:16]
            iv = os.urandom(16)
            aes = AES(key)

            def encrypt_field(value):
                data = value.encode('utf-8')
                encrypted = aes.encrypt_cfb(data, iv)
                print("b64 encrypted: ", base64.b64encode(encrypted).decode('utf-8'))
                return base64.b64encode(encrypted).decode('utf-8')

            form.instance.unica = encrypt_field(form.cleaned_data['unica'])
            form.instance.sii = encrypt_field(form.cleaned_data['sii'])
            form.instance.factura_electronica = encrypt_field(form.cleaned_data['factura_electronica'])
            form.instance.dir_trabajo = encrypt_field(form.cleaned_data['dir_trabajo'])
            form.instance.iv = iv

            # decryption test
            encrypted = base64.b64decode(form.instance.unica)
            decrypted = aes.decrypt_cfb(encrypted, form.instance.iv)
            print("decryption test: ", decrypted, type(decrypted))

            form.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
        
class ClaveListView(ListView):
    model = Claves
    template_name = 'claves/list.html'
    context_object_name = 'claves'

class ClaveDetailView(DetailView):
    model = Claves
    template_name = 'claves/detail.html'
    context_object_name = 'c'

class ClaveUpdateView(UpdateView):
    model = Claves
    template_name = 'claves/update.html'
    form_class = ClaveForm
    success_url = reverse_lazy('list_claves')

class ClaveDeleteView(DeleteView):
    model = Claves
    template_name = 'claves/delete.html'
    success_url = reverse_lazy('list_claves')