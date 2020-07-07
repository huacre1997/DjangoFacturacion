from django.urls import path
from .views import *
urlpatterns = [
    path("categorias/",CategoriaView.as_view(),name="categoria_list"),
    path("categorias/new",CategoriaNew.as_view(), name="categoria_new"),
    path("categorias/edit/<int:pk>",CategoriaEdit.as_view(), name="categoria_edit"),
    path("categorias/delete/<int:pk>",CategoriaDel.as_view(), name="categoria_del"),
    
    path("subcategorias/",SubCategoriaView.as_view(),name="subcategoria_list"),
    path("subcategorias/new",SubCategoriaNew.as_view(),name="subcategoria_new"),
    path("subcategorias/edit/<int:pk>",SubCategoriaEdit.as_view(), name="subcategoria_edit"),
    path("subcategorias/delete/<int:pk>",SubCategoriaDel.as_view(), name="subcategoria_del"),
    
    path("marcas/",MarcaView.as_view(),name="marca_list"),
    path("marcas/new",MarcaNew.as_view(), name="marca_new"),
    path("marcas/edit/<int:pk>",MarcaEdit.as_view(), name="marca_edit"),
    path("marcas/inactive/<int:id>",marca_inactivar, name="marca_inactive"),

    path("products/",ProductoView.as_view(),name="product_list"),
    path("products/new",ProductoNew.as_view(), name="product_new"),
    path("products/edit/<int:pk>",ProductoEdit.as_view(), name="product_edit"),
    path("products/inactive/<int:id>",producto_inactivar, name="product_inactive"),
    
]
