# Buenos Aires Rental Prices - ETL Project

Sistema completo de extracción, transformación y exposición de datos de alquileres en Buenos Aires.

## 🚀 Características

-   **Web Scraping**: Extracción automática desde Argenprop (extensible a otras fuentes)
-   **Base de datos**: PostgreSQL con historial de precios y métricas agregadas
-   **API REST**: FastAPI con endpoints para consultar datos
-   **ETL Pipeline**: Procesamiento automático de datos
-   **Análisis**: Estadísticas por barrio, tendencias históricas
-   **Scheduler**: Ejecución automática diaria

## 📁 Estructura del Proyecto

```
rental-prices-ba/
├── main.py                 # Script principal orquestador
├── argenprop_scraper.py   # Scraper para Argenprop
├── database_models.py     # Modelos SQLAlchemy y gestión DB
├── rental_api.py          # API FastAPI
├── requirements.txt       # Dependencias Python
├── .env.example          # Variables de entorno ejemplo
├── docker-compose.yml    # Docker setup (opcional)
└── README.md             # Este archivo
```

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
docker-compose up -d postgres
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

Archivo `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/rentals_db
SCRAPING_DELAY=2.0
MAX_PAGES_DEFAULT=5
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

## 🚀 Uso

### 1. Configuración inicial

```bash
# Crear tablas en la base de datos
python main.py --setup-db
```

### 2. Ejecutar scraping y procesamiento

```bash
# Ejecución completa (recomendado para primera vez)
python main.py --max-pages 10

# Solo scraping de Argenprop
python main.py --sources argenprop --max-pages 5

# Procesar datos existentes sin scraping
python main.py --skip-scraping

# Exportar datos a CSV
python main.py --export-csv
```

### 3. Ejecutar API

```bash
# Servidor de desarrollo
python main.py api

# O directamente
uvicorn rental_api:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Scheduler automático

```bash
# Ejecutar diariamente (job en background)
python main.py scheduler
```

## 📊 API Endpoints

### Endpoints principales:

-   **GET `/`** - Información general de la API
-   **GET `/stats`** - Estadísticas generales del sistema
-   **GET `/properties`** - Listar propiedades con filtros
-   **GET `/neighborhoods`** - Estadísticas por barrio
-   **GET `/neighborhoods/{barrio}/history`** - Historial de precios
-   **GET `/neighborhoods/list`** - Lista de barrios disponibles

### Ejemplos de uso:

```bash
# Estadísticas generales
curl http://localhost:8000/stats

# Propiedades en Palermo
curl "http://localhost:8000/properties?neighborhood=Palermo&limit=10"

# Estadísticas por barrio (últimos 30 días)
curl "http://localhost:8000/neighborhoods?days_back=30"

# Historial de precios de Recoleta
curl "http://localhost:8000/neighborhoods/Recoleta/history?days_back=90"

# Filtros avanzados
curl "http://localhost:8000/properties?min_price_usd=500&max_price_usd=1500&min_rooms=2&has_garage=true"
```

### Documentación interactiva:

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`

## 🔧 Configuración Avanzada

### Parámetros del scraper:

```python
# En argenprop_scraper.py
scraper = ArgenpropScraper(
    delay_between_requests=2.0,  # Delay entre requests
    max_retries=3,               # Reintentos en caso de error
    timeout=10                   # Timeout de requests
)
```

### Configuración de base de datos:

```python
# En database_models.py
db_manager = DatabaseManager(
    database_url="postgresql://user:pass@host:port/db"
)
```

## 📈 Monitoreo y Logs

Los logs se guardan en `rental_scraper.log` y incluyen:

-   Progreso del scraping
-   Errores y warnings
-   Estadísticas de ejecución
-   Performance metrics

```bash
# Ver logs en tiempo real
tail -f rental_scraper.log

# Buscar errores
grep ERROR rental_scraper.log
```

## 🐳 Docker (Opcional)

```yaml
# docker-compose.yml incluido
version: '3.8'
services:
    postgres:
        image: postgres:13
        environment:
            POSTGRES_DB: rentals_db
            POSTGRES_USER: rental_user
            POSTGRES_PASSWORD: rental_pass
        ports:
            - '5432:5432'
        volumes:
            - postgres_data:/var/lib/postgresql/data

    api:
        build: .
        ports:
            - '8000:8000'
        depends_on:
            - postgres
        environment:
            DATABASE_URL: postgresql://rental_user:rental_pass@postgres:5432/rentals_db

volumes:
    postgres_data:
```

```bash
# Levantar todo con Docker
docker-compose up -d

# Solo base de datos
docker-compose up -d postgres
```

## 📋 Datos que se recolectan

### Por propiedad:

-   **Básicos**: Título, descripción, URL, fecha
-   **Ubicación**: Barrio, dirección
-   **Características**: Ambientes, baños, m², tipo
-   **Precios**: ARS, USD, expensas
-   **Amenities**: Cochera, balcón, pileta, gym, etc.

### Métricas agregadas:

-   Precios promedio/mediano por barrio
-   Precio por m² por zona
-   Cantidad de propiedades activas
-   Tendencias históricas
-   Propiedades nuevas por día

## 🔄 Proceso ETL

1. **Extract**: Web scraping desde sitios inmobiliarios
2. **Transform**: Limpieza y normalización de datos
3. **Load**: Guardado en PostgreSQL con deduplicación
4. **Metrics**: Cálculo de estadísticas agregadas

## 🎯 Roadmap

### Próximas funcionalidades:

-   [ ] Scraper para Zonaprop
-   [ ] Scraper para MercadoLibre
-   [ ] Geocoding automático (lat/lng)
-   [ ] Dashboard web con gráficos
-   [ ] Predicciones de precios (ML básico)
-   [ ] Alertas por email/webhook
-   [ ] Cache con Redis
-   [ ] Rate limiting en API

### Mejoras técnicas:

-   [ ] Tests unitarios
-   [ ] CI/CD pipeline
-   [ ] Monitoreo con Prometheus
-   [ ] Retry logic más robusto
-   [ ] Proxy rotation para scraping

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

## 🆘 Troubleshooting

### Problemas comunes:

**Error de conexión a DB:**

```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Verificar conexión
psql -h localhost -U tu_usuario -d rentals_db
```

**Scraper bloqueado:**

```bash
# Aumentar delay entre requests
python main.py --sources argenprop --max-pages 2
# Y ajustar delay_between_requests en el código
```

**API no responde:**

```bash
# Verificar que el puerto esté libre
lsof -i :8000

# Reiniciar API
pkill -f rental_api
python main.py api
```

## 📞 Soporte

Para reportar bugs o solicitar funcionalidades, crear un issue en GitHub.

---

**Happy coding! 🚀**
