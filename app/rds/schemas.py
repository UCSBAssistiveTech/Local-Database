from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    age: int

class PatientInteract(PatientBase):
    id: int

class PatientRead(PatientBase):
    id: int

    class Config:
        from_attributes = True

class ExamBase(BaseModel):
    reaction_time: float
    pupil_dialation: float
    eye_velocity: float
    patient_id: int

class ExamInteract(ExamBase):
    id: int

class ExamRead(ExamBase):
    id: int

    class Config:
        from_attributes = True