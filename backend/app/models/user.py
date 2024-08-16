import uuid
from typing import Optional, List, TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .role import Role
    from .company import Company
    from .profile import Profile
    from .item import Item
    from .application import Application

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = Field(default=None, max_length=255)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: Optional[str] = Field(default=None, max_length=255)

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=40)

class UserUpdateMe(SQLModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[EmailStr] = Field(default=None, max_length=255)

class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
    
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    role_id: Optional[uuid.UUID] = Field(default=None, foreign_key="role.id", nullable=True)
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="company.id", nullable=True)
    profile_id: Optional[uuid.UUID] = Field(default=None, foreign_key="profile.id", nullable=True)

    role: Optional["Role"] = Relationship(back_populates="users", sa_relationship_kwargs={"foreign_keys": "User.role_id"})
    company: Optional["Company"] = Relationship(back_populates="users", sa_relationship_kwargs={"foreign_keys": "User.company_id"})
    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "foreign_keys": "Profile.user_id"
        }
    )
    items: List["Item"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    applications: List["Application"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int  