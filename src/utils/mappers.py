from datetime import datetime, timezone
from domain.entities.dapartment import Department, DeptDetails
from infrastructure.db.models import DepartmentModel


def map_department_to_model(dept: Department, source: str, neighborhood_id: int) -> DepartmentModel:
    return DepartmentModel(
        source=source,
        url=dept.url,
        title=dept.title,
        neighborhood_id=neighborhood_id,
        property_type="Departamento",  # o algo derivado de la data si lo tienes
        rooms=dept.details.ambientes if dept.details else None,
        bedrooms=dept.details.bedrooms if dept.details else None,
        bathrooms=dept.details.bathrooms if dept.details else None,
        surface_total=dept.details.area if dept.details else None,
        garages=dept.details.garages if dept.details else 0,  # Asignar 0 si no hay información
        price=dept.price,
        currency_price="USD" if dept.is_usd else "ARS",
        expenses=dept.expenses,
        currency_expenses="ARS",  # podrías hacer lógica si algún día tienes gastos en USD
        is_active=True,
        scraped_at=datetime.now(timezone.utc)
    )


def model_to_department(model: DepartmentModel) -> Department:
    details = None
    if any([model.rooms, model.bedrooms, model.bathrooms, model.surface_total, model.property_type]):
        details = DeptDetails(
            ambientes=model.rooms or 0,
            bedrooms=model.bedrooms or 0,
            bathrooms=model.bathrooms or 0,
            area=model.surface_total or 0,
            garages= model.garages or 0
        )

    return Department(
        title=model.title,
        url=model.url,
        price=float(model.price) if model.price is not None else 0,
        is_usd=(model.currency_price == 'USD'),
        location=model.neighborhood.name if model.neighborhood else "",
        expenses=float(model.expenses) if model.expenses is not None else None,
        details=details
    )