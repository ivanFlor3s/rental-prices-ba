import logging


def run_api_server():
    """Función para ejecutar el servidor API"""
    import uvicorn
    from rental_api import app
    
    logger.info("Iniciando servidor API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
# Verificar si se quiere ejecutar en modo especial
if len(sys.argv) > 1 and sys.argv[1] == "api":
    run_api_server()
elif len(sys.argv) > 1 and sys.argv[1] == "scheduler":
    run_scheduler()
else:
    main()