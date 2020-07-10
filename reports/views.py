from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReportForm
class ReportSaleView(LoginRequiredMixin,generic.TemplateView):
    template_name="reports/reports.html"
    login_url = "bases:login"
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(**kwargs)
        context["form"]=ReportForm()
        return context
