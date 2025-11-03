from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    age: int

class PatientInteract(PatientBase):
    id: int

class ExamBase(BaseModel):
    reaction_time: float
    pupil_dialation: float
    eye_velocity: float
    patient_id: int

class ExamInteract(ExamBase):
    id: int