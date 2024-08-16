import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User

class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)

class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)

class ItemUpdate(ItemBase):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)

class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="items", sa_relationship_kwargs={"foreign_keys": "Item.owner_id"})

class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID

class ItemsPublic(SQLModel):
    data: List[ItemPublic]
    count: int