from django.urls import path
from . import views
from .views import (
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClavesCreateView,
    ClientDeleteView,
    PagosCreateView,
    PagosListView,
    PagosUpdateView,
    PagosDeleteView,
    PagosDetailView,
    TestView
)

urlpatterns = [
    # Clientes
    path("list-clients/", ClientListView.as_view(), name="list_clients"),
    path("export-clients/", views.ClientExport, name="export_clients"),
    path("create-client/", ClientCreateView.as_view(), name="create_client"),
    path("detail-client/<int:pk>", ClientDetailView.as_view(), name="detail_client"),
    path("update-client/<int:pk>", ClientUpdateView.as_view(), name="update_client"),
    path("delete-client/<int:pk>", ClientDeleteView.as_view(), name="delete_client"),
    path("create-client/run-validacion/", views.check_run, name="check_run"),
    path("create-client/rut-validacion/", views.check_rut, name="check_rut"),

    # Claves
    path("create-claves/", ClavesCreateView.as_view(), name="create_claves"),
    path("test/<int:pk>", TestView.as_view(), name="test"), # pk para testeo
    # en view agregar def get() para tomar el id del cliente y mostrar solo esas claves

    # Pagos
    path("list-pagos/", PagosListView.as_view(), name="list_pagos"),
    path("create-pago/", PagosCreateView.as_view(), name="create_pago"),
    path("update-pago/<int:pk>", PagosUpdateView.as_view(), name="update_pago"),
    path("detail-pago/<int:pk>", PagosDetailView.as_view(), name="detail_pago"),
]
