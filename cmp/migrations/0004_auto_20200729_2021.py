# Generated by Django 3.0.7 on 2020-07-30 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0003_auto_20200615_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprasdet',
            name='updatedUsu',
            field=models.IntegerField(blank=True, null=True, verbose_name='user.User'),
        ),
        migrations.AlterField(
            model_name='comprasenc',
            name='updatedUsu',
            field=models.IntegerField(blank=True, null=True, verbose_name='user.User'),
        ),
        migrations.AlterField(
            model_name='proovedor',
            name='updatedUsu',
            field=models.IntegerField(blank=True, null=True, verbose_name='user.User'),
        ),
    ]
