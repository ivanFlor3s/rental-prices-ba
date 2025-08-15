# Buenos Aires Rental Prices - Scrapping System

Sistema completo de scrapping y análisis de precios de alquileres en Buenos Aires con arquitectura limpia y logging avanzado.

## 🚀 Características

-   **Web Scraping**: Extracción automática desde ZonaProp con rate limiting inteligente
-   **Arquitectura Limpia**: Separación de responsabilidades con Domain-Driven Design
-   **Base de datos**: PostgreSQL con Alembic para migraciones
-   **API REST**: FastAPI con endpoints para consultar datos
-   **Logging Avanzado**: Sistema de logs detallado con múltiples formatos
-   **Control de Concurrencia**: Semáforos y delays para evitar bloqueos IP
-   **Gestión de Barrios**: Sistema completo de neighborhoods con normalización

## 🛠 Instalación

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
# Crear base de datos
createdb rentals_db

# O usando psql
psql -c "CREATE DATABASE rentals_db;"
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 4. Ejecutar migraciones

```bash
# Ejecutar migraciones para crear tablas y seed de barrios
alembic upgrade head
```

## 🚀 Uso

### 1. Sistema de Scrapping

```python
from src.application.orchestors.scrap_map_save import ScrappingOrchestrator

# Inicializar el orquestador
orchestrator = ScrappingOrchestrator(min_delay=2.0, max_delay=4.0)

# Scrapear todos los barrios
result = orchestrator.scrap_all_neighborhoods()

# Scrapear barrios específicos
result = orchestrator.scrap_specific_neighborhoods(["Palermo", "Recoleta"])

# Ver resumen
print(result.get_summary())
```

### 2. Funciones de compatibilidad

```python
# Usando las funciones originales (backward compatibility)
from src.application.orchestors.scrap_map_save import scrap_map_save

result = scrap_map_save()
```

### 3. Ejecutar API

```bash
# Servidor de desarrollo
python main.py

# O directamente con uvicorn
uvicorn rental_api:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 API Endpoints

### Endpoints principales:

-   **GET `/`** - Información general de la API
-   **GET `/health`** - Estado de la aplicación
-   **GET `/api/departments`** - Listar departamentos con filtros
-   **GET `/api/departments/{id}`** - Obtener departamento específico
-   **GET `/api/neighborhoods`** - Listar barrios disponibles

```

### Documentación interactiva:

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`

## 🔧 Sistema de Logging

### Logs de Scrapping

El sistema genera logs detallados de cada ejecución de scrapping:

```

logs/
└── scrapping/
├── scrapping_result_20250815_143022.log
├── scrapping_result_20250815_150145.log
└── scrapping_result_20250815_152330.log

````

Cada archivo contiene:

-   Resumen de ejecución (duración, éxito/fallo)
-   Detalles por barrio
-   URLs utilizadas
-   Errores específicos

### Configuración de Logs

```python
# Variables de entorno
SCRAPPING_LOG_DIR=logs/scrapping  # Directorio de logs
LOG_LEVEL=INFO                    # Nivel de logging
````

### Mantenimiento de Logs

```python
from src.application.orchestors.scrap_map_save import ScrappingOrchestrator

orchestrator = ScrappingOrchestrator()

# Limpiar logs antiguos
orchestrator.cleanup_old_logs(days_to_keep=30)

# Obtener logs recientes
recent_logs = orchestrator.get_recent_logs(limit=5)
```

python main.py --skip-scraping

# Exportar datos a CSV

python main.py --export-csv

````

### 3. Ejecutar API

```bash
# Servidor de desarrollo
python main.py api

# O directamente
uvicorn rental_api:app --host 0.0.0.0 --port 8000 --reload
````

### Documentación interactiva:

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`

## 🏗️ Arquitectura y Componentes

### Capa de Dominio

-   **Entities**: `Department`, `Neighborhood`, `ScrappingResult`
-   **Enums**: `Currency`, `PropertyType`, `Provider`
-   **Scrappers**: `ZonaPropScrapper` con URL builder

### Capa de Aplicación

-   **Orquestadores**: `ScrappingOrchestrator` - Control principal del scrapping
-   **Casos de Uso**: `DepartmentUseCases` - Lógica de negocio

### Capa de Infraestructura

-   **Base de Datos**: SQLAlchemy con Alembic
-   **Repositorios**: `DepartmentRepository`, `NeighborhoodRepository`
-   **Logging**: Sistema especializado de logs
-   **Jobs**: Servicios en background

### Capa de Presentación

-   **API Controllers**: FastAPI endpoints
-   **Health Checks**: Monitoreo de estado

## 🎯 Enumeraciones Centralizadas

```python
from src.domain.enum import Currency, PropertyType, Provider

# Uso simple en una línea
currency = Currency.USD
property_type = PropertyType.DEPARTMENT
provider = Provider.ZONAPROP
```

## 🗃️ Migraciones con Alembic

### Comandos útiles:

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

### Barrios Incluidos:

El sistema viene con 48 barrios de Buenos Aires pre-cargados:

-   Palermo, Recoleta, Puerto Madero, Villa Crespo
-   Belgrano, Caballito, San Telmo, La Boca
-   Y todos los demás barrios porteños

## 📈 Monitoreo y Análisis

### Logs de Sistema

Los logs del sistema se guardan en diferentes niveles:

```bash
# Ver logs de scrapping en tiempo real
tail -f logs/scrapping/scrapping_result_*.log

# Buscar errores específicos
grep "❌ FAILED" logs/scrapping/*.log

# Analizar tasas de éxito
grep "Success rate" logs/scrapping/*.log
```

### Métricas de Scrapping

Cada ejecución genera métricas detalladas:

-   Duración total del proceso
-   Tasa de éxito por barrio
-   Cantidad de departamentos encontrados
-   Errores específicos por URL

### Análisis de Resultados

```python
from src.application.orchestors.scrap_map_save import ScrappingOrchestrator

orchestrator = ScrappingOrchestrator()

# Ver logs recientes
recent_logs = orchestrator.get_recent_logs(5)

# Análisis manual de archivos
for log_file in recent_logs:
    print(f"Log file: {log_file}")
```

## 📋 Datos que se Recolectan

### Por Departamento:

-   **Básicos**: Título, descripción, URL de origen
-   **Ubicación**: Barrio (normalizado)
-   **Características**: Ambientes, baños, m², tipo de propiedad
-   **Precios**: ARS, USD, expensas
-   **Amenities**: Garage, balcón, amenities varios
-   **Fechas**: Creación, última actualización

### Resultados de Scrapping:

```python
# NeighborhoodScrappingResult
- neighborhood_id, neighborhood_name, url
- success, departments_count, titles[]
- error_message, timestamp

# ScrappingBatchResult
- successful_results[], failed_results[]
- total_neighborhoods, total_departments_scraped
- start_time, end_time, success_rate, duration
```

## 🔄 Proceso de Scrapping

### Flujo Principal:

1. **Inicialización**: `ScrappingOrchestrator` con rate limiting configurado
2. **Obtención de Barrios**: Query a la DB para obtener neighborhoods
3. **Normalización**: Conversión de nombres de barrios para URLs
4. **Scrapping**: `ZonaPropScrapper` procesa cada barrio
5. **Persistencia**: Guardado en DB con deduplicación
6. **Logging**: Generación de logs detallados por ejecución
7. **Rate Limiting**: Delays aleatorios entre 1.5-4.0 segundos

### Arquitectura Resiliente:

-   ✅ Rollback automático en caso de error
-   ✅ Logs detallados por barrio
-   ✅ Continuación del proceso aunque falle un barrio
-   ✅ Gestión de sesiones de DB por barrio

## 🎯 Roadmap

### Funcionalidades Completadas: ✅

-   [x] Arquitectura limpia con DDD
-   [x] Scrapper para ZonaProp
-   [x] Sistema de logging avanzado
-   [x] Migraciones con Alembic
-   [x] Rate limiting inteligente
-   [x] Gestión de barrios completa
-   [x] API REST con FastAPI
-   [x] Enumeraciones centralizadas
-   [x] Manejo robusto de errores

### Próximas funcionalidades: 🚧

-   [ ] Sistema asíncrono con semáforos (en progreso)
-   [ ] Scraper para MercadoLibre
-   [ ] Scraper para ArgentProp
-   [ ] Dashboard web con gráficos
-   [ ] Geocoding automático (lat/lng)
-   [ ] Predicciones de precios (ML básico)
-   [ ] Alertas por email/webhook
-   [ ] Cache con Redis
-   [ ] Rate limiting en API

### Mejoras técnicas: 🔧

-   [ ] Tests unitarios completos
-   [ ] CI/CD pipeline
-   [ ] Monitoreo con Prometheus
-   [ ] Proxy rotation para scrapping
-   [ ] Kubernetes deployment
-   [ ] Métricas de performance

## 🤝 Contribuir

1. Fork del proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push to branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

MIT License - ver archivo `LICENSE` para detalles.

## ⚠️ Consideraciones Legales

-   Respetar `robots.txt` de los sitios web
-   No sobrecargar servidores (usar delays apropiados)
-   Uso solo para fines educativos y de investigación
-   Verificar términos de servicio de cada sitio
