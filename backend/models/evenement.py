from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base_config import Base
#from models.base_config import Base #for migration


class Evenement(Base):
    """evenement model."""
    __tablename__ = "evenement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contrat_id = Column(Integer, ForeignKey("contrat.id"), nullable=False)  # foreign key to Contrat
    contrat = relationship("Contrat")
    client_name = Column(String(100), nullable=False)
    client_contact_id = Column(Integer, ForeignKey("client.id"), nullable=False)  # foreign key to Client
    client = relationship("Client")
    support_id = Column(Integer, ForeignKey("user.id"), nullable=True)  # # foreign key to User
    support = relationship("User")
    start_date = Column(String(100), nullable=False)
    end_date = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    expected = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

