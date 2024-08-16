import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .job import Job

class Company(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)
    website: Optional[str] = Field(default=None, max_length=255)

    users: List["User"] = Relationship(back_populates="company", sa_relationship_kwargs={"foreign_keys": "User.company_id"})
    jobs: List["Job"] = Relationship(back_populates="company", sa_relationship_kwargs={"foreign_keys": "Job.company_id"})

class CompanyPublic(SQLModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    website: Optional[str]