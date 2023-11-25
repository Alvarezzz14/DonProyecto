# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue  # Agrega la importación de Queue
from django.conf import settings

# Configuración de Celery
app = Celery('ProyectoSgi')

# Configuración del broker (puedes usar Redis o RabbitMQ)
app.conf.broker_url = 'pyamqp://guest@localhost//'

# Configuración para manejar tareas en segundo plano
app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
)

# Nueva configuración a partir de Celery 6.0
app.conf.broker_connection_retry_on_startup = True
# Importa las tareas de tu aplicación
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
