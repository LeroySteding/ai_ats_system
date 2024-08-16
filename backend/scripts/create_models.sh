#!/bin/bash

# Maak de models directory aan
mkdir -p backend/app/models

# Maak de __init__.py file aan
cat <<EOL > backend/app/models/__init__.py
from .role import Role, RolePermissionLink
from .permission import Permission
from .user import User, UserBase, UserCreate, UserRegister, UserUpdate, UserUpdateMe, UpdatePassword, UserPublic, UsersPublic
from .company import Company
from .profile import Profile
from .job import Job
from .application import Application
from .item import Item, ItemBase, ItemCreate, ItemUpdate, ItemPublic, ItemsPublic
from .utility import Message, Token, TokenPayload, NewPassword
EOL

# Maak de role.py file aan
cat <<EOL > backend/app/models/role.py
import uuid
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

class Role(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    users: List["User"] = Relationship(back_populates="role")

class RolePermissionLink(SQLModel, table=True):
    role_id: uuid.UUID = Field(foreign_key="role.id", primary_key=True)
    permission_id: uuid.UUID = Field(foreign_key="permission.id", primary_key=True)
EOL

# Maak de permission.py file aan
cat <<EOL > backend/app/models/permission.py
import uuid
from typing import Optional
from sqlmodel import Field, SQLModel

class Permission(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
EOL

# Maak de user.py file aan
cat <<EOL > backend/app/models/user.py
import uuid
from typing import Optional, List
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

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
    role_id: uuid.UUID = Field(foreign_key="role.id", nullable=True)
    company_id: uuid.UUID = Field(foreign_key="company.id", nullable=True)
    profile_id: uuid.UUID = Field(foreign_key="profile.id", nullable=True)

    role: Optional["Role"] = Relationship(back_populates="users")
    company: Optional["Company"] = Relationship(back_populates="users")
    profile: Optional["Profile"] = Relationship(back_populates="user")
    items: List["Item"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    applications: List["Application"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int
EOL

# Maak de company.py file aan
cat <<EOL > backend/app/models/company.py
import uuid
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

class Company(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)
    website: Optional[str] = Field(default=None, max_length=255)

    users: List["User"] = Relationship(back_populates="company")
    jobs: List["Job"] = Relationship(back_populates="company")
EOL

# Maak de profile.py file aan
cat <<EOL > backend/app/models/profile.py
import uuid
from typing import Optional, List, Annotated
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

class Profile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True, nullable=False)
    bio: Optional[str] = Field(default=None)
    skills: Optional[Annotated[List[str], JSONB]] = Field(sa_column=JSONB, default=None)
    experience: Optional[Annotated[List[dict], JSONB]] = Field(sa_column=JSONB, default=None)
    education: Optional[Annotated[List[dict], JSONB]] = Field(sa_column=JSONB, default=None)
    job_preferences: Optional[Annotated[List[dict], JSONB]] = Field(sa_column=JSONB, default=None)
    resume_url: Optional[str] = Field(default=None, max_length=255)

    user: "User" = Relationship(back_populates="profile")
EOL

# Maak de job.py file aan
cat <<EOL > backend/app/models/job.py
import uuid
from typing import Optional, List, Annotated
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

class Job(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None, max_length=255)
    salary_range: Optional[str] = Field(default=None, max_length=100)
    employment_type: str = Field(max_length=50)
    requirements: Optional[Annotated[List[str], JSONB]] = Field(sa_column=JSONB, default=None)
    benefits: Optional[Annotated[List[str], JSONB]] = Field(sa_column=JSONB, default=None)
    company_id: uuid.UUID = Field(foreign_key="company.id", nullable=False)

    company: "Company" = Relationship(back_populates="jobs")
    applications: List["Application"] = Relationship(back_populates="job", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
EOL

# Maak de application.py file aan
cat <<EOL > backend/app/models/application.py
import uuid
import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Application(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    job_id: uuid.UUID = Field(foreign_key="job.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    cover_letter: Optional[str] = Field(default=None)
    status: str = Field(default="Submitted", max_length=50)
    applied_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    job: "Job" = Relationship(back_populates="applications")
    user: "User" = Relationship(back_populates="applications")
EOL

# Maak de item.py file aan
cat <<EOL > backend/app/models/item.py
import uuid
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

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
    owner: Optional["User"] = Relationship(back_populates="items")

class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID

class ItemsPublic(SQLModel):
    data: List[ItemPublic]
    count: int
EOL

# Maak de utility.py file aan
cat <<EOL > backend/app/models/utility.py
from typing import Optional
from sqlmodel import Field, SQLModel

class Message(SQLModel):
    message: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: Optional[str] = None

class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
EOL

echo "Bestanden en mappen zijn aangemaakt."