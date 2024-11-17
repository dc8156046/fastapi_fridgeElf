from collections import defaultdict
from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from pydantic import BaseModel
from database import get_db
from models import Area, Category, Item, User
from sqlalchemy.orm import Session
from category import CategoryOut
from item import ItemOut, CategoryWithItemsOut
from auth import get_current_user

router = APIRouter(tags=["areas"], prefix="/areas")


# Schema for outputting area data
class AreaOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]


# Get all areas
@router.get("/", response_model=list[AreaOut])
async def get_areas(db: Session = Depends(db_dependency)):
    areas = db.query(Area).all()
    return areas


# Get categories by area
@router.get("/{area_id}/categories", response_model=list[CategoryOut])
async def get_categories_by_area(area_id: int, db: Session = Depends(db_dependency)):
    categories = db.query(Category).filter(Category.area_id == area_id).all()
    return categories


@router.get("/{area_id}/items", response_model=list[CategoryWithItemsOut])
async def get_items_by_area(
    area_id: int,
    db: Session = Depends(db_dependency),
    user: User = Depends(user_dependency),
):

    # Query items and their categories
    items = (
        db.query(Item, Category)
        .join(Category, Item.category_id == Category.id)
        .filter(Category.area_id == area_id, Item.user_id == user.id)
        .all()
    )

    # Group items by category
    categories_dict = defaultdict(lambda: {"id": None, "name": None, "items": []})

    for item, category in items:
        if categories_dict[category.id]["id"] is None:
            categories_dict[category.id]["id"] = category.id
            categories_dict[category.id]["name"] = category.name

        categories_dict[category.id]["items"].append(
            ItemOut(
                id=item.id,
                name=item.name,
                quantity=item.quantity,
                expire_date=item.expire_date,
            )
        )

    # Convert dictionary to list of CategoryWithItemsOut
    categories = [
        CategoryWithItemsOut(
            id=category_data["id"],
            name=category_data["name"],
            items=category_data["items"],
        )
        for category_data in categories_dict.values()
    ]

    return categories
