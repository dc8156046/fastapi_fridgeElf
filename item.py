from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from pydantic import BaseModel
from database import get_db
from models import Area, Category, User, Item
from sqlalchemy.orm import Session
from auth import get_current_user
from datetime import datetime

router = APIRouter(tags=["items"], prefix="/items")

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]


# Schema for outputting item data
class ItemOut(BaseModel):
    id: int
    name: str
    quantity: int
    expire_date: datetime

    class Config:
        from_attributes = True


# Schema for outputting category data with items
class CategoryWithItemsOut(BaseModel):
    id: int
    name: str
    items: list[ItemOut]

    class Config:
        from_attributes = True


# Schema for creating an item
class ItemCreate(BaseModel):
    name: str
    quantity: int
    expire_date: datetime
    category_id: int

    class Config:
        from_attributes = True


# Schema for updating an item
class ItemUpdate(BaseModel):
    name: str
    quantity: int

    class Config:
        from_attributes = True


@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: int, db: db_dependency, user: user_dependency):
    item = db.query(Item).filter(Item.id == item_id, Item.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/", response_model=list[CategoryWithItemsOut])
async def get_items(db: db_dependency, user: user_dependency):
    # get all categories that belong to the user
    categories = (
        db.query(Category)
        .join(Item, Category.id == Item.category_id)
        .filter(Item.user_id == user["id"])
        .all()
    )

    # create a list of categories with items
    result = []
    for category in categories:
        category_items = [
            ItemOut(
                id=item.id,
                name=item.name,
                quantity=item.quantity,
                expire_date=item.expire_date,
            )
            for item in category.items
        ]
        result.append(
            CategoryWithItemsOut(
                id=category.id,
                name=category.name,
                items=category_items,
            )
        )

    return result


@router.post("/", response_model=ItemOut)
async def create_item(request: ItemCreate, db: db_dependency, user: user_dependency):
    item = Item(**request.dict(), user_id=user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ItemOut)
async def update_item(
    item_id: int, request: ItemUpdate, db: db_dependency, user: user_dependency
):
    item = db.query(Item).filter(Item.id == item_id, Item.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = request.name
    item.quantity = request.quantity
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, db: db_dependency, user: user_dependency):
    item = db.query(Item).filter(Item.id == item_id, Item.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
