from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:Jumpjet;@localhost/epic_events"
engine = create_engine(DATABASE_URL, echo=False)  # echo=True, display every SQL queries in the console.
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
