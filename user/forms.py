from django.forms import *
from .models import User
from datetime import datetime
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class UserForm(ModelForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)

    class Meta:
        model = User
        exclude = ["groups", "user_permissions", "last_login", "date_joined"]
        widgets = {
            'email': EmailInput(attrs={
                "name": "email",
                "id": "email",
                "placeholder": "Ingrese un correo electrónico",
                'class': 'form-control',
            }),
            'password': PasswordInput(render_value=True, attrs={
                "name": "password",
                "id": "password",
                "placeholder": "Contraseña",
                'class': 'form-control',
            })

        }

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
                passwd=self.cleaned_data["password"]
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(passwd)
                else:
                    user = User.objects.get(pk=u.pk) 
                    if user.password != passwd:
                       u.set_password(passwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
