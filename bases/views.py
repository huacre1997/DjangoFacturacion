from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import User
from fac.models import FacturaEnc,FacturDet
from inv.models import Producto
from django.utils.decorators import method_decorator
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
import json

class LoginFormView(generic.FormView):
    form_class=AuthenticationForm
    template_name="bases/login.html"
    success_url=reverse_lazy("bases:casa")
    def dispatch(self,request,*args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        lo  gin(self.request,form.get_user())
        return HttpResponseRedirect(self.success_url)

class LogoutView(generic.RedirectView):
    pattern_name = 'bases:login'
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
class DashBoardView(LoginRequiredMixin,generic.TemplateView):
    template_name="bases/dashboard.html"
   
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="get_graph_Sales":
                data=self.get_graph_sales()
            elif  action=="get_graph_products":
                data=self.get_graph_products()
            elif  action=="get_graph_empleado":
                data=self.get_graph_empleado()
            else:
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            pass
        return JsonResponse(data,safe=False)
    def get_graph_empleado(self):
        data=[]
        try: 
            for m in range(0,12):
                for user in User.objects.all():
                    total=FacturaEnc.objects.filter(uc=user.id,fecha__month=m).aggregate(r=Coalesce(Sum("total"),0)).get("r") 
                    
                    data.append([user.id,m,float(total)])
            print(data)
        except Exception as e:
            print(e)
        return data
    def get_graph_products(self):
        data=[]
        try:
            month=datetime.now().month
            year=datetime.now().year
            for p in Producto.objects.all():
                total=FacturDet.objects.filter(factura_id__fecha__year=year,factura_id__fecha__month=month,producto=p.id).aggregate(r=Coalesce(Sum("sub_total"),0)).get("r")           
                data.append(    {
                    "name":p.descripcion,
                    "y":float(total)
                })
            
        
        except Exception as e:
            print(e)
        return data
    def get_graph_sales(self):
        data=[]
        try:
            year=datetime.now().year
            for m in range(1,13):
                total=FacturaEnc.objects.filter(fecha__year=year,fecha__month=m).aggregate(r=Coalesce(Sum("total"),0)).get("r")           
                data.append(float(total))

        except Exception as e:
            print(e)
        return data
    def get_empleados(self):
        data=[]
        data.append("0")
     
        for item in User.objects.all().order_by("id"):
            data.append(item.first_name)
        return data  
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        # context["report_sales_year"] = self.get_graph_sales()
        context["empleado"]=json.dumps(self.get_empleados())
        print(context)
        return context
        