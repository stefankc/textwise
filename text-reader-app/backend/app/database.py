"""Database configuration and setup using SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Replace the following values according to your PostgreSQL configuration
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Construct the database URL
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{
    DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
print(DATABASE_URL)
print('DATABASE_URL')
# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True  # Enables SQL logging, useful for debugging
)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()
