from src.infrastructure.db.session import engine
from sqlalchemy.orm import Session
from src.application.use_cases.department_use_cases import create_department_from_scrapping
from src.domain.scrappers.zonaprop_scrapper import ZonaPropScrapper
from src.domain.scrappers.scrap_url_builder import ZonaPropUrlBuilder
from src.infrastructure.logging.config import logger
from src.infrastructure.repositories.neighborhood_repository import NeighborhoodRepository


def scrap_map_save():
    try:
        # Get caballito neighborhood
        session = Session(engine)
        neighborhood_repo = NeighborhoodRepository(session=session)
        caballito_neighborhood = neighborhood_repo.get_by_name("caballito")

        # Init scrapper
        url = init_url_to_scrap(caballito_neighborhood.name)
        scrapper = ZonaPropScrapper(url)
        logger.info("Scrapper initialized successfully.")

        # Process page and get departments
        departments = scrapper.process_page()
        logger.info("Departments processed successfully.")

        
        for dept in departments:
            create_department_from_scrapping("zonaprop", neighborhood_id=caballito_neighborhood.id, department=dept, session=session)
            logger.info("Departamento creado desde scrapping", department=dept)

        session.commit()
        session.close()
        logger.info("Scrapping and saving completed successfully.")


    except Exception as e:
        logger.error(f"Error in process: {e}")


 

def init_url_to_scrap(neighborhood: str):
    """Initialize the URL to scrap."""
    urlBuilder = ZonaPropUrlBuilder().set_operation("alquiler").set_neighborhood(neighborhood)
    return urlBuilder.build()
