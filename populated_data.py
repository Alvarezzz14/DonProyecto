from django.core.management.base import BaseCommand
from faker import Faker
from ProyectoSgi import settings
from UsuariosSena.models import ProductosInventarioDevolutivo, InventarioDevolutivo

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoSgi.settings')

settings.configure(django.setup)
django.setup()


class Command(BaseCommand):
    help = 'Populate data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Crea 100 instancias de ProductosInventarioDevolutivo
        for _ in range(100):
            nombre = fake.word()
            categoria = fake.random_element(elements=('C1', 'C2', 'C3'))
            estado = fake.random_element(elements=('D1', 'D2', 'D3'))
            descripcion = fake.sentence()
            valor_unidad = fake.random_int(min=1, max=1000)
            disponibles = fake.random_int(min=0, max=100)

            producto = ProductosInventarioDevolutivo.objects.create(
                nombre=nombre,
                categoria=categoria,
                estado=estado,
                descripcion=descripcion,
                valor_unidad=valor_unidad,
                disponibles=disponibles
            )

            # Crea instancias de InventarioDevolutivo asociadas al producto
            for _ in range(fake.random_int(min=0, max=5)):
                fecha_registro = fake.date_this_decade()
                observacion = fake.text()
                serial = fake.uuid4()
                factura = fake.file_name()

                InventarioDevolutivo.objects.create(
                    producto=producto,
                    fecha_registro=fecha_registro,
                    observacion=observacion,
                    serial=serial,
                    factura=factura
                )

        self.stdout.write(self.style.SUCCESS('Data populated successfully'))
