from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import *
from django.db.models import Sum
import json,datetime    
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from cmp.forms import ProveedorForm,ComprasEncForm
from inv.models import Producto


class ProveedorView(LoginRequiredMixin, generic.ListView):
    template_name = "cmp/proveedor_list.html"
    login_url = "bases:login"

    def get(self, request, *args, **kwargs):
        obj = Proovedor.objects.all().order_by("id")
        return render(request, self.template_name, {'obj': obj})


class ProveedorNew(SuccessMessageMixin,LoginRequiredMixin, generic.CreateView):
    model = Proovedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
    login_url = "bases:login"
    success_message="Proveedor creado exitosamente"

    def form_valid(self, form):
        form.instance.createdUsu = self.request.user
        return super().form_valid(form)
   

class ProveedorEdit(SuccessMessageMixin,LoginRequiredMixin, generic.UpdateView):
    model = Proovedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor editado exitosamente"

    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.updatedUsu = self.request.user.id
        return super().form_valid(form)

@csrf_exempt
def proveedor_inactivar(request, id):
    prov = Proovedor.objects.filter(id=id).last()
    template_name = "cmp/proveedor_list.html"
    contexto = {}
    if not prov:
        return HttpResponse("Proveedor no existe"+str(id))
    if request.method == "GET":
        contexto = {"obj": prov}
    if request.method == "POST":
        prov.estado = False
        prov.save()
        contexto = {"obj": prov}
        messages.success(request,"Proveedor desactivado")

        return HttpResponseRedirect("../../../cmp/proveedor",contexto)
    return render(request, template_name, contexto)

@csrf_exempt
def proveedor_activar(request, id):
    prov = Proovedor.objects.filter(id=id).last()
    template_name = "cmp/proveedor_list.html"
    contexto = {}
    if not prov:
        return HttpResponse("Proveedor no existe"+str(id))
    if request.method == "GET":
        contexto = {"obj": prov}
    if request.method == "POST":
        prov.estado = True
        prov.save()
        messages.success(request,"Proveedor activado")
        contexto = {"obj": prov}
        return HttpResponseRedirect("../../../cmp/proveedor",contexto)
    return render(request, template_name, contexto)
class ComprasView(LoginRequiredMixin, generic.ListView):
    model=ComprasEnc
    template_name="cmp/compras_list.html"
    context_object_name="obj"
    login_url = "bases:login"
def Compras(request,compra_id=None):
    template_name="cmp/compras.html"
    prod=Producto.objects.filter(estado=True)
    form_compras={}
    contexto={}
    login_url = "bases:login"

    if request.method=="GET":
        form_compras=ComprasEncForm()
        enc=ComprasEnc.objects.filter(pk=compra_id).first()

        if enc:
            det=ComprasDet.objects.filter(compra=enc)
            fecha_compra=datetime.date.isoformat(enc.fecha_compra)
            fecha_factura=datetime.date.isoformat(enc.fecha_factura)
            e={
                "fecha_compra":fecha_compra,
                "proveedor":enc.proveedor,
                "observacion":enc.observacion,
                "no_factura":enc.no_factura,
                "fecha_factura":fecha_factura,
                "sub_total":enc.sub_total,
                "descuento":enc.descuento,
                "total":enc.total
            }
            form_compras=ComprasEncForm(e)
        else:
            det=None
        contexto={"productos":prod,"encabezado":enc,"detalle":det,"form_enc":form_compras}

    if request.method=="POST":
        fecha_compra=request.POST.get("fecha_compra")
        observacion=request.POST.get("observacion")
        no_factura=request.POST.get("no_factura")
        fecha_factura=request.POST.get("fecha_factura")
        proveedor=request.POST.get("proveedor")
        sub_total=0
        descuento=0
        total=0
        if not compra_id:
            prov=Proovedor.objects.get(pk=proveedor)
            enc= ComprasEnc(
                fecha_compra=fecha_compra,
                observacion=observacion,
                no_factura=no_factura,
                fecha_factura=fecha_factura,
                proveedor=prov,
                createdUsu=request.user
            )
            if  enc:
                enc.save()
                compra_id=enc.id
        else:
            enc=ComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra=fecha_compra
                enc.observacion=observacion
                enc.no_factura=no_factura
                enc.fecha_factura=fecha_factura
                enc.updatedUsu=request.user.id
                enc.save()
        if not compra_id:
            return redirect("cmp:compras_list")

        producto=request.POST.get("id_id_producto")
        cantidad=request.POST.get("id_cantidad_detalle")
        precio=request.POST.get("id_precio_detalle")
        sub_total_detalle=request.POST.get("id_sub_total_detalle")
        descuento_detalle=request.POST.get("id_descuento_detalle")
        total_detalle=request.POST.get("id_total_detalle")

        prod=Producto.objects.get(pk=producto)
        det=ComprasDet(
            compra=enc,
            producto=prod,
            cantidad=cantidad,
            precio_prv=precio,
            descuento=descuento_detalle,
            costo=0,
            createdUsu=request.user
        )
        if det:
            det.save()
            sub_total=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum("sub_total"))
            descuento=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum("descuento"))
            enc.sub_total=sub_total["sub_total__sum"]
            enc.descuento=descuento["descuento__sum"]
            enc.save()
        return redirect("cmp:compras_edit",compra_id=compra_id)
            
    return render(request,template_name,contexto)



class CompraDetDelete(LoginRequiredMixin, generic.DeleteView):
    model = ComprasDet
    template_name = "cmp/compras_del.html"
    context_object_name = 'obj'
    
    def get_success_url(self):
          compra_id=self.kwargs['compra_id']
          return reverse_lazy('cmp:compras_edit', kwargs={'compra_id': compra_id})