from django.urls import path

from . import views

app_name = "modulo"

urlpatterns = [
    path("", views.lista_viajes, name="lista"),
    path("nuevo/", views.crear_viaje, name="crear"),
    path("<int:pk>/", views.detalle_viaje, name="detalle"),
    path("<int:pk>/editar/", views.editar_viaje, name="editar"),
    path("<int:pk>/eliminar/", views.eliminar_viaje, name="eliminar"),
]