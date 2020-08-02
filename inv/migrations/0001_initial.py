# Generated by Django 3.0.7 on 2020-08-01 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('updatedUsu', models.IntegerField(blank=True, null=True, verbose_name='user.User')),
                ('description', models.CharField(help_text='Descripcion de la categoría', max_length=100, verbose_name='Descripción')),
                ('createdUsu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('updatedUsu', models.IntegerField(blank=True, null=True, verbose_name='user.User')),
                ('descripcion', models.CharField(help_text='Descripción de la marca', max_length=100, unique=True)),
                ('createdUsu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Marcas',
            },
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('updatedUsu', models.IntegerField(blank=True, null=True, verbose_name='user.User')),
                ('descripcion', models.CharField(help_text='Descripcion de la categoría', max_length=100)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.Categoria')),
                ('createdUsu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Sub Cateorias',
                'unique_together': {('categoria', 'descripcion')},
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('updatedUsu', models.IntegerField(blank=True, null=True, verbose_name='user.User')),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('codigo_barra', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=200)),
                ('precio', models.FloatField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('ultima_compra', models.CharField(blank=True, max_length=50, null=True)),
                ('createdUsu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.Marca', verbose_name='Marca')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.SubCategoria', verbose_name='Sub categoria')),
            ],
            options={
                'verbose_name_plural': 'Productos',
                'unique_together': {('codigo', 'codigo_barra')},
            },
        ),
    ]