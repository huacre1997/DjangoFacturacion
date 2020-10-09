from django.db import models
from django.forms import model_to_dict
from inv.models import Producto
from bases.models import ClaseModelo,ClaseModelo2
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.models import User
class Cliente(ClaseModelo):
    NAT="Natural"
    JUR="Jurídica"
    TIPO_CLIENTE={
        (NAT,"Natural"),
        (JUR,"Jurídica")
    }
    nombres=models.CharField(max_length=100,blank=False,unique=True,error_messages={'unique': 'Please enter your name'})
    apellidos=models.CharField(max_length=100,unique=True,blank=False)
    celular=models.CharField(max_length=20,null=True,blank=False,unique=True)
    tipo=models.CharField(max_length=10,choices=TIPO_CLIENTE,default="NAT")
    def __str__(self):
        return "{} {}".format(self.apellidos,self.nombres)
    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Cliente,self).save()
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta: 
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
class FacturaEnc(ClaseModelo2):
    cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE)
    fecha=models.DateField(default=datetime.now)
    sub_total=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    igv=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    def __str__(self):
        return "{}".format(self.id)
    def save(self):
        self.total=self.sub_total+self.igv
        super(FacturaEnc,self).save()
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['sub_total'] = format(self.sub_total, '.2f')
        item['igv'] = format(self.igv, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.facturdet_set.all()]
        return item
class FacturDet(ClaseModelo2):
    factura=models.ForeignKey(FacturaEnc, on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad=models.BigIntegerField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    def __str__(self):
        return "{}".format(self.producto)
    def save(self):
        self.sub_total=float(float(int(self.cantidad))*float(self.precio))
        super(FacturDet,self).save()
    class Meta: 
        verbose_name = 'Detalle Factura'
        verbose_name_plural = 'Detalles Facturas'
    def toJSON(self):
        item = model_to_dict(self)
        item["producto"]=self.producto.toJSON()
        item["sub_total"]=format(self.sub_total,".2f")
        item["precio"]=format(self.precio,".2f")
    
        return item
@receiver(post_save, sender=FacturDet)
def detalle_fac_guardar(sender,instance,**kwargs):
    factura_id = instance.factura.id
    producto_id = instance.producto.id

    prod=Producto.objects.filter(pk=producto_id).first()
    if prod:
        cantidad = int(prod.stock) - int(instance.cantidad)
        prod.stock = cantidad
        prod.save()



