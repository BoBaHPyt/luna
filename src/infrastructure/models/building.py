from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship

from src.infrastructure.database import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=False)
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)

    organizations = relationship("Organization", back_populates="building")
