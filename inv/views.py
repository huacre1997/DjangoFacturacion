from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import *
import json
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, ProductForm
# Create your views here.


class CategoriaView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class CategoriaNew(LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    login_url = "bases:login"

    def post(self, request, *args, **kwargs):
        data = {}
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.instance.createdUsu = self.request.user
            form.save()
            data = {
                'stat': 'ok',
                'form': render_to_string(self.template_name, {'form': form}, request=request)
            }
            return JsonResponse(data)
        else:
            return render(request, self.template_name, {'form': form})


class CategoriaEdit(LoginRequiredMixin, generic.UpdateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:categoria_list")
    login_url = "bases:login"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updatedUsu = self.request.user.id
        return super().form_valid(form)



class CategoriaDel(LoginRequiredMixin, generic.DeleteView):
    model = Categoria
    template_name = "inv/catalogo_del.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:categoria_list")


class SubCategoriaView(LoginRequiredMixin, generic.ListView):
    model = SubCategoria
    template_name = "inv/subcategoria_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class SubCategoriaNew(LoginRequiredMixin, generic.CreateView):
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inv:subcategoria_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.createdUsu = self.request.user
        return super().form_valid(form)


class SubCategoriaEdit(LoginRequiredMixin, generic.UpdateView):
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inv:subcategoria_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.updatedUsu = self.request.user.id
        return super().form_valid(form)


class SubCategoriaDel(LoginRequiredMixin, generic.DeleteView):
    model = SubCategoria
    template_name = "inv/subcatalogo_del.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inv:subcategoria_list")


class MarcaView(LoginRequiredMixin, generic.ListView):
    model = Marca
    template_name = "inv/marca_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class MarcaNew(LoginRequiredMixin, generic.CreateView):
    model = Marca
    template_name = "inv/marca_form.html"
    context_object_name = "obj"
    form_class = MarcaForm
    success_url = reverse_lazy("inv:marca_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.createdUsu = self.request.user
        return super().form_valid(form)


class MarcaEdit(LoginRequiredMixin, generic.UpdateView):
    model = Marca
    template_name = "inv/marca_form.html"
    context_object_name = "obj"
    form_class = MarcaForm
    success_url = reverse_lazy("inv:marca_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.updatedUsu = self.request.user.id
        return super().form_valid(form)


def marca_inactivar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inv/catalogo_del.html"
    if not marca:
        redirect("inv:marca_list")
    if request.method == "GET":
        contexto = {"obj": marca}
    else:
        marca.estado = False
        marca.save()
        return redirect("inv:marca_list")
    return render(request, template_name, contexto)


class ProductoView(LoginRequiredMixin, generic.ListView):
    model = Producto
    template_name = "inv/product_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class ProductoNew(LoginRequiredMixin, generic.CreateView):
    model = Producto
    template_name = "inv/product_form.html"
    context_object_name = "obj"
    form_class = ProductForm
    success_url = reverse_lazy("inv:product_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.createdUsu = self.request.user
        return super().form_valid(form)


class ProductoEdit(LoginRequiredMixin, generic.UpdateView):
    model = Producto
    template_name = "inv/product_form.html"
    context_object_name = "obj"
    form_class = ProductForm
    success_url = reverse_lazy("inv:product_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.updatedUsu = self.request.user.id
        return super().form_valid(form)


def producto_inactivar(request, id):
    prod = Producto.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inv/catalogo_del.html"
    if not prod:
        redirect("inv:product_list")
    if request.method == "GET":
        contexto = {"obj": prod}
    if request.method == "POST":
        prod.estado = False
        prod.save()
        return redirect("inv:product_list")

    return render(request, template_name, contexto)
