# En tu archivo tasks.py
from huey import crontab
from huey.contrib.djhuey import task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Prestamo
# tasks.py
from huey import RedisHuey



# Imprime la ruta del módulo actual
print("Current module path (tasks.py):", __file__)

@task()
def enviar_alerta():
    print("Task 'enviar_alerta' is being executed...")
    prestamos_vigentes = Prestamo.objects.filter(estadoPrestamo='Vigente', fechaDevolucion=timezone.now().date())

    for prestamo in prestamos_vigentes:
        dias_restantes = prestamo.dias_restantes()

        # Agrega mensajes de depuración
        print(f'Prestamo: {prestamo}, Dias Restantes: {dias_restantes}, Fecha Final: {prestamo.fechaDevolucion}, Fecha Actual: {timezone.now().date()}')

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

# Programar la tarea para ejecutarse cada día a una hora específica
enviar_alerta.schedule(crontab(hour=1, minute=0))
