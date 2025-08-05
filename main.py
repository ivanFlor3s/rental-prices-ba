
from src.infrastructure.logging.config import logger
import sys

def run_api_server():
    """Función para ejecutar el servidor API"""
    import uvicorn
    from rental_api import app
    uvicorn.run(app, host="localhost", port=8000, log_level="info")

def main():
    """Función principal del script"""
    logger.info("Ejecutando script principal...")
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_api_server()
    else:
        main()