# Generated by Django 3.2.12 on 2023-09-26 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsuariosSena', '0002_usuariossena_fotousuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementos',
            name='facturaElemento',
            field=models.ImageField(blank=True, null=True, upload_to='facturaElemento/'),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='firmaDigital',
            field=models.ImageField(blank=True, null=True, upload_to='firmaDigital/'),
        ),
    ]
