# Generated by Django 4.2.4 on 2024-02-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoHistoryArApp', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recorridos',
            name='puntoInteres',
            field=models.ManyToManyField(blank=True, related_name='punto_interes', to='ProyectoHistoryArApp.puntosinteres'),
        ),
    ]
