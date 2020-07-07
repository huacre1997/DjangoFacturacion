from django.shortcuts import render,get_object_or_404,redirect
from django.template.loader import render_to_string
from datetime import datetime
from .models import FacturaEnc,FacturDet,Cliente
from django.core import serializers
from django.db import transaction

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ClienteForm,FacturaEncForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import json
from inv.models import Producto
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
class ClienteView(LoginRequiredMixin, generic.ListView):
    template_name = "fac/cliente_list.html"
    login_url = "bases:login"
    model=Cliente

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)

    


class CLienteNew(SuccessMessageMixin,LoginRequiredMixin,generic.CreateView):
    model = Cliente
    form_class = ClienteForm
    login_url = "bases:login"
    template_name="fac/cliente_form.html"
    def post(self,request,*args, **kwargs):
        data={}
        action=request.POST["action"]
        if action=="add":
            form=ClienteForm(request.POST)
            if form.is_valid():
                form.instance.createdUsu = self.request.user
                form.save()
                data = {
                'stat': 'ok',
                'form': render_to_string(self.template_name, {'form': form}, request=request)}
                return JsonResponse(data)

            else:
                data = render_to_string(self.template_name,{'form': form}, request=request)
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data["error"]="Nose ha ingresado nada s"
  
   

class ClienteEdit(SuccessMessageMixin,LoginRequiredMixin, generic.UpdateView):
    model = Cliente
    template_name = "fac/cliente_form.html"
    context_object_name = "obj"
    form_class = ClienteForm
    success_url = reverse_lazy("fac:cliente_list")
    login_url = "bases:login"
 
    def dispatch(self,request,*args, **kwargs):
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        action=request.POST["action"]
        if action=="edit":
            form = self.get_form()
            if form.is_valid():
                form.instance.updatedUsu = self.request.user.id
                form.save()
                data = {
                'stat': 'ok',
                'form': render_to_string(self.template_name, {'form': form}, request=request)}
                return JsonResponse(data)
            else:

                html = render_to_string(self.template_name, {"form":form,"obj":self.get_object}, request=request)
                serialized_data = json.dumps({"form": html})
                return HttpResponse(serialized_data,content_type = "application/json")
        else:
            data["error"]="Nose ha ingresado nada"

class FacturaView(LoginRequiredMixin, generic.ListView):
    template_name = "fac/facturacion_list.html"
    login_url = "bases:login"
    model=FacturaEnc
    # def get(self, request, *args, **kwargs):
    #     obj = Proovedor.objects.all().order_by("id")
    #     return render(request, self.template_name, {'obj': obj})
    # def post(self,request,*args, **kwargs):
    #     objects= FacturaEnc.objects.all()
    #     json = serializers.serialize('json', objects)
    #     return HttpResponse(json, content_type='application/json')
    # @method_decorator(csrf_exempt)
    # def dispatch(self,request,*args, **kwargs):
    #     return super().dispatch(request,*args,**kwargs)
    # def post(self,request,*args, **kwargs):
    #     data={}
    #     try:
    #         action=request.POST["action"]
    #         if action=="searchData":
    #             data=[]
    #             for i in FacturaEnc.objects.all():
    #                 data.append(i.toJSON())
                 
    #         else:
    #             data["error"]="Ha ocurrido un error"
    #     except Exception as e:
    #         print(e)
    #     return JsonResponse(data,safe=False)
class FacturaEdit(LoginRequiredMixin,generic.UpdateView):
    template_name="fac/facturacion_details.html"
    login_url = "bases:login"
    model=FacturaEnc
    context_object_name = "obj"
    
class FacturaNew(LoginRequiredMixin,  generic.CreateView):
    template_name="fac/facturacion_form.html"
    login_url = "bases:login"
    model=FacturaEnc
    context_object_name = "obj"
    form_class = FacturaEncForm
    success_url = reverse_lazy('fac:facturacion_list')
    url_redirect=success_url
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request,*args, **kwargs):
        enc = FacturaEnc.objects.last()
        encabezado={
            "id":enc.id+1
        }
        # if not enc:
        #     encabezado = {
        #         'id':"0001",
             
        #     }
        form=FacturaEncForm(request.POST)
        contexto = {"enc":encabezado,"form":form,"action":"add"}
        return render(request,self.template_name,contexto)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            print("la action es "+action)
            if action=="searchProduct":
                data=[]
                prod=Producto.objects.filter(descripcion__icontains=request.POST["term"])
                for i in  prod:
                    item=i.toJSON()
                    item['value'] = i.descripcion
                    item["cantidad"]=request.POST["cantidad"]
                    data.append(item)
            elif action=="add":
                with transaction.atomic():
                    vents=json.loads(request.POST["vents"])
                    enc=FacturaEnc()
                    enc.fecha=vents["fecha"]
                    enc.cliente_id=vents["cliente"]
                    enc.descuento=float(vents["descuento"])
                    enc.sub_total=float(vents["subtotal"])
                    enc.save()
                    for i in vents["products"]:
                        det=FacturDet()
                        det.factura_id=enc.id
                        det.producto_id=i["id"]
                        det.cantidad=int(i["cantidad"])
                        det.precio=float(i["precio"])
                        det.save()
                    data["mensaje"]="guardado"

            else:
                data["error"]="No se ha ingresado una opción"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)

class FacturaEdit(LoginRequiredMixin,  generic.UpdateView):
    model=FacturaEnc
    form_class = FacturaEncForm
    template_name="fac/facturacion_form.html"
    login_url = "bases:login"
    success_url = reverse_lazy('fac:facturacion_list')
    url_redirect=success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_details_product(self):
        data=[]
        try:
            for i in FacturDet.objects.filter(factura_id=self.get_object().id):
                item=i.producto.toJSON()
                item["cantidad"]=i.cantidad
                data.append(item)
        except:
            pass
        return data
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="editarFactura":
                with transaction.atomic():
                    vents=json.loads(request.POST["vents"])
                    enc=self.get_object()
                    enc.fecha=vents["fecha"]
                    enc.cliente_id=vents["cliente"]
                    enc.descuento=float(vents["descuento"])
                    enc.sub_total=float(vents["subtotal"])
                    enc.save()
                    enc.facturdet_set.all().delete()
                    for i in vents["products"]:
                        det=FacturDet()
                        det.factura_id=enc.id
                        det.producto_id=i["id"]
                        det.cantidad=int(i["cantidad"])
                        det.precio=float(i["precio"])
                        det.save()
                    data["mensaje"]="editado"

            else:
                data["error"]="No se ha ingresado una opción"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
        # cliente = request.POST.get("enc_cliente")
        # fecha= request.POST.get("fecha")
        # cli=Cliente.objects.get(pk=cliente)

        # if not id:
        #     enc = FacturaEnc(
        #         cliente = cli,
        #         fecha = fecha
        #     )
        #     if enc:
        #         enc.save()
        #         id = enc.id
        # else:
        #     enc = FacturaEnc.objects.filter(pk=id).first()
        #     if enc:
        #         enc.cliente = cli
        #         enc.save()

        # if not id:
        #     messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
        #     return redirect("fac:factura_list")
        
        # codigo = request.POST.get("codigo")
        # cantidad = request.POST.get("cantidad")
        # precio = request.POST.get("precio")
        # s_total = request.POST.get("sub_total_detalle")
        # descuento = request.POST.get("descuento_detalle")
        # total = request.POST.get("total_detalle")

        # prod = Producto.objects.get(codigo=codigo)
        # det = FacturDet(
        #     factura = enc,
        #     producto = prod,
        #     cantidad = cantidad,
        #     precio = precio,
        #     sub_total = s_total,
        #     descuento = descuento,
        #     total = total
        # )
        
        # if det:
        #     det.save()
        
        # return redirect("fac:facturacion_edit",id=id)
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(**kwargs)
        context["obj"]=self.get_object()
        context["det"]=json.dumps(self.get_details_product())
        context["action"]="editarFactura"
        return context   
    # html = render_to_string(self.template_name, contexto, request=request)
    # serialized_data = json.dumps({"form": html})
    # return HttpResponse(serialized_data,content_type = "application/json")
@login_required(login_url="/login/")
def productoSearch(request):
    template_name="fac/producto_buscar.html"
    product=Producto.objects.all()
    contexto={"obj":product}
    return render(request,template_name,contexto)
@login_required(login_url="/login/")
@method_decorator(csrf_exempt)
def facturaDetail(request):
    template_name="fac/facturacion_detail.html"
    action=request.POST["action"]
    if action=="search_details":
        data=[]
        enc=FacturaEnc.objects.filter(pk=request.POST["id"])
           
        for i  in FacturDet.objects.filter(factura_id=request.POST["id"]):
            data.append(i.toJSON())
    de = render_to_string(template_name,{"data":data,"enc":enc}, request=request)
    return HttpResponse(json.dumps(de), content_type="application/json")
    # class ProveedorEdit(SuccessMessageMixin,LoginRequiredMixin, generic.UpdateView):
#     model = Proovedor
#     template_name = "cmp/proveedor_form.html"
#     context_object_name = "obj"
#     form_class = ProveedorForm
#     success_url = reverse_lazy("cmp:proveedor_list")
#     success_message="Proveedor editado exitosamente"

#     login_url = "bases:login"

#     def form_valid(self, form):
#         form.instance.updatedUsu = self.request.user.id
#         return super().form_valid(form)
        # data={}
        # action=request.POST["action"]
        # if action=="edit":
        #     form=ClienteForm(request.POST)
        #     if form.is_valid():
        #         form.instance.updatedUsu = self.request.user.id
        #         form.save()
        #         data = {
        #         'stat': 'ok',
        #         'form': render_to_string(self.template_name, {'form': form}, request=request)}
        #         return JsonResponse(data)

        #     else:
        #         data = render_to_string(self.template_name,{'form': form}, request=request)
        #         return HttpResponse(json.dumps(data), content_type="application/json")
        # else:
        #     data["error"]="Nose ha ingresado nada"
  