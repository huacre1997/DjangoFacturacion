from django.contrib import admin

from .models import Categoria


class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Categoria, AuthorAdmin)