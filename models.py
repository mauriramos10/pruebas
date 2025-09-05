
import os
from datetime import datetime
from sqlalchemy import create_engine, String, Integer, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

class Base(DeclarativeBase):
    pass

def get_engine_and_session(database_url: str):
    engine = create_engine(database_url, echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return engine, SessionLocal

class Equipment(Base):
    __tablename__ = "equipment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    sap_number: Mapped[str] = mapped_column(String(100), nullable=True)
    tag: Mapped[str] = mapped_column(String(100), nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    criticality: Mapped[str] = mapped_column(String(50), nullable=True, default="Media")
    status: Mapped[str] = mapped_column(String(50), nullable=True, default="Operativo")
    description: Mapped[str] = mapped_column(Text, nullable=True)

    maintenance: Mapped[list["Maintenance"]] = relationship("Maintenance", back_populates="equipment", cascade="all, delete-orphan")

    def to_dict(self, detail: bool=False):
        data = {
            "id": self.id,
            "name": self.name,
            "sap_number": self.sap_number,
            "tag": self.tag,
            "location": self.location,
            "criticality": self.criticality,
            "status": self.status,
            "description": self.description,
        }
        if detail:
            data["maintenance"] = [m.to_dict() for m in self.maintenance]
        return data

class Maintenance(Base):
    __tablename__ = "maintenance"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    performed: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    technician: Mapped[str] = mapped_column(String(120), nullable=True)
    hours: Mapped[float] = mapped_column(Float, default=0.0)

    equipment: Mapped["Equipment"] = relationship("Equipment", back_populates="maintenance")

    def to_dict(self):
        return {
            "id": self.id,
            "equipment_id": self.equipment_id,
            "date": self.date.isoformat(),
            "performed": self.performed,
            "notes": self.notes,
            "technician": self.technician,
            "hours": self.hours,
        }
