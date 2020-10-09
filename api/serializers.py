from rest_framework import serializers
from inv.models import Producto
from fac.models import Cliente
from fac.models import FacturaEnc
from django.db.models.fields import DateField,DateTimeField
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cliente
        fields="__all__"
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Producto
        fields="__all__"
class FacturaSerializer(serializers.ModelSerializer):
    # cliente_nombres = serializers.CharField(source='cliente.nombres')
    # cliente_apellidos = serializers.CharField(source='cliente.apellidos')
    cliente = ClienteSerializer(required=True)
    # cliente2 = serializers.CharField(source='cliente')
    fc=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # def get_cliente(self, obj):
    #         return '{} {}'.format(obj.cliente.nombres, obj.cliente.apellidos) 
 
 
    class Meta:
        model=FacturaEnc
        fields=('id','cliente','fc','sub_total','igv','total',"estado")