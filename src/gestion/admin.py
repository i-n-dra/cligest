from django.contrib import admin
from .models import Client, Region, Comuna, CodigoSII

# Register your models here.
admin.site.register(Client)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(CodigoSII)