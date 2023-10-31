
# Generated by Django 3.0.3 on 2023-10-24 19:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elementos',
            fields=[
                ('fechaElemento', models.DateField()),
                ('nombreElemento', models.CharField(max_length=25)),
                ('categoriaElemento', models.CharField(choices=[('C', 'Consumible'), ('D', 'Devolutivo')], default='C', max_length=25)),
                ('estadoElemento', models.CharField(choices=[('G', 'Garantia'), ('B', 'Baja'), ('D', 'Disponible')], default='D', max_length=25)),
                ('descripcionElemento', models.CharField(max_length=25)),
                ('observacionElemento', models.CharField(max_length=25)),
                ('cantidadElemento', models.IntegerField()),
                ('valorUnidadElemento', models.IntegerField()),
                ('valorTotalElemento', models.IntegerField()),
                ('serialSenaElemento', models.CharField(max_length=25)),
                ('facturaElemento', models.ImageField(blank=True, null=True, upload_to='facturaElemento/')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('fechaEntrega', models.DateField()),
                ('fechaDevolucion', models.DateField()),
                ('observacionesPrestamo', models.CharField(max_length=25)),
                ('firmaDigital', models.ImageField(blank=True, null=True, upload_to='firmaDigital/')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UsuariosSena',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nombres', models.CharField(max_length=25)),
                ('apellidos', models.CharField(max_length=25)),
                ('tipoIdentificacion', models.CharField(choices=[('CC', 'Cedula de ciudadania'), ('TI', 'Tarjeta de identidad'), ('PEP', 'Permiso especial de permanencia'), ('O', 'Otro')], default='CC', max_length=25)),
                ('numeroIdentificacion', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=25)),
                ('celular', models.CharField(max_length=10)),
                ('rol', models.CharField(choices=[('superAdmin', 'super Administrador'), ('I', 'instructor'), ('M', 'Monitor')], default='I', max_length=25)),
                ('cuentadante', models.CharField(choices=[('adminS', 'administrador Solidario'), ('adminD', 'administrador Directo'), ('monitor', 'monitor')], default='adminD', max_length=25)),
                ('tipoContrato', models.CharField(choices=[('P', 'Planta'), ('C', 'Contratista'), ('A', 'Aprendiz')], default='P', max_length=25)),
                ('is_active', models.BooleanField(default=1)),
                ('duracionContrato', models.CharField(max_length=25)),
                ('password', models.CharField(default='', max_length=30)),
                ('fotoUsuario', models.ImageField(blank=True, null=True, upload_to='usuarioFoto/')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-23 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elementos',
            fields=[
                ('fechaElemento', models.DateField()),
                ('nombreElemento', models.CharField(max_length=25)),
                ('categoriaElemento', models.CharField(choices=[('C', 'Consumible'), ('D', 'Devolutivo')], default='C', max_length=25)),
                ('estadoElemento', models.CharField(choices=[('G', 'Garantia'), ('B', 'Baja'), ('D', 'Disponible')], default='D', max_length=25)),
                ('descripcionElemento', models.CharField(max_length=25)),
                ('observacionElemento', models.CharField(max_length=25)),
                ('cantidadElemento', models.IntegerField()),
                ('valorUnidadElemento', models.IntegerField()),
                ('valorTotalElemento', models.IntegerField()),
                ('serialSenaElemento', models.CharField(max_length=25)),
                ('facturaElemento', models.ImageField(blank=True, null=True, upload_to='facturaElemento/')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('fechaEntrega', models.DateField()),
                ('fechaDevolucion', models.DateField()),
                ('nombreEntrega', models.CharField(max_length=25)),
                ('nombreRecibe', models.CharField(max_length=25)),
                ('observacionesPrestamo', models.CharField(max_length=25)),
                ('firmaDigital', models.ImageField(blank=True, null=True, upload_to='firmaDigital/')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SalidaConsumibles',
            fields=[
                ('nombreEntrega', models.CharField(max_length=25)),
                ('nombreRecibe', models.CharField(max_length=25)),
                ('observacionesPrestamo', models.CharField(max_length=25)),
                ('firmaDigital', models.ImageField(blank=True, null=True, upload_to='firmaDigital/')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UsuariosSena',
            fields=[
                ('nombre', models.CharField(max_length=25)),
                ('apellidoo', models.CharField(max_length=25)),
                ('tipoIdentificacion', models.CharField(choices=[('CC', 'Cedula de ciudadania'), ('TI', 'Tarjeta de identidad'), ('PEP', 'Permiso especial de permanencia'), ('O', 'Otro')], default='CC', max_length=25)),
                ('numeroIdentificacion', models.CharField(max_length=25)),
                ('correoSena', models.EmailField(max_length=254)),
                ('celular', models.CharField(max_length=10)),
                ('rol', models.CharField(choices=[('superAdmin', 'super Administrador'), ('I', 'instructor'), ('M', 'Monitor')], default='I', max_length=25)),
                ('cuentadante', models.CharField(choices=[('adminS', 'administrador Solidario'), ('adminD', 'administrador Directo'), ('monitor', 'monitor')], default='adminD', max_length=25)),
                ('tipoContrato', models.CharField(choices=[('P', 'Planta'), ('C', 'Contratista'), ('A', 'Aprendiz')], default='P', max_length=25)),
                ('duracionContrato', models.CharField(max_length=25)),
                ('estadoUsuario', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=25)),
                ('contraSena', models.CharField(max_length=25)),
                ('validacionContraSena', models.CharField(max_length=25)),
                ('fotoUsuario', models.ImageField(blank=True, null=True, upload_to='usuarioFoto/')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]

