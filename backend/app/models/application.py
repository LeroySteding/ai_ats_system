import uuid
import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .job import Job
    from .user import User

class Application(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    job_id: uuid.UUID = Field(foreign_key="job.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    cover_letter: Optional[str] = Field(default=None)
    status: str = Field(default="Submitted", max_length=50)
    applied_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    job: "Job" = Relationship(back_populates="applications", sa_relationship_kwargs={"foreign_keys": "Application.job_id"})
    user: "User" = Relationship(back_populates="applications", sa_relationship_kwargs={"foreign_keys": "Application.user_id"})


class ApplicationPublic(SQLModel):
    id: uuid.UUID
    job_id: uuid.UUID
    user_id: uuid.UUID
    cover_letter: Optional[str]
    status: str
    applied_at: datetime.datetime