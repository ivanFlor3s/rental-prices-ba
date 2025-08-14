from datetime import datetime
from src.infrastructure.db.session import engine
from sqlalchemy.orm import Session
from src.application.use_cases.department_use_cases import create_department_from_scrapping
from src.domain.scrappers.zonaprop_scrapper import ZonaPropScrapper
from src.domain.scrappers.scrap_url_builder import ZonaPropUrlBuilder
from src.infrastructure.logging.config import logger
from src.infrastructure.logging.scrapping_logger import ScrappingResultLogger
from src.infrastructure.db.models import NeighborhoodModel
from src.infrastructure.repositories.neighborhood_repository import NeighborhoodRepository
from src.domain.entities.scrapping_result import NeighborhoodScrappingResult, ScrappingBatchResult
from src.utils.normalizers import normalized_neighborhood_name
import time, random


def scrap_map_save_for(neighborhood: NeighborhoodModel) -> NeighborhoodScrappingResult:
    """Scrap and save departments for a specific neighborhood."""
    normalized_name = normalized_neighborhood_name(neighborhood.name)
    url = init_url_to_scrap(normalized_name)
    result = NeighborhoodScrappingResult(
        neighborhood_id=neighborhood.id,
        neighborhood_name=neighborhood.name,
        url=url,
        success=False,
        titles=[],
    )
    
    session = None
    try:
        # Get session
        session = Session(engine)
      
        # Init scrapper
        scrapper = ZonaPropScrapper(url, neighborhood=normalized_name)
        logger.info(f"Scrapper initialized for {neighborhood.name} with URL: {url}")

        # Process page and get departments
        departments = scrapper.process_page()
        
        result.titles = [dept.title for dept in departments]

        # Save departments
        departments_saved = 0
        for dept in departments:
            create_department_from_scrapping("zonaprop", neighborhood_id=neighborhood.id, department=dept, session=session)
            departments_saved += 1
            logger.info(f"Department saved for {neighborhood.name}", department=dept)

        session.commit()
        result.success = True
        result.departments_count = departments_saved
        logger.info(f"Scrapping completed successfully for {neighborhood.name}. Saved {departments_saved} departments.")

    except Exception as e:
        error_msg = f"Error scrapping {neighborhood.name}: {str(e)}"
        result.error_message = error_msg
        logger.error(error_msg)
        if session:
            session.rollback()
    finally:
        if session:
            session.close()
    
    return result


 

def init_url_to_scrap(neighborhood: str):
    """Initialize the URL to scrap."""
    urlBuilder = ZonaPropUrlBuilder().set_operation("alquiler").set_neighborhood(neighborhood)
    return urlBuilder.build()

def get_neighborhoods_to_scrap():
    """Get the neighborhoods to scrap."""
    session = Session(engine)
    neighborhood_repo = NeighborhoodRepository(session=session)
    neighborhoods = neighborhood_repo.get_all()
    session.close()
    return neighborhoods

def scrap_map_save() -> ScrappingBatchResult:
    """Scrap and save departments for all neighborhoods."""
    start_time = datetime.now()
    neighborhoods = get_neighborhoods_to_scrap()
    
    if not neighborhoods:
        logger.warning("No neighborhoods found to scrap.")
        return ScrappingBatchResult(
            successful_results=[],
            failed_results=[],
            total_neighborhoods=0,
            total_departments_scraped=0,
            start_time=start_time
        )
    
    logger.info(f"Starting scrapping process for {len(neighborhoods)} neighborhoods.")
    
    batch_result = ScrappingBatchResult(
        successful_results=[],
        failed_results=[],
        total_neighborhoods=len(neighborhoods),
        total_departments_scraped=0,
        start_time=start_time
    )
    
    for neighborhood in neighborhoods:
        logger.info(f"Processing neighborhood: {neighborhood.name}")
        result = scrap_map_save_for(neighborhood)
        time.sleep(random.uniform(1.5, 4.0)) 
        if result.success:
            batch_result.add_successful_result(result)
            logger.info(f"✅ Successfully scraped {neighborhood.name}: {result.departments_count} departments")
        else:
            batch_result.add_failed_result(result)
            logger.error(f"❌ Failed to scrape {neighborhood.name}: {result.error_message}")
    
    batch_result.end_time = datetime.now()
    
    # Save results to log file
    result_logger = ScrappingResultLogger()
    result_logger.log_batch_result(batch_result)
    
    # Log summary
    logger.info("Scrapping process completed!")
    
    return batch_result