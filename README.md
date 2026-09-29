# Buenos Aires Rental Prices - Scrapping System

Sistema dedicado al **scrapping** y **persistencia** de precios de alquileres en Buenos Aires, con arquitectura limpia y logging avanzado.

## Características

-   **Web Scraping**: Extracción automática desde ZonaProp con rate limiting inteligente
-   **Persistencia**: PostgreSQL con SQLAlchemy y Alembic para migraciones
-   **CLI**: Scraping total o por barrios, y exportación a CSV
-   **Logging Avanzado**: Sistema de logs detallado con múltiples formatos
-   **Control de Concurrencia**: Delays aleatorios para evitar bloqueos IP
-   **Gestión de Barrios**: Sistema completo de neighborhoods con normalización

## Instalación

### 1. Clonar y configurar entorno

```bash
git clone <tu-repo>
cd rental-prices-ba

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar base de datos PostgreSQL

#### Opción A: Docker (recomendado)

```bash
docker-compose up -d
```

#### Opción B: PostgreSQL local

```bash
createdb rentals_db
# o usando psql
psql -c "CREATE DATABASE rentals_db;"
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 4. Ejecutar migraciones

```bash
alembic upgrade head
```

## Uso

### CLI

```bash
# Scrapear todos los barrios
python main.py

# Scrapear barrios específicos
python main.py Palermo Recoleta

# Exportar departamentos persistidos a CSV
python main.py --export-csv departamentos.csv

# Chequear la salud de los selectores DOM del scrapper
python main.py --health
```

### Uso programático

```python
from src.application.orchestors.scrap_map_save import ScrappingOrchestrator

orchestrator = ScrappingOrchestrator(min_delay=2.0, max_delay=4.0)

# Scrapear todos los barrios
result = orchestrator.scrap_all_neighborhoods()

# Scrapear barrios específicos
result = orchestrator.scrap_specific_neighborhoods(["Palermo", "Recoleta"])

# Ver resumen
print(result.get_summary())
```

## Sistema de Logging

Los resultados de cada ejecución se guardan en `logs/scrapping/`:

```
logs/
└── scrapping/
    ├── scrapping_result_20250815_143022.log
    └── scrapping_result_20250815_150145.log
```

Cada archivo contiene resumen de ejecución, detalles por barrio, URLs utilizadas y errores específicos.

### Configuración

```python
SCRAPPING_LOG_DIR=logs/scrapping  # Directorio de logs
LOG_LEVEL=INFO                    # Nivel de logging
```

### Mantenimiento

```python
from src.infrastructure.logging.scrapping_logger import ScrappingResultLogger

result_logger = ScrappingResultLogger()
result_logger.cleanup_old_logs(days_to_keep=30)
recent_logs = result_logger.get_latest_logs(limit=5)
```

## Arquitectura y Componentes

### Capa de Dominio

-   **Entities**: `Department`, `Neighborhood`, `ScrappingResult`
-   **Enums**: `Currency`, `PropertyType`, `Provider`
-   **Scrappers**: `ZonaPropScrapper` con URL builder

### Capa de Aplicación

-   **Orquestadores**: `ScrappingOrchestrator` - Control principal del scrapping
-   **Casos de Uso**: `DepartmentUseCases` - Persistencia de departamentos

### Capa de Infraestructura

-   **Base de Datos**: SQLAlchemy con Alembic
-   **Repositorios**: `NeighborhoodRepository`
-   **Logging**: Sistema especializado de logs

## Migraciones con Alembic

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripcion_del_cambio"

# Aplicar migraciones
alembic upgrade head

# Ver historial
alembic history

# Rollback
alembic downgrade -1
```

El sistema viene con 48 barrios de Buenos Aires pre-cargados (Palermo, Recoleta, Puerto Madero, Belgrano, Caballito, San Telmo, La Boca, etc.).

## Datos que se Recolectan

### Por Departamento

-   **Básicos**: Título, URL de origen
-   **Ubicación**: Barrio (normalizado)
-   **Características**: Ambientes, dormitorios, baños, m², cocheras
-   **Precios**: ARS, USD, expensas
-   **Fechas**: Creación, última actualización

### Resultados de Scrapping

```python
# NeighborhoodScrappingResult
# - neighborhood_id, neighborhood_name, url
# - success, departments_count, titles[]
# - error_message, timestamp

# ScrappingBatchResult
# - successful_results[], failed_results[]
# - total_neighborhoods, total_departments_scraped
# - start_time, end_time, success_rate, duration
```

## Proceso de Scrapping

1. **Inicialización**: `ScrappingOrchestrator` con rate limiting configurado
2. **Obtención de Barrios**: Query a la DB para obtener neighborhoods
3. **Normalización**: Conversión de nombres de barrios para URLs
4. **Scrapping**: `ZonaPropScrapper` procesa cada barrio
5. **Persistencia**: Guardado en DB con deduplicación por URL
6. **Logging**: Generación de logs detallados por ejecución
7. **Rate Limiting**: Delays aleatorios entre 1.5-4.0 segundos

### Arquitectura Resiliente

-   Rollback automático en caso de error
-   Logs detallados por barrio
-   Continuación del proceso aunque falle un barrio
-   Gestión de sesiones de DB por barrio

## Roadmap

### Funcionalidades Completadas

-   [x] Arquitectura limpia con DDD
-   [x] Scrapper para ZonaProp
-   [x] Sistema de logging avanzado
-   [x] Migraciones con Alembic
-   [x] Rate limiting inteligente
-   [x] Gestión de barrios completa
-   [x] Exportación a CSV

### Próximas funcionalidades

-   [ ] Sistema asíncrono con semáforos
-   [ ] Scraper para MercadoLibre
-   [ ] Scraper para ArgentProp
-   [ ] Geocoding automático (lat/lng)
-   [ ] Predicciones de precios (ML básico)
-   [ ] Proxy rotation para scrapping

## Licencia

MIT License - ver archivo `LICENSE` para detalles.

## Consideraciones Legales

-   Respetar `robots.txt` de los sitios web
-   No sobrecargar servidores (usar delays apropiados)
-   Uso solo para fines educativos y de investigación
-   Verificar términos de servicio de cada sitio
