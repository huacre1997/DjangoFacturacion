from django.forms import *
from .models import  User
from datetime import datetime
from tempus_dominus.widgets import DatePicker,TimePicker,DateTimePicker
class UserForm(ModelForm):
       
   
    class Meta:
        model = User
        fields="__all__"

        exclude=["groups","user_permissions","last_login","date_joined"]
     

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
       