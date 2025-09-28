from django.contrib import admin
from .models import Client, Region, Comuna, CodigoSII, RegTributario, TipoContabilidad, Claves, GiroRubro

# Register your models here.
admin.site.register(Client)
admin.site.register(Claves)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(CodigoSII)
admin.site.register(RegTributario)
admin.site.register(TipoContabilidad)
admin.site.register(GiroRubro)