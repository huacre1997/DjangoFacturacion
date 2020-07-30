from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey
from django.conf import settings
class ClaseModelo(models.Model):
    estado=models.BooleanField(default=True);
    created=models.DateTimeField(verbose_name="Fecha de creación",auto_now_add=True)
    updated=models.DateTimeField(verbose_name="Fecha de modificación", auto_now=True)
    createdUsu=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updatedUsu=models.IntegerField(settings.AUTH_USER_MODEL,blank=True,null=True)
    class Meta:
        abstract=True
class ClaseModelo2(models.Model):
    estado=models.BooleanField(default=True);
    fc=models.DateTimeField(verbose_name="Fecha de creación",auto_now_add=True)
    fm=models.DateTimeField(verbose_name="Fecha de modificación", auto_now=True)
    uc=UserForeignKey(auto_user_add="True",related_name="+")
    um=UserForeignKey(auto_user=True,related_name="+")
    class Meta:
        abstract=True
        