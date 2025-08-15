
from src.application.orchestors.scrap_map_save import scrap_map_save
from src.infrastructure.logging.config import logger
from src.domain.scrappers.zonaprop_scrapper import ZonaPropScrapper
import sys

def run_api_server():
    """Función para ejecutar el servidor API"""
    import uvicorn
    from rental_api import app
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def main():
   scrap_map_save()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_api_server()
    else:
        main()