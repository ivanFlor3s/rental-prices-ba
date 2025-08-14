import os
from datetime import datetime
from pathlib import Path

from src.domain.entities.scrapping_result import ScrappingBatchResult


class ScrappingResultLogger:
    """Simple logger for scrapping results."""
    
    def __init__(self, log_dir: str = None):
        # Use environment variable if available, otherwise default
        if log_dir is None:
            log_dir = os.getenv("SCRAPPING_LOG_DIR", "logs/scrapping")
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def log_batch_result(self, batch_result: ScrappingBatchResult) -> str:
        """Log batch result to a new text file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"scrapping_result_{timestamp}.log"
        
        with open(log_file, 'w', encoding='utf-8') as file:
            file.write(f"{'='*80}\n")
            file.write(f"SCRAPPING EXECUTION - {batch_result.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"{'='*80}\n")
            
            # Summary info
            file.write(f"Duration: {batch_result.duration_seconds:.2f} seconds\n")
            file.write(f"Total neighborhoods: {batch_result.total_neighborhoods}\n")
            file.write(f"Successful: {len(batch_result.successful_results)}\n")
            file.write(f"Failed: {len(batch_result.failed_results)}\n")
            file.write(f"Success rate: {batch_result.success_rate:.1f}%\n")
            file.write(f"Total departments found: {batch_result.total_departments_scraped}\n\n")
            
            # Successful results
            if batch_result.successful_results:
                file.write("✅ SUCCESSFUL:\n")
                for result in batch_result.successful_results:
                    file.write(f"  - {result.neighborhood_name}\n")
                    file.write(f"    URL Scraped: {result.url}\n")
                    file.write(f"    {result.departments_count} departments\n")
                    # Add titles if available
                    if hasattr(result, 'titles') and result.titles:
                        file.write(f"    Departments: {', '.join(result.titles)}\n")
                file.write("\n")
            
            # Failed results
            if batch_result.failed_results:
                file.write("❌ FAILED:\n")
                for result in batch_result.failed_results:
                    file.write(f"  - {result.neighborhood_name}\n")
                    file.write(f"    URL: {result.url}\n")
                    file.write(f"    Error: {result.error_message}\n")
                file.write("\n")
            
            file.write(f"{'='*80}\n")
        
        return str(log_file)
    
    def cleanup_old_logs(self, days_to_keep: int = 30):
        """Remove log files older than specified days."""
        cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        for log_file in self.log_dir.glob("scrapping_result_*.log"):
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                print(f"Removed old log file: {log_file}")
    
    def get_latest_logs(self, limit: int = 10) -> list:
        """Get the latest log files."""
        log_files = list(self.log_dir.glob("scrapping_result_*.log"))
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return [str(f) for f in log_files[:limit]]
