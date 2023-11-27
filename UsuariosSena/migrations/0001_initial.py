from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ElementosConsumible",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fechaAdquisicion", models.DateField(auto_now_add=True)),
                ("nombreElemento", models.CharField(max_length=25)),
                (
                    "categoriaElemento",
                    models.CharField(
                        choices=[("D", "Devolutivo"), ("C", "Consumible")],
                        default="C",
                        max_length=25,
                    ),
                ),
                (
                    "estadoElemento",
                    models.CharField(
                        choices=[("D", "Disponible"), ("A", "Agotado")],
                        default="D",
                        max_length=25,
                    ),
                ),
                ("descripcionElemento", models.CharField(max_length=25)),
                ("observacionElemento", models.CharField(max_length=25)),
                ("cantidadElemento", models.IntegerField()),
                ("costoUnidadElemento", models.IntegerField()),
                ("costoTotalElemento", models.IntegerField(blank=True, null=True)),
                (
                    "facturaElemento",
                    models.ImageField(
                        blank=True, null=True, upload_to="facturaElemento/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EntregaConsumible",
            fields=[
                ("fecha_entrega", models.DateField()),
                ("responsable_Entrega", models.CharField(max_length=25)),
                ("nombre_solicitante", models.CharField(max_length=100)),
                ("nombreElemento", models.CharField(max_length=25)),
                ("cantidad_prestada", models.PositiveIntegerField()),
                ("observaciones_prestamo", models.TextField()),
                (
                    "firmaDigital",
                    models.ImageField(blank=True, null=True, upload_to="firmaDigital/"),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="InventarioDevolutivo",
            fields=[
                ("fecha_Registro", models.DateField(auto_now_add=True)),
                ("observacion", models.TextField()),
                (
                    "serial",
                    models.CharField(max_length=25, primary_key=True, serialize=False),
                ),
                (
                    "factura",
                    models.ImageField(
                        blank=True, null=True, upload_to="facturaElemento/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductosInventarioDevolutivo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=75)),
                (
                    "categoria",
                    models.CharField(
                        choices=[("C", "Consumible"), ("D", "Devolutivo")],
                        default="C",
                        max_length=25,
                    ),
                ),
                (
                    "estado",
                    models.CharField(
                        choices=[("G", "Garantia"), ("B", "Baja"), ("D", "Disponible")],
                        default="D",
                        max_length=25,
                    ),
                ),
                ("descripcion", models.CharField(max_length=255)),
                ("valor_unidad", models.IntegerField()),
                ("disponibles", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="UsuariosSena",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("nombres", models.CharField(max_length=25)),
                ("apellidos", models.CharField(max_length=25)),
                (
                    "tipoIdentificacion",
                    models.CharField(
                        choices=[
                            ("CC", "Cedula de ciudadania"),
                            ("TI", "Tarjeta de identidad"),
                            ("PEP", "Permiso especial de permanencia"),
                            ("O", "Otro"),
                        ],
                        default="CC",
                        max_length=25,
                    ),
                ),
                (
                    "numeroIdentificacion",
                    models.CharField(
                        max_length=25, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("email", models.EmailField(max_length=25)),
                ("celular", models.CharField(max_length=10)),
                (
                    "rol",
                    models.CharField(
                        choices=[
                            ("superAdmin", "super Administrador"),
                            ("I", "instructor"),
                            ("M", "Monitor"),
                        ],
                        default="I",
                        max_length=25,
                    ),
                ),
                (
                    "cuentadante",
                    models.CharField(
                        choices=[
                            ("adminS", "administrador Solidario"),
                            ("adminD", "administrador Directo"),
                            ("monitor", "monitor"),
                        ],
                        default="adminD",
                        max_length=25,
                    ),
                ),
                (
                    "tipoContrato",
                    models.CharField(
                        choices=[
                            ("P", "Planta"),
                            ("C", "Contratista"),
                            ("A", "Aprendiz"),
                        ],
                        default="P",
                        max_length=25,
                    ),
                ),
                ("is_active", models.BooleanField(default=1)),
                ("duracionContrato", models.CharField(max_length=25)),
                ("password", models.CharField(default="", max_length=100)),
                (
                    "fotoUsuario",
                    models.ImageField(blank=True, null=True, upload_to="usuarioFoto/"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Prestamo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fechaEntrega", models.DateField()),
                ("fechaDevolucion", models.DateField()),
                ("valorUnidadElemento", models.IntegerField()),
                (
                    "firmaDigital",
                    models.ImageField(blank=True, null=True, upload_to="firmaDigital/"),
                ),
                ("observacionesPrestamo", models.TextField()),
                (
                    "nombreEntrega",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="prestamos_entregados",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "nombreRecibe",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="prestamos_recibidos",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "serialSenaElemento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prestamos",
                        to="UsuariosSena.inventariodevolutivo",
                    ),
                ),
            ],
            options={
                "verbose_name": "Préstamo",
                "verbose_name_plural": "Préstamos",
            },
        ),
        migrations.AddField(
            model_name="inventariodevolutivo",
            name="producto",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="UsuariosSena.productosinventariodevolutivo",
            ),
        ),
    ]
