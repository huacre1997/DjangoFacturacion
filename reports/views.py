from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReportForm
from fac.models import FacturaEnc,FacturDet
from inv.models import Producto
from django.utils.decorators import method_decorator
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime
class DashBoardView(LoginRequiredMixin,generic.TemplateView):
    template_name="reports/dashboard.html"
    login_url = "bases:login"
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
            else:
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            pass
        return JsonResponse(data,safe=False)
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_sales_year"] = self.get_graph_sales()
        return context
        
class ReportSaleView(LoginRequiredMixin,generic.TemplateView):
    template_name="reports/reports.html"
    login_url = "bases:login"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action =="search_report":
                data=[]
                start_date=request.POST.get("start_date","")
                end_date=request.POST.get("end_date","")
                print(start_date)
                print(end_date)

                search=FacturaEnc.objects.all()
                if len(start_date) and len(end_date):
                    search=search.filter(fecha__range=[start_date,end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.cliente.apellidos+" "+s.cliente.nombres,
                        s.fecha.strftime("%Y-%m-%d"),
                        format(s.sub_total,".2f"),
                        format(s.descuento,".2f"),
                        format(s.total,".2f"),
                    ])
                    subtotal= search.aggregate(r=Coalesce(Sum("sub_total"),0)).get("r")
                    descuento= search.aggregate(r=Coalesce(Sum("descuento"),0)).get("r")
                    total= search.aggregate(r=Coalesce(Sum("total"),0)).get("r")

                data.append([
                    "",
                    "",
                    "<strong>Total</strong>",
                    format(subtotal,".2f"),   
                    format(descuento,".2f") ,  
                    format(total,".2f")   

                ])
            else:
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(**kwargs)
        context["form"]=ReportForm()
        return context
