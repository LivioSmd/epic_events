from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base_config import Base
# from models.base_config import Base #for migration
from datetime import date


class Contrat(Base):
    """contrat model."""
    __tablename__ = "contrat"

    id = Column(Integer, primary_key=True, autoincrement=True)

    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)  # foreign key to Client
    # ORM relationship (allowing direct access to the Client object
    # a field not stored in the database)
    client = relationship("Client")
    commercial_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    commercial = relationship("User")
    total_amount = Column(Float, nullable=False)
    outstanding_amount = Column(Float, nullable=False)
    creation_date = Column(Date, nullable=False, default=date.today())
    signed = Column(Integer, default=0, nullable=False)
