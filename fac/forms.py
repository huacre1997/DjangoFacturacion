from django.forms import *
from .models import Cliente,FacturaEnc,FacturDet
from datetime import datetime
from tempus_dominus.widgets import DatePicker,TimePicker,DateTimePicker

class FacturaEncForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = FacturaEnc
        fields="__all__"
        exclude = ["um", "uc", "fm", "fc","estado"]

        widgets = {
         
            'cliente': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id':"enc_cliente"
            }),
         'fecha': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control ',
                    'id': 'fecha',
                    'data-target': 'fecha',
                    'data-toggle': 'datetimepicker',
                    'readonly': True,

                }
            ),
            'igv': NumberInput(attrs={
                "name":"igv",
                "id":"igv",

                'readonly': True,
                'class': 'form-control',
            }),
            'sub_total': NumberInput(attrs={
                 "name":"sub_total",
                "id":"sub_total",
                'readonly': True,
                'class': 'form-control',
            }),
            'total': NumberInput(attrs={
                "name":"total",
                "id":"total",
                'readonly': True,
                'class': 'form-control',
            })
        }

class ClienteForm(ModelForm):
   
   
    class Meta:
        model = Cliente
        fields=["nombres","apellidos","tipo","celular","estado", "createdUsu"]
        exclude = ["created", "updated", "updatedUsu"]
     

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })
       
    
    

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    def clean_apellidos(self):
        apellidos=self.cleaned_data["apellidos"]
        ap=Cliente.objects.filter(apellidos__iexact=apellidos)

        if self.instance  :
            ap = ap.exclude(pk=self.instance.pk)

        if ap:
            raise forms.ValidationError("El apllido "+apellidos+" ya esta registrado.")
        return apellidos
    def clean_nombres(self):
        nombres=self.cleaned_data["nombres"]

        le=Cliente.objects.filter(nombres__iexact=nombres)

        if self.instance  :
            le = le.exclude(pk=self.instance.pk)

        if le:
            raise forms.ValidationError("El nombre "+nombres+" ya esta registrado.")
        return nombres
