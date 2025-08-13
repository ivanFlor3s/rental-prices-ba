from sqlalchemy import ForeignKey, Column, Integer, String, Text, DECIMAL, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timezone 
from .session import Base


class DepartmentModel(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
   
    source = Column(String(50), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    title = Column(Text)
    
    # Ubicación
    neighborhood_id = Column(Integer, ForeignKey('neighborhoods.id'))
    neighborhood = relationship("NeighborhoodModel", backref="departments")

    # Características básicas
    property_type = Column(String(50))
    rooms = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    surface_total = Column(Integer)
    garages = Column(Integer, default=0)  # Si no tienes este campo, puedes eliminarlo
    
    # Precios
    price = Column(DECIMAL(20, 2))
    currency_price = Column(String(3), default='ARS')
    expenses = Column(DECIMAL(20, 2))
    currency_expenses = Column(String(3), default='ARS')

    # Metadatos
    is_active = Column(Boolean, default=True)
    scraped_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    # Constraints
    __table_args__ = (
        CheckConstraint("rooms >= 0"),
        CheckConstraint("bedrooms >= 0"),
        CheckConstraint("bathrooms >= 0"),
        CheckConstraint("surface_total >= 0"),
        CheckConstraint("price >= 0"),
        CheckConstraint("expenses >= 0"),
        CheckConstraint("currency_price IN ('ARS', 'USD')"),
        CheckConstraint("currency_expenses IN ('ARS', 'USD')"),
        CheckConstraint("source IN ('argenprop', 'zonaprop', 'mercadolibre', 'cabaprop')"),
        CheckConstraint("property_type IN ('department', 'house', 'duplex', 'ph')"),
    )


class NeighborhoodModel(Base):
    __tablename__ = 'neighborhoods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)