from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from pydantic import BaseModel
from database import get_db
from models import Area, Category
from sqlalchemy.orm import Session
from category import CategoryOut

router = APIRouter(tags=["areas"], prefix="/areas")


# Schema for outputting area data
class AreaOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


db_dependency = Annotated[Session, Depends(get_db)]


# Get all areas
@router.get("/", response_model=list[AreaOut])
async def get_areas(db: db_dependency):
    areas = db.query(Area).all()
    return areas


# Get categories by area
@router.get("/{area_id}/categories", response_model=list[CategoryOut])
async def get_categories_by_area(area_id: int, db: db_dependency):
    categories = db.query(Category).filter(Category.area_id == area_id).all()
    return categories
