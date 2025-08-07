
from src.infrastructure.logging.config import logger
from src.domain.scrappers.zonaprop_scrapper import ZonaPropScrapper
import sys

def run_api_server():
    """Función para ejecutar el servidor API"""
    import uvicorn
    from rental_api import app
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def main():
    """Función principal del script"""
    logger.info("Ejecutando script principal...")

    scrapper = ZonaPropScrapper("https://www.zonaprop.com.ar/departamentos-alquiler-capital-federal.html")
    departments = scrapper.process_page()
    for dept in departments:
        logger.info("department_info", dapartment=dept)
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_api_server()
    else:
        main()