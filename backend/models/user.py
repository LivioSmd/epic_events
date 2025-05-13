from sqlalchemy import Column, Integer, String
import bcrypt
from .base_config import Base
#from models.base_config import Base #for migration


class User(Base):
    """User model."""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    type = Column(String(50), nullable=False)  # commercial, gestion, support
    password_hash = Column(String(255), nullable=False)

    def set_password(self, password):
        """Hash and store the password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Verify the password against the stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
