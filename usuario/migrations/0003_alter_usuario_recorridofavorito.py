# Generated by Django 4.2.4 on 2024-02-24 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recorrido', '0003_rename_puntos_recorrido_puntointeres'),
        ('usuario', '0002_remove_usuario_apellido_usuario_recorridofavorito_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='recorridoFavorito',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recorridoFavorito', to='recorrido.recorrido'),
        ),
    ]
