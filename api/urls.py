from django.urls import path,include
from .views  import *
urlpatterns = [
    path("v1/productos/",ProductoList.as_view(),name="producto_list"),
    path("v1/productos/<str:codigo>",ProductoDetalle.as_view(),name="producto_detalle"),
    path("v1/facturas/",FacturaList.as_view(),name="factura_list"),

]
