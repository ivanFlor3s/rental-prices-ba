
import logging
import sys
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False
)

logger = structlog.get_logger()


def run_api_server():
    """Función para ejecutar el servidor API"""
    import uvicorn
    from rental_api import app
    
    logger.info("Iniciando servidor API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def main():
    """Función principal del script"""
    logger.info("Ejecutando script principal...")
    # Aquí puedes agregar la lógica principal de tu aplicación
    # Por ejemplo, cargar datos, procesar información, etc.
    pass

if __name__ == "__main__":
# Verificar si se quiere ejecutar en modo especial
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_api_server()
    else:
        main()