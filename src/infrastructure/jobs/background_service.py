
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from src.infrastructure.logging.config import logger

scheduler = BackgroundScheduler()


# Tarea que queremos ejecutar periódicamente
def my_scheduled_job():
    logger.info("Ejecutando tarea programada...")
    # Aquí iría la lógica de la tarea que deseas ejecutar
    # Por ejemplo, podrías consultar una API, actualizar una base de datos, etc.

# Agregamos la tarea al scheduler (cada 10 segundos)
scheduler.add_job(my_scheduled_job, trigger=CronTrigger(hour= 3, minute=0, second=0), id='my_job_id', replace_existing=True)