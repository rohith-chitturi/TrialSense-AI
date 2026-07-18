import uuid
from datetime import date, datetime
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fhir_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String)
    birth_date = Column(Date)
    
    # Store full FHIR JSON resource for interoperability
    fhir_resource = Column(JSONB)
    
    conditions = relationship("Condition", back_populates="patient")
    observations = relationship("Observation", back_populates="patient")

class Condition(Base):
    """FHIR Condition resource representing diagnoses/problems"""
    __tablename__ = "conditions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    
    # Ontology coding
    system = Column(String, default="http://hl7.org/fhir/sid/icd-10")
    code = Column(String, nullable=False)
    display = Column(String)
    
    recorded_date = Column(DateTime, default=datetime.utcnow)
    fhir_resource = Column(JSONB)
    
    patient = relationship("Patient", back_populates="conditions")

class Observation(Base):
    """FHIR Observation resource representing lab results/vitals"""
    __tablename__ = "observations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    
    # Ontology coding (LOINC)
    system = Column(String, default="http://loinc.org")
    code = Column(String, nullable=False)
    display = Column(String)
    
    value_quantity = Column(JSON) # e.g. {"value": 5.4, "unit": "mmol/L"}
    effective_datetime = Column(DateTime)
    
    fhir_resource = Column(JSONB)
    
    patient = relationship("Patient", back_populates="observations")
