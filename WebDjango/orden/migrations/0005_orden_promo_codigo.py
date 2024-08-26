# Generated by Django 5.0.6 on 2024-08-19 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden', '0004_orden_direccion_envio'),
        ('promo_codigo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='promo_codigo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promo_codigo.promocodigo'),
        ),
    ]
