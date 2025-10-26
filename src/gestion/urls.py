from django.urls import path
from . import views
from .views import (
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClavesCreateView,
    ClaveDetailView,
    ClaveListView,
    ClaveDeleteView,
    ClaveUpdateView,
    ClavesExportar,
    ClavesExportarCliente,
    ClientDeleteView,
    PagosCreateView,
    PagosListView,
    PagosUpdateView,
    PagosDeleteView,
    PagosDetailView,
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
    path("create-clave/", ClavesCreateView.as_view(), name="create_clave"),
    path("list-claves/", ClaveListView.as_view(), name="list_claves"),
    path("update-clave/<int:pk>", ClaveUpdateView.as_view(), name="update_clave"),
    path("detail-clave/<int:pk>", ClaveDetailView.as_view(), name="detail_clave"),
    path("delete-clave/<int:pk>", ClaveDeleteView.as_view(), name="delete_clave"),
    path("export-claves/", ClavesExportar.as_view(), name="export_claves"),
    path("export-claves/<int:pk>", ClavesExportarCliente.as_view(), name="export_claves_client"),

    # Pagos
    path("list-pagos/", PagosListView.as_view(), name="list_pagos"),
    path("create-pago/", PagosCreateView.as_view(), name="create_pago"),
    path("update-pago/<int:pk>", PagosUpdateView.as_view(), name="update_pago"),
    path("detail-pago/<int:pk>", PagosDetailView.as_view(), name="detail_pago"),
    path("delete-pago/<int:pk>", PagosDeleteView.as_view(), name="delete_pago"),
    path("export-pagos/", views.ClientExport, name="export_pagos"),
]
