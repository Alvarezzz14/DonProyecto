# tasks.py
from celery import Celery
from django.core.mail import send_mail
from django.utils import timezone
from kombu import Exchange, Queue
from .models import Prestamo

from ProyectoSgi.celery import app

@app.task
def enviar_alerta():
    prestamos_vigentes = Prestamo.objects.filter(estadoPrestamo='Vigente', fechaDevolucion=timezone.now())

    for prestamo in prestamos_vigentes:
        dias_restantes = (prestamo.fecha_final - timezone.now().date()).days

        # Agrega mensajes de depuración
        print(f'Prestamo: {prestamo}, Dias Restantes: {dias_restantes}, Fecha Final: {prestamo.fecha_final}, Fecha Actual: {timezone.now().date()}')

        # Verifica las condiciones y envía el correo
        if dias_restantes in [15, 7, 2]:
            mensaje = f'Tu préstamo con fecha límite {prestamo.estadoPrestamo} sigue vigente. Quedan {dias_restantes} días.'
            print(mensaje)
            send_mail(
                'Recordatorio de Préstamo',
                f'Tu préstamo con fecha límite {prestamo.estadoPrestamo} sigue vigente. Quedan {dias_restantes} días.',
                'remitente@example.com',
                ['destinatario@example.com'],
                fail_silently=False,
            )
