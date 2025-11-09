from django.shortcuts import render, get_object_or_404
import time, os, base64
from django.contrib.auth.models import User
from .models import (
    Client,
    Claves,
    PagosCliente,
    CodigoSII,
    GiroRubro,
    RegTributario,
    TipoContabilidad,
)
from .forms import (
    ClientForm,
    ClaveForm,
    PagosClienteForm,
    PagosClienteUpdateForm,
    ExportClavesForm,
    PagosExportSelectForm
)
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .static.py.aes import AES
from .static.py.exportar_clientes import exportar_clientes_main, exportar_cliente
from .static.py.exportar_pagos import exportar_pagos_deuda, exportar_pagos_historial
from .static.py.exportar_claves import exportar_claves_all, exportar_clave
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.db.models import OuterRef, Subquery

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

@login_required
@permission_required('gestion.export_client', raise_exception=True)
def ClientExportAll(request):
    clientes = Client.objects.all()
    pagos = PagosCliente.objects.all()
    msg = exportar_clientes_main(clientes, pagos)
    return render(request, 'clients/msg_exportacion.html', { 'msg': msg })

@login_required
@permission_required('gestion.export_client', raise_exception=True)
def ClientExport(request, pk):
    cliente = get_object_or_404(Client, pk=pk)
    pagos = PagosCliente.objects.all()
    msg = exportar_cliente(cliente, pagos)
    return render(request, 'clients/msg_exportacion.html', { 'msg': msg })

@method_decorator([login_required, permission_required('gestion.view_client', raise_exception=True)], name='dispatch')
class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clientes'
    ordering = ['last_name_1_rep_legal']

@method_decorator([login_required, permission_required('gestion.view_client', raise_exception=True)], name='dispatch')
class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/detail.html'
    context_object_name = 'c'
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            cliente = self.object
            context['pagos'] = PagosCliente.objects.filter(client=cliente).last()
            context['claves'] = Claves.objects.filter(client=cliente).last()
            return context
    
@method_decorator([login_required, permission_required('gestion.change_client', raise_exception=True)], name='dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'clients/update.html'
    form_class = ClientForm
    success_url = reverse_lazy('list_clients')

@method_decorator([login_required, permission_required('gestion.add_client', raise_exception=True)], name='dispatch')
class ClientCreateView(CreateView):
    model = Client
    template_name = 'clients/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('create_clave')

    def form_valid(self, form):
        form.instance.nombre_rep_legal = str(form.instance.nombre_rep_legal).capitalize()
        form.instance.last_name_1_rep_legal = str(form.instance.last_name_1_rep_legal).capitalize()
        form.instance.last_name_2_rep_legal = str(form.instance.last_name_2_rep_legal).capitalize()
        form.instance.address = str(form.instance.address).title()

        form.save()
        global client_id
        client_id = form.instance.id
        return super().form_valid(form)

@method_decorator([login_required, permission_required('gestion.delete_client', raise_exception=True)], name='dispatch')
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

@permission_required('gestion.export_pagos', raise_exception=True)
def PagosExportSelect(request):
    if request.method == 'POST':
        form = PagosExportSelectForm(request.POST)
        if form.is_valid():
            mes = form.cleaned_data['mes']

            if mes == "mes":
                return PagosExport(request)
            if mes == "historica":
                return PagosExportHistorial(request)
    else:
        form = PagosExportSelectForm()
    return render(request, 'pagos/export.html', {'form': form})

@permission_required('gestion.export_pagos', raise_exception=True)
def PagosExport(request): # pagos de este mes, que no sean 0
    now = timezone.now()
    ultimo_pago = PagosCliente.objects.filter(
        client=OuterRef('client')
    ).order_by('-created_at')
    pagos_recientes = PagosCliente.objects.filter(
        pk=Subquery(ultimo_pago.values('pk')[:1])
    )
    con_deuda = pagos_recientes.filter(
    a_pagar__gt=0,
    created_at__year=now.year,
    created_at__month=now.month
    )   

    msg = exportar_pagos_deuda.add_rows(self=exportar_pagos_deuda, deudas=con_deuda)
    return render(request, 'pagos/msg_exportacion.html', { 'msg': msg })

@permission_required('gestion.export_pagos', raise_exception=True)
def PagosExportHistorial(request): # pagos de meses anteriores
    now = timezone.now()
    pagos = PagosCliente.objects.all()
    primer_dia_mes = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    pagos_historial = pagos.filter(created_at__lt=primer_dia_mes)
    if pagos_historial.count() == 0:
        raise PermissionDenied("No existen pagos históricos que extraer")
    msg = exportar_pagos_historial.add_rows(self=exportar_pagos_historial, pagos=pagos_historial)
    return render(request, 'pagos/msg_exportacion.html', { 'msg': msg })

@method_decorator([login_required, permission_required('gestion.add_pagoscliente', raise_exception=True)], name='dispatch')
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

@method_decorator([login_required, permission_required('gestion.view_pagoscliente', raise_exception=True)], name='dispatch')
class PagosListView(ListView):
    model = PagosCliente
    template_name = "pagos/list.html"
    context_object_name = 'pagos'
    ordering = ['created_at']

@method_decorator([login_required, permission_required('gestion.view_pagoscliente', raise_exception=True)], name='dispatch')
class PagosDetailView(DetailView):
    model = PagosCliente
    template_name = 'pagos/detail.html'
    context_object_name = 'p'

@method_decorator([login_required, permission_required('gestion.delete_pagoscliente', raise_exception=True)], name='dispatch')
class PagosDeleteView(DeleteView):
    model = PagosCliente
    template_name = 'pagos/delete.html'
    success_url = reverse_lazy('list_pagos')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        now = timezone.now()
        created = self.object.created_at
        curr_user = self.request.user.groups.all()

        if (created.year != now.year or created.month != now.month) and curr_user[0].name != "Administrador":
            raise PermissionDenied("Las declaraciones históricas no se pueden eliminar.")

        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator([login_required, permission_required('gestion.change_pagoscliente', raise_exception=True)], name='dispatch')
class PagosUpdateView(UpdateView):
    model = PagosCliente
    template_name = "pagos/update.html"
    form_class = PagosClienteUpdateForm
    success_url = reverse_lazy('list_pagos')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        q = PagosCliente.objects.filter(id=form.instance.id).order_by('-created_at').first()
        obj = q.created_at if q else None
        now = timezone.now()
        curr_user = self.request.user.groups.all()

        if (obj.year != now.year or obj.month != now.month) and curr_user[0].name != "Administrador":
            raise PermissionDenied("Las declaraciones históricas no se pueden modificar.")
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
    
### Claves Views ###
@login_required
@permission_required('gestion.export_claves', raise_exception=True)
def ClavesExportarCliente(request, pk): # exportar un conjunto de claves
    users = User.objects.all()
    clave = get_object_or_404(Claves, pk=pk)
    msg = []

    if request.method == "POST":
        form = ExportClavesForm(request.POST)
        user = request.user
        if form.is_valid():
            req_pass = form.cleaned_data['password']
            authenticated_user = authenticate(request, username=user.username, password=req_pass)
            if authenticated_user is None:
                print("Authentication failed")
                return render(request, 'claves/msg_exportacion.html', {'msg': "Contraseña incorrecta."})
            
            db_user = users.get(username=user)
            user_password = db_user.password
            key = bytes(user_password.encode())
            key = key.rjust(16, b'\0')[:16]
            aes = AES(key)
            msg = exportar_clave.export(
                self=exportar_clave,
                client=clave,
                aes=aes
            )

        if len(msg) >= 1:
            return render(request, 'claves/msg_exportacion.html', {'msg': msg})
    else:
        form = ExportClavesForm()

    initial_msg = f"Para exportar las claves de {clave.client.nombre_rep_legal} {clave.client.last_name_1_rep_legal} {clave.client.last_name_2_rep_legal}"
    return render(request, 'claves/export-cliente.html', {'msg': initial_msg, 'c': clave, 'form': form})

@method_decorator([login_required, permission_required('gestion.export_claves')], name='dispatch')
class ClavesExportar(FormView): # exportar todas las claves
    claves = Claves.objects.all()
    users = User.objects.all()
    template_name = 'claves/export.html'
    form_class = ExportClavesForm
    success_url = reverse_lazy('list_claves')

    def export(self, request, req_pass):
        msg = []
        user = request.user
        authenticated_user = authenticate(request, username=user.username, password=req_pass)

        if authenticated_user is None:
            msg.clear() if msg else None
            print("Authentication failed")
            return render(request, 'claves/msg_exportacion.html', {'msg': ["Contraseña incorrecta"]})
        else:
            msg.clear() if msg else None
            db_user = self.users.get(username=user)
            user_password = db_user.password
            key = bytes(user_password.encode())
            key = key.rjust(16, b'\0')[:16]
            aes = AES(key)
            try:
                msg = exportar_claves_all.export(
                    self=exportar_claves_all,
                    claves=self.claves,
                    aes=aes
                )
            except UnicodeDecodeError:
                raise PermissionDenied("Solo se pueden extraer todos los conjuntos de claves cuando estos son creados por un mismo usuario.")

            if len(msg) >= 1:
                return render(request, 'claves/msg_exportacion.html', {'msg': msg})
            else:
                return render(request, 'claves/msg_exportacion.html', {'msg': ["Ocurrió un error al exportar"]})

    def form_valid(self, form):
        password = form.cleaned_data.get("password")
        return self.export(self.request, password)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

@login_required
def get_aes_key(request):
    users = User.objects.all()
    if request.user.is_authenticated:
        current_user = request.user
        db_user = users.get(username=current_user)
        user_password = db_user.password
        key = bytes(user_password.encode())
        return key

@method_decorator([login_required, permission_required('gestion.add_claves', raise_exception=True)], name='dispatch')
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
            key = get_aes_key(request).rjust(16, b'\0')[:16]
            iv = os.urandom(16)
            aes = AES(key)

            def encrypt_field(value):
                data = value.encode('utf-8')
                encrypted = aes.encrypt_cfb(data, iv)
                return base64.b64encode(encrypted).decode('utf-8')

            form.instance.unica = encrypt_field(form.cleaned_data['unica'])
            form.instance.sii = encrypt_field(form.cleaned_data['sii'])
            form.instance.factura_electronica = encrypt_field(form.cleaned_data['factura_electronica'])
            form.instance.dir_trabajo = encrypt_field(form.cleaned_data['dir_trabajo'])
            form.instance.iv = iv

            form.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

@method_decorator([login_required, permission_required('gestion.view_claves', raise_exception=True)], name='dispatch')
class ClaveListView(ListView):
    model = Claves
    template_name = 'claves/list.html'
    context_object_name = 'claves'

@method_decorator([login_required, permission_required('gestion.view_claves', raise_exception=True)], name='dispatch')
class ClaveDetailView(DetailView):
    model = Claves
    template_name = 'claves/detail.html'
    context_object_name = 'c'

@method_decorator([login_required, permission_required('gestion.delete_claves', raise_exception=True)], name='dispatch')
class ClaveDeleteView(DeleteView):
    model = Claves
    template_name = 'claves/delete.html'
    success_url = reverse_lazy('list_claves')

### list views ###

def ListViews(request):
    return render(request, 'lists/menu.html')

@method_decorator([login_required, permission_required('gestion.view_codigosii', raise_exception=True)], name='dispatch')
class CodigoSIIListView(ListView):
    model = CodigoSII
    template_name = 'lists/codigosii.html'
    context_object_name = 'codigos'
    ordering = ['code']

@method_decorator([login_required, permission_required('gestion.view_girorubro', raise_exception=True)], name='dispatch')
class GiroRubroListView(ListView):
    model = GiroRubro
    template_name = 'lists/girorubro.html'
    context_object_name = 'id'
    ordering = ['name']

@method_decorator([login_required, permission_required('gestion.view_regtributario', raise_exception=True)], name='dispatch')
class RegTributarioListView(ListView):
    model = RegTributario
    template_name = 'lists/regs.html'
    context_object_name = 'id'
    ordering = ['name']

@method_decorator([login_required, permission_required('gestion.view_tipocontabilidad', raise_exception=True)], name='dispatch')
class TipoContabilidadListView(ListView):
    model = TipoContabilidad
    template_name = 'lists/tiposcont.html'
    context_object_name = 'id'
    ordering = ['name']