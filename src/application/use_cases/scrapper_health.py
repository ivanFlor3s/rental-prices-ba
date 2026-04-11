import logging
from typing import Dict, Any, List

from src.domain.scrappers.zonaprop_scrapper import ZonaPropScrapper
from src.domain.scrappers.scrap_url_builder import ZonaPropUrlBuilder
from src.utils.normalizers import normalized_neighborhood_name

logger = logging.getLogger(__name__)

class ScrapperHealthCheckUseCase:
    """Service to verify the health of the scrapper DOM selectors."""

    def __init__(self, neighborhood_to_test: str = "Palermo", max_samples: int = 5):
        self.neighborhood_to_test = neighborhood_to_test
        self.max_samples = max_samples

    def check_zonaprop_health(self) -> Dict[str, Any]:
        """
        Executes a localized scrap operation and inspects the output to determine
        if the ZonaProp DOM selectors are still functioning correctly.
        """
        normalized_name = normalized_neighborhood_name(self.neighborhood_to_test)
        url_builder = ZonaPropUrlBuilder().set_operation("alquiler").set_neighborhood(normalized_name)
        url = url_builder.build()

        health_report = {
            "source": "zonaprop",
            "neighborhood_tested": self.neighborhood_to_test,
            "status": "broken",
            "scraped_items": 0,
            "fields_failing": [],
            "message": ""
        }

        try:
            scrapper = ZonaPropScrapper(url, neighborhood=normalized_name)
            departments = scrapper.process_page()

            if not departments:
                health_report["message"] = "No departments returned. Search might be invalid or DOM changed."
                return health_report
            
            # Sample the first few departments
            sample = departments[:self.max_samples]
            health_report["scraped_items"] = len(sample)

            failures = {
                "title": 0,
                "price": 0,
                "url": 0,
                "location": 0,
                "area": 0
            }

            for dept in sample:
                if dept.title == "No title found" or not dept.title:
                    failures["title"] += 1
                if dept.price <= 0:
                    failures["price"] += 1
                if not dept.url:
                    failures["url"] += 1
                if not dept.location:
                    failures["location"] += 1
                # The details parsing might be broken if area == 0 across all samples
                if dept.details.area <= 0:
                    failures["area"] += 1

            failing_fields = []
            for field, failure_count in failures.items():
                if failure_count == len(sample):
                    # If the field failed for ALL samples, it's definitely broken
                    failing_fields.append(field)
            
            health_report["fields_failing"] = failing_fields

            if not failing_fields:
                health_report["status"] = "healthy"
                health_report["message"] = "All checked fields are being extracted correctly."
            else:
                health_report["status"] = "degraded"
                health_report["message"] = f"DOM Selectors failing for: {', '.join(failing_fields)}"

        except Exception as e:
            logger.error(f"Error during scrapper health check: {str(e)}")
            health_report["status"] = "broken"
            health_report["message"] = f"Exception occurred: {str(e)}"

        return health_report
