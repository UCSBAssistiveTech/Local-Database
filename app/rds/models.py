from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Patient(Base):

    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, Index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    exams = relationship("Exam", back_populates="patient")


class Exam(Base):

    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True, Index=True)
    reaction_time = Column(Float, nullable=False)
    pupil_dialation = Column(Float, nullable=False)
    eye_velocity = Column(Float, nullable=False)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship("Patient", back_populates="exams")