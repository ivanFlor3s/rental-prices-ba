from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta

# Inicializar FastAPI
app = FastAPI(
    title="Buenos Aires Rental Prices API",
    description="API para consultar precios de alquileres en Buenos Aires",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class APIStats(BaseModel):
    total_properties: int
    active_properties: int
    total_neighborhoods: int
    last_update: datetime
    properties_by_source: Dict[str, int]

# Endpoints

@app.get("/", tags=["Info"])
async def root():
    """Información básica de la API"""
    return {
        "message": "Buenos Aires Rental Prices API",
        "version": "1.0.0",
        "endpoints": {
            "properties": "/properties",
            "neighborhoods": "/neighborhoods",
            "stats": "/stats",
            "history": "/neighborhoods/{neighborhood}/history"
        }
    }

@app.get("/stats", response_model=APIStats, tags=["Stats"])
async def get_api_stats():
    """Estadísticas generales de la API"""
    
    total_properties = 12
    active_properties = 12
    
    total_neighborhoods = 133

    last_update = datetime.now(datetime.now().tzinfo)

    # Properties by source
    source_counts = []
    
    properties_by_source = {source: count for source, count in source_counts}
    
    return APIStats(
        total_properties=total_properties,
        active_properties=active_properties,
        total_neighborhoods=total_neighborhoods,
        last_update=last_update,
        properties_by_source=properties_by_source
    )

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Endpoint para desarrolladores - documentación de uso
@app.get("/docs-examples", tags=["Documentation"])
async def api_examples():
    """Ejemplos de uso de la API"""
    return {
        "examples": {
            "get_properties": {
                "url": "/properties?neighborhood=Palermo&min_price_usd=500&max_price_usd=1000&limit=10",
                "description": "Obtener propiedades en Palermo entre USD 500 y 1000"
            },
            "neighborhood_stats": {
                "url": "/neighborhoods?days_back=30&property_type=departamento",
                "description": "Estadísticas de departamentos en los últimos 30 días"
            },
            "price_history": {
                "url": "/neighborhoods/Palermo/history?days_back=90",
                "description": "Historial de precios de Palermo en los últimos 90 días"
            }
        },
        "filters": {
            "neighborhood": "Nombre del barrio (búsqueda parcial)",
            "min_price_usd": "Precio mínimo en dólares",
            "max_price_usd": "Precio máximo en dólares",
            "min_rooms": "Cantidad mínima de ambientes",
            "property_type": "Tipo de propiedad (departamento, casa, ph)",
            "has_garage": "true/false para cochera",
            "days_back": "Días hacia atrás para estadísticas",
            "limit": "Cantidad máxima de resultados (máx 1000)",
            "offset": "Para paginación"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)