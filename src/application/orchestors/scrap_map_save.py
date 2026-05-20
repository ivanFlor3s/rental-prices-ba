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


class ScrappingOrchestrator:
    """Orchestrates the scrapping process for rental properties."""
    
    def __init__(self, min_delay: float = 1.5, max_delay: float = 4.0):
        """
        Initialize the scrapping orchestrator.
        
        Args:
            min_delay: Minimum delay between requests in seconds
            max_delay: Maximum delay between requests in seconds
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.result_logger = ScrappingResultLogger()
    
    def scrap_neighborhood(self, neighborhood: NeighborhoodModel) -> NeighborhoodScrappingResult:
        """Scrap and save departments for a specific neighborhood."""
        normalized_name = normalized_neighborhood_name(neighborhood.name)
        url = self._build_scrapping_url(normalized_name)
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
    
    def scrap_all_neighborhoods(self) -> ScrappingBatchResult:
        """Scrap and save departments for all neighborhoods."""
        start_time = datetime.now()
        neighborhoods = self._get_neighborhoods_to_scrap()
        
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
            result = self.scrap_neighborhood(neighborhood)
            
            # Add random delay to avoid being blocked
            self._apply_rate_limiting()
            
            if result.success:
                batch_result.add_successful_result(result)
                logger.info(f"✅ Successfully scraped {neighborhood.name}: {result.departments_count} departments")
            else:
                batch_result.add_failed_result(result)
                logger.error(f"❌ Failed to scrape {neighborhood.name}: {result.error_message}")
        
        batch_result.end_time = datetime.now()
        
        # Save results to log file
        log_file_path = self.result_logger.log_batch_result(batch_result)
        
        # Log summary
        logger.info("Scrapping process completed!")
        logger.info(batch_result.get_summary())
        logger.info(f"📄 Results saved to: {log_file_path}")
        
        return batch_result
    
    def scrap_specific_neighborhoods(self, neighborhood_names: list) -> ScrappingBatchResult:
        """Scrap specific neighborhoods by name."""
        start_time = datetime.now()
        
        # Get neighborhoods by names
        session = Session(engine)
        neighborhood_repo = NeighborhoodRepository(session=session)
        neighborhoods = []
        
        for name in neighborhood_names:
            neighborhood = neighborhood_repo.get_by_name(name)
            if neighborhood:
                neighborhoods.append(neighborhood)
            else:
                logger.warning(f"Neighborhood '{name}' not found in database")
        
        session.close()
        
        if not neighborhoods:
            logger.warning("No valid neighborhoods found to scrap.")
            return ScrappingBatchResult(
                successful_results=[],
                failed_results=[],
                total_neighborhoods=0,
                total_departments_scraped=0,
                start_time=start_time
            )
        
        logger.info(f"Starting scrapping process for {len(neighborhoods)} specific neighborhoods.")
        
        batch_result = ScrappingBatchResult(
            successful_results=[],
            failed_results=[],
            total_neighborhoods=len(neighborhoods),
            total_departments_scraped=0,
            start_time=start_time
        )
        
        for neighborhood in neighborhoods:
            logger.info(f"Processing neighborhood: {neighborhood.name}")
            result = self.scrap_neighborhood(neighborhood)
            
            # Add random delay
            self._apply_rate_limiting()
            
            if result.success:
                batch_result.add_successful_result(result)
                logger.info(f"✅ Successfully scraped {neighborhood.name}: {result.departments_count} departments")
            else:
                batch_result.add_failed_result(result)
                logger.error(f"❌ Failed to scrape {neighborhood.name}: {result.error_message}")
        
        batch_result.end_time = datetime.now()
        
        # Save results to log file
        log_file_path = self.result_logger.log_batch_result(batch_result)
        
        # Log summary
        logger.info("Scrapping process completed!")
        logger.info(batch_result.get_summary())
        logger.info(f"📄 Results saved to: {log_file_path}")
        
        return batch_result
    
    def _build_scrapping_url(self, neighborhood: str) -> str:
        """Build the URL for scrapping a specific neighborhood."""
        url_builder = ZonaPropUrlBuilder().set_operation("alquiler").set_neighborhood(neighborhood)
        return url_builder.build()
    
    def _get_neighborhoods_to_scrap(self) -> list:
        """Get all neighborhoods available for scrapping."""
        session = Session(engine)
        neighborhood_repo = NeighborhoodRepository(session=session)
        neighborhoods = neighborhood_repo.get_all()
        session.close()
        return neighborhoods
    
    def _apply_rate_limiting(self):
        """Apply rate limiting delay between requests."""
        delay = random.uniform(self.min_delay, self.max_delay)
        logger.debug(f"Applying rate limiting delay: {delay:.2f}s")
        time.sleep(delay)


def scrap_map_save():
    """Main function to initiate the scrapping process."""
    orchestrator = ScrappingOrchestrator()
    
    # Uncomment the next line to scrap all neighborhoods
    # result = orchestrator.scrap_all_neighborhoods()
    
    # Example: scrap specific neighborhoods
    neighborhoods_to_scrap = ["Caballito"]
    result = orchestrator.scrap_specific_neighborhoods(neighborhoods_to_scrap)
    
    return result