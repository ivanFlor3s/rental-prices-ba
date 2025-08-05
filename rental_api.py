from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.controllers import departments, health



app = FastAPI(
    title="Buenos Aires Rental Prices API",
    description="API para consultar precios de alquileres en Buenos Aires",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(departments.router)
app.include_router(health.router)
