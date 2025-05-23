from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base_config import Base
#from models.base_config import Base #for migration
from datetime import date


class Client(Base):
    """client model."""
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    company_name = Column(String(150), nullable=False)
    user_contact_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # foreign key to User
    # ORM relationship (allowing direct access to the User object
    # a field not stored in the database)
    user_contact = relationship("User")
    information = Column(Text, nullable=False)
    creation_date = Column(Date, default=date.today(), nullable=False)
    last_update = Column(Date, default=date.today(), onupdate=date.today(), nullable=False)
