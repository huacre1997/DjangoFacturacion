from .views import *
from django.urls import path
urlpatterns = [
        path("ventas/",ReportSaleView.as_view(),name="report_Ventas"),

]