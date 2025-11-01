from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Patient(Base):

    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, Index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    reaction_time = Column(Float, nullable=False)
    pupil_dialation = Column(Float, nullable=False)
    eye_velocity = Column(Float, nullable=False)


