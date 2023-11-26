# Importa la clase Huey y la tarea que deseas ejecutar
from huey import RedisHuey
from UsuariosSena.tasks import enviar_alerta


# Crea una instancia de Huey
huey = RedisHuey('tasks')

# Función principal para iniciar el consumidor Huey
def main():
    # Inicia el consumidor Huey con la tarea especificada
    huey_consumer = huey.create_consumer(workers=4)
    huey_consumer.add_consumer('tasks.huey')
    huey_consumer.run()

# Ejecuta la función principal al ejecutar el script
if __name__ == '__main__':
    main()
