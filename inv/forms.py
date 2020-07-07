from django import forms
from .models import Categoria,SubCategoria,Marca,Producto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields=["description","estado"]
        widget={"description":forms.TextInput}
        error_messages = {
            'description': {
                'unique':"Este nombre ya esta registrado",
            },
           
        }    

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in  iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class":"form-control"  
            })
    def clean_description(self):
        description=self.cleaned_data["description"]
        pe=Categoria.objects.filter(description__iexact=description).exists()

        if pe:
            raise forms.ValidationError("La categoria "+description+" ya esta registrada")
        if description=="abc":
            raise forms.ValidationError("El nombre abc no es valido")
    
        return description
    
    
class SubCategoriaForm(forms.ModelForm):
    categoria=forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True).order_by("description")
    )
    class Meta:
        model=SubCategoria
        fields=["categoria","descripcion","estado"]
        labels={"descripcion":"Sub-categoría","estado":"Status"}
        widget={"descripcion":forms.TextInput}
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in  iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class":"form-control"
            })
        self.fields["categoria"].empty_label="Seleccione Categoría"
    
class MarcaForm(forms.ModelForm):
   
    class Meta:
        model=Marca
        fields=["descripcion","estado"]
        labels={"descripcion":"Descripción","estado":"Status"}
        widget={"descripcion":forms.TextInput}
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in  iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class":"form-control"
            })

class ProductForm(forms.ModelForm):
       
    class Meta:
        model=Producto
        fields=["codigo","codigo_barra","descripcion","estado","precio","stock","ultima_compra","marca","subcategoria"]
        widget={"descripcion":forms.TextInput}
        exclude=["created","updated","createdUsu","updatedUsu"]
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in  iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class":"form-control"
            })
        self.fields["ultima_compra"].widget.attrs["readonly"]=True
        self.fields["stock"].widget.attrs["readonly"]=True
 