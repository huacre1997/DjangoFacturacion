from django.db import models
from django.forms import model_to_dict

from bases.models import ClaseModelo


class Categoria(ClaseModelo):
    description = models.CharField(
        max_length=100, verbose_name="Descripción",help_text="Descripcion de la categoría",blank=False)

    def __str__(self):
        return "{}".format(self.description)

    def save(self):
        self.description = self.description.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural = "Categorías"

    def toJSON(self):
        item = model_to_dict(self)
        return item
class SubCategoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text="Descripcion de la categoría"
    )
    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        return item
    def __str__(self):
        return "{}:{}".format(self.categoria.description, self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural = 'Sub Cateorias'
        unique_together = ("categoria", "descripcion")


class Marca(ClaseModelo):
    descripcion = models.CharField(
        max_length=100, help_text="Descripción de la marca", unique=True)

    def __str__(self):
        return "{}".format(self.descripcion)
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Marca,self).save()
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name_plural = 'Marcas'
class Producto(ClaseModelo):
    codigo=models.CharField( max_length=20,unique=True)
    codigo_barra=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=200)
    precio=models.FloatField(default=0)
    stock=models.IntegerField(default=0)
    ultima_compra=models.CharField(null=True,blank=True,max_length=50)
    marca=models.ForeignKey(Marca, verbose_name="Marca", on_delete=models.CASCADE)
    subcategoria=models.ForeignKey(SubCategoria, verbose_name="Sub categoria", on_delete=models.CASCADE)
    def __str__(self):
        return "{}".format(self.descripcion)
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto,self).save()
    def toJSON(self):
        item = model_to_dict(self)
        item['marca'] = self.marca.toJSON()
        item['subcategoria'] = self.subcategoria.toJSON()
        item["precio"]=format(self.precio,".2f")

        return item
    
    class Meta:
        verbose_name_plural = 'Productos'
        unique_together=("codigo","codigo_barra")
