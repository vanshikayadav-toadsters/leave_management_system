import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from alembic import context
from sqlmodel import SQLModel

# Add project root
sys.path.append(os.getcwd())

# ✅ Import your app settings
from src.core.settings import settings

# Import models (IMPORTANT for metadata)
from src.db.models.user_model import User
from src.db.models.leave_request_model import LeaveRequest, LeaveStatus
from src.db.models.leave_balance_model import LeaveBalance

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata
target_metadata = SQLModel.metadata

# ✅ FORCE correct DB
DATABASE_URL = settings.DATABASE_URL
print("🚀 ALEMBIC USING DB:", DATABASE_URL)


# ------------------------
# OFFLINE MODE
# ------------------------
def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ------------------------
# ONLINE MODE
# ------------------------
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        version_table_schema="public",
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(
        DATABASE_URL,
        echo=True,
    )

    async with connectable.connect() as connection:
        # ensure schema
        await connection.execute(text("SET search_path TO public"))

        # Run migrations in Alembic transaction
        await connection.run_sync(do_run_migrations)

        # Explicit commit after running migrations
        await connection.commit()

    await connectable.dispose()


# ------------------------
# ENTRY POINT
# ------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())