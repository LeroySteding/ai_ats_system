import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .company import Company
    from .application import Application

class Job(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None, max_length=255)
    salary_range: Optional[str] = Field(default=None, max_length=100)
    employment_type: str = Field(max_length=50)
    requirements: Optional[List[str]] = Field(sa_column=Column(JSONB), default=None)
    benefits: Optional[List[str]] = Field(sa_column=Column(JSONB), default=None)
    company_id: uuid.UUID = Field(foreign_key="company.id", nullable=False)

    company: "Company" = Relationship(back_populates="jobs", sa_relationship_kwargs={"foreign_keys": "Job.company_id"})
    applications: List["Application"] = Relationship(back_populates="job", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class JobPublic(SQLModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    location: Optional[str]
    salary_range: Optional[str]
    employment_type: str
    requirements: Optional[List[str]]
    benefits: Optional[List[str]]
    company_id: uuid.UUID