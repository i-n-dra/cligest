from django.urls import path
from .views import (
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClavesCreateView,
    ClientDeleteView,
    TestView
)

urlpatterns = [
    # Clientes
    path("list-clients/", ClientListView.as_view(), name="list_clients"),
    path("create-client/", ClientCreateView.as_view(), name="create_client"),
    path("detail-client/<int:pk>", ClientDetailView.as_view(), name="detail_client"),
    path("update-client/<int:pk>", ClientUpdateView.as_view(), name="update_client"),
    path("delete-client/<int:pk>", ClientDeleteView.as_view(), name="delete_client"),

    # Claves
    path("create-claves/", ClavesCreateView.as_view(), name="create_claves"),
    path("test/<int:pk>", TestView.as_view(), name="test") # pk para testeo
    # en view agregar def get() para tomar el id del cliente y mostrar solo esas claves
]
