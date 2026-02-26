from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from src.infrastructure.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=True)
    level = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="check_activity_level"),
    )

    parent = relationship("Activity", remote_side=[id], backref="children")
    organizations = relationship("Organization", secondary="organization_activities", back_populates="activities")
