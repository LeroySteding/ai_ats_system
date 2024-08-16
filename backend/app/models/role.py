import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User

class Role(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    users: List["User"] = Relationship(back_populates="role", sa_relationship_kwargs={"foreign_keys": "User.role_id"})

class RolePermissionLink(SQLModel, table=True):
    role_id: uuid.UUID = Field(foreign_key="role.id", primary_key=True)
    permission_id: uuid.UUID = Field(foreign_key="permission.id", primary_key=True)

class RolePublic(SQLModel):
    id: uuid.UUID
    name: str
    description: Optional[str]