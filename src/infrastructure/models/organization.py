from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.infrastructure.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False)

    building = relationship("Building", back_populates="organizations")
    phones = relationship("OrganizationPhone", back_populates="organization", cascade="all, delete-orphan")
    activities = relationship("Activity", secondary="organization_activities", back_populates="organizations")


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    phone = Column(String(20), nullable=False)

    organization = relationship("Organization", back_populates="phones")


class OrganizationActivity(Base):
    __tablename__ = "organization_activities"

    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)
