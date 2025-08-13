
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.infrastructure.logging.config import logger

scheduler = BackgroundScheduler()

# Tarea que queremos ejecutar periódicamente
def run_scrapper_create_deptos_job():
    logger.info("Ejecutando tarea programada...")
    from src.domain.scrappers.zonaprop_scrapper import ZonaPropScrapper
    from src.infrastructure.db.session import get_session
    from src.application.use_cases.department_use_cases import create_department_from_scrapping

    scrapper = ZonaPropScrapper("https://www.zonaprop.com.ar/departamentos-alquiler-capital-federal.html")
    departments = scrapper.process_page()
    with get_session() as session:
        for dept in departments:
            create_department_from_scrapping(dept, session)
            logger.info("Departamento creado desde scrapping", department=dept)
    


# Agregamos la tarea al scheduler (cada 10 segundos)
scheduler.add_job(run_scrapper_create_deptos_job, trigger=CronTrigger(hour= 3, minute=0, second=0), id='create_deptos_from_scrapping', replace_existing=True)
