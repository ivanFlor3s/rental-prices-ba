import os
from datetime import datetime
from pathlib import Path

from src.domain.entities.scrapping_result import ScrappingBatchResult


class ScrappingResultLogger:
    """Simple logger for scrapping results."""
    
    def __init__(self, log_file: str = "logs/scrapping_results.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_batch_result(self, batch_result: ScrappingBatchResult):
        """Log batch result to a simple text file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_file, 'a', encoding='utf-8') as file:
            file.write(f"\n{'='*80}\n")
            file.write(f"SCRAPPING EXECUTION - {timestamp}\n")
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
                    file.write(f"    Url Scrapped: {result.url}\n")
                    if(result.error_message is not None):
                        file.write(f"    Error: {result.error_message}\n")
                    else:
                        file.write(f"    {result.departments_count} departments\n")
                        file.write(f"    Departments ({result.departments_count}): {', '.join(result.titles)}\n")

                file.write("\n")
            
            # Failed results
            if batch_result.failed_results:
                file.write("❌ FAILED:\n")
                for result in batch_result.failed_results:
                    file.write(f"  • {result.neighborhood_name}: {result.error_message}\n")
                file.write("\n")
            
            file.write(f"{'='*80}\n\n")
    
    def cleanup_old_logs(self, max_lines: int = 10000):
        """Keep only the last N lines of the log file."""
        if not self.log_file.exists():
            return
            
        with open(self.log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if len(lines) > max_lines:
            # Keep only the last max_lines
            with open(self.log_file, 'w', encoding='utf-8') as file:
                file.writelines(lines[-max_lines:])
            print(f"Trimmed log file to last {max_lines} lines")
