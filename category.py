from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from pydantic import BaseModel
from database import get_db
from models import Area, Category, User, Item
from sqlalchemy.orm import Session
from auth import get_current_user

router = APIRouter(tags=["categories"], prefix="/categories")

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]


# Schema for outputting category data
class CategoryOut(BaseModel):
    id: int
    name: str
    area_id: int

    class Config:
        from_attributes = True


# Schema for creating a category
class CategoryCreate(BaseModel):
    name: str
    area_id: int

    class Config:
        from_attributes = True


# Schema for updating a category
class CategoryUpdate(BaseModel):
    name: str

    class Config:
        from_attributes = True


# Schema for outputting item data
class ItemOut(BaseModel):
    id: int
    name: str
    quantity: int
    category_id: int
    user_id: int

    class Config:
        from_attributes = True


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/", response_model=list[CategoryOut])
async def get_categories(db: db_dependency):
    categories = db.query(Category).all()
    return categories
