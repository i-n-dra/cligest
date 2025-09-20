from django.urls import path
from .views import (
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClavesCreateView,
    TestView
)

urlpatterns = [
    # Clientes
    path("list-clients/", ClientListView.as_view(), name="list_clients"),
    path("create-client/", ClientCreateView.as_view(), name="create_client"),
    path("detail-client/<int:pk>", ClientDetailView.as_view(), name="detail_client"),

    # Claves
    path("create-claves/", ClavesCreateView.as_view(), name="create_claves"),
    path("test/", TestView.as_view(), name="test")
]
