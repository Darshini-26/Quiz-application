from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config.config as config

# Retrieve the DATABASE_URL from config.py (via SSM)
DATABASE_URL = config.database_url()

if not DATABASE_URL:
    raise RuntimeError("Failed to retrieve the database URL from SSM.")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,              # Number of connections in the pool
    max_overflow=20,           # Extra connections beyond the pool size
    pool_timeout=30,           # Timeout for getting a connection from the pool
    pool_recycle=3600,         # Recycle connections every hour to avoid stale connections
    connect_args={"connect_timeout": 30}  # Connection timeout in seconds
)

# Set up the session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()  # Create a new session from the sessionmaker
    try:
        yield db
    finally:
        db.close()  # Ensure this line is not indented under the try block

# Create all tables in the database
Base.metadata.create_all(bind=engine)
