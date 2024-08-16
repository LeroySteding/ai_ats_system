import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel, Column

if TYPE_CHECKING:
    from .user import User

class Profile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True, nullable=False)
    bio: Optional[str] = Field(default=None)
    skills: Optional[List[str]] = Field(sa_column=Column(JSONB), default=None)
    experience: Optional[List[dict]] = Field(sa_column=Column(JSONB), default=None)
    education: Optional[List[dict]] = Field(sa_column=Column(JSONB), default=None)
    job_preferences: Optional[List[dict]] = Field(sa_column=Column(JSONB), default=None)
    resume_url: Optional[str] = Field(default=None, max_length=255)

    user: "User" = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={
            "foreign_keys": "Profile.user_id"  # Specify the correct foreign key
        }
    )

class ProfilePublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    bio: Optional[str]
    skills: Optional[List[str]]
    experience: Optional[List[dict]]
    education: Optional[List[dict]]
    job_preferences: Optional[List[dict]]
    resume_url: Optional[str]