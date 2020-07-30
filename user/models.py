from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings
class User(AbstractUser):
    dni=models.CharField(max_length=8)
    image=models.ImageField(upload_to="users/%Y/%m/%d",null=True,blank=True)
    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL,self.image)
        return '{}{}'.format(settings.STATIC_URL,"img/user.png")
