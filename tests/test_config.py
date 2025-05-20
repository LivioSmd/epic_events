# backend/test_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

# SQLite in-memory DB (volatile, pour les tests uniquement)
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crée les tables à la volée
Base.metadata.create_all(bind=engine)
