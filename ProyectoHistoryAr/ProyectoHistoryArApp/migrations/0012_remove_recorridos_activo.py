# Generated by Django 4.2.4 on 2024-03-29 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoHistoryArApp', '0011_recorridos_activo_alter_recorridos_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recorridos',
            name='activo',
        ),
    ]