from sqlalchemy import Column, Integer, String, Text
from .base_config import Base
#from models.base_config import Base #for migration


class Evenement(Base):
    """evenement model."""
    __tablename__ = "evenement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contrat_id = Column(Integer, nullable=False)
    client_name = Column(String(100), nullable=False)
    client_contact_id = Column(Integer, nullable=False)
    support_id = Column(String(100), nullable=True)
    start_date = Column(String(100), nullable=False)
    end_date = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    expected = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

