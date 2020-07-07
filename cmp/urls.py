from .views import *

from django.urls import path
from .reportes import reportes_Compras,imprimir_compra
urlpatterns = [
    path("proveedor/",ProveedorView.as_view(),name="proveedor_list"),
    path("proveedor/new",ProveedorNew.as_view(), name="proveedor_new"),
    path("proveedor/edit/<int:pk>",ProveedorEdit.as_view(), name="proveedor_edit"),
    path("proveedor/inactive/<int:id>",proveedor_inactivar, name="proveedor_inactive"),
    path("proveedor/active/<int:id>",proveedor_activar, name="proveedor_active"),
    path("compras/",ComprasView.as_view(),name="compras_list"),
    path("compras/new",Compras,name="compras_new"),
    path("compras/edit/<int:compra_id>",Compras,name="compras_edit"),

    path("compras/<int:compra_id>/delete/<int:pk>",CompraDetDelete.as_view(),name="compras_del"),
    path("compras/listado",reportes_Compras,name="compras_print_all"),
    path("compras/<int:compra_id>/imprimir",imprimir_compra,name="compras_print_once")

]
