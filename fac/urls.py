from .views import *

from django.urls import path
urlpatterns = [
    path("cliente/",ClienteView.as_view(),name="cliente_list"),
    path("cliente/new",CLienteNew.as_view(),name="cliente_new"),
    path("cliente/edit/<int:pk>/",ClienteEdit.as_view(),name="cliente_edit"),
    path("ventas/",FacturaView.as_view(),name="facturacion_list"),
    path("ventas/new",FacturaNew.as_view(),name="facturacion_new"),
    path("ventas/edit/<int:pk>",FacturaEdit.as_view(),name="facturacion_edit"),
    path("ventas/invoice/pdf/<int:pk>",VentasPdf.as_view(),name="ventas_pdf"),
    path("ventas/new/searchProduct",productoSearch,name="searchProduct"),
    path("ventas/facturaDetail",facturaDetail,name="facturaDetail"),


]
