from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    age: int

class PateintRead(PatientBase):
    id: int
    class Config:
        orm_mode = True


class ExamBase(BaseModel):
    reaction_time: float
    pupil_dialation: float
    eye_velocity: float
    patient_id: int

class ExamRead(ExamBase):
    id: int
    class Config:
        orm_mode = True