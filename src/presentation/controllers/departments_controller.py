from fastapi import APIRouter, Depends, status
from src.infrastructure.db.session import get_session
from typing import Annotated
from sqlalchemy.orm import Session
from src.domain import Department

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/", status_code=status.HTTP_200_OK)
async def get_departments():
    return {"message": "List of departments"}
