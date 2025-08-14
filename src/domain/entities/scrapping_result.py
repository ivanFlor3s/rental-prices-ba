from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class NeighborhoodScrappingResult:
    """Represents the result of scrapping a specific neighborhood."""
    neighborhood_id: int
    neighborhood_name: str
    url: str
    titles: List[str]
    success: bool
    departments_count: int = 0
    error_message: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass 
class ScrappingBatchResult:
    """Represents the result of scrapping multiple neighborhoods."""
    successful_results: List[NeighborhoodScrappingResult]
    failed_results: List[NeighborhoodScrappingResult]
    total_neighborhoods: int
    total_departments_scraped: int
    start_time: datetime
    end_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.end_time is None:
            self.end_time = datetime.now()
    
    @property
    def success_rate(self) -> float:
        """Calculate the success rate as a percentage."""
        if self.total_neighborhoods == 0:
            return 0.0
        return (len(self.successful_results) / self.total_neighborhoods) * 100
    
    @property
    def duration_seconds(self) -> float:
        """Calculate the duration in seconds."""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def add_successful_result(self, result: NeighborhoodScrappingResult):
        """Add a successful scrapping result."""
        result.success = True
        self.successful_results.append(result)
        self.total_departments_scraped += result.departments_count
    
    def add_failed_result(self, result: NeighborhoodScrappingResult):
        """Add a failed scrapping result."""
        result.success = False
        self.failed_results.append(result)
    
    def get_summary(self) -> str:
        """Get a summary of the scrapping batch result."""
        return (
            f"Scrapping Summary:\n"
            f"- Total neighborhoods: {self.total_neighborhoods}\n"
            f"- Successful: {len(self.successful_results)}\n"
            f"- Failed: {len(self.failed_results)}\n"
            f"- Success rate: {self.success_rate:.1f}%\n"
            f"- Total departments scraped: {self.total_departments_scraped}\n"
            f"- Duration: {self.duration_seconds:.2f} seconds"
        )
