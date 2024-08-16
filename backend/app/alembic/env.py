import os
from logging.config import fileConfig
from importlib import import_module

from alembic import context
from sqlalchemy import engine_from_config, pool

# Dit is het Alembic Config object, dat toegang biedt tot de waarden in het .ini-bestand dat in gebruik is.
config = context.config

# Interpreteer het configuratiebestand voor Python logging.
# Deze regel stelt loggers in.
fileConfig(config.config_file_name)

# Dynamisch importeren van modellen om circulaire importen te vermijden
models = [
    "app.models.role",
    "app.models.permission",
    "app.models.user",
    "app.models.company",
    "app.models.profile",
    "app.models.job",
    "app.models.application",
    "app.models.item",
    "app.models.utility",
]

for model in models:
    import_module(model)

from sqlmodel import SQLModel
from app.core.config import settings  # noqa

target_metadata = SQLModel.metadata

# Andere waarden uit de configuratie, gedefinieerd door de behoeften van env.py,
# kunnen worden verkregen:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    return str(settings.SQLALCHEMY_DATABASE_URI)

def run_migrations_offline():
    """Voer migraties uit in 'offline' modus.

    Dit configureert de context met alleen een URL
    en niet een Engine, hoewel een Engine hier ook acceptabel is.
    Door het Engine aanmaken over te slaan, hoeven we niet eens een DBAPI beschikbaar te hebben.

    Oproepen naar context.execute() hier geven de opgegeven string door aan de
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Voer migraties uit in 'online' modus.

    In dit scenario moeten we een Engine maken
    en een verbinding associëren met de context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()