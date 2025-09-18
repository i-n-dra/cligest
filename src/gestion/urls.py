from django.urls import path
from .views import ClientListView

urlpatterns = [
    path("list-clients/", ClientListView.as_view(), name="list_clients"),
    path("create-client/", ClientListView.as_view(), name="create_client")
]
