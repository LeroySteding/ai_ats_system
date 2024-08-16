from sqlmodel import Session, create_engine, select
from app import crud
from app.core.config import settings
from app.models import User, UserCreate

# Initialize the engine with the database URI
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    # Check if the first superuser already exists
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()

    # If the superuser doesn't exist, create one
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

        # Add the user to the session and commit the transaction
        session.add(user)
        session.commit()
        session.refresh(user)

    # Optional: Log or print confirmation that the superuser was created or already exists
    print(f"Superuser {user.email} exists or was created successfully.")
