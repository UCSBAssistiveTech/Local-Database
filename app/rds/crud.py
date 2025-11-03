from sqlalchemy.orm import Session
from rds.models import Patient, Exam
from rds.schemas import PatientBase, PatientInteract, ExamBase, ExamInteract
from typing import List, Optional

def create_patient(db: Session, patient: PatientBase) -> Patient:
    patient = Patient(name=patient.name, age=patient.age)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def create_exam(db: Session, exam: ExamBase) -> Exam:
    exam_record = Exam(
        reaction_time=exam.reaction_time,
        pupil_dialation=exam.pupil_dialation,
        eye_velocity=exam.eye_velocity,
        patient_id=exam.patient_id
    )
    db.add(exam_record)
    db.commit()
    db.refresh(exam_record)
    return exam_record

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()

def update_patient(db: Session, patient_data: PatientInteract) -> Optional[Patient]:
    patient = db.query(Patient).filter(Patient.id == patient_data.id).first()
    if patient:
        patient.name = patient_data.name
        patient.age = patient_data.age
        db.commit()
        db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int) -> bool:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient:
        db.delete(patient)
        db.commit()
        return True
    return False

def get_exam(db: Session, exam_id: int) -> Optional[Exam]:
    return db.query(Exam).filter(Exam.id == exam_id).first()

def get_exams(db: Session, skip: int = 0, limit: int = 100) -> List[Exam]:
    return db.query(Exam).offset(skip).limit(limit).all()

def get_exams_by_patient(db: Session, patient_id: int) -> List[Exam]:
    return db.query(Exam).filter(Exam.patient_id == patient_id).all()

def update_exam(db: Session, exam_data: ExamInteract) -> Optional[Exam]:
    exam = db.query(Exam).filter(Exam.id == exam_data.id).first()
    if exam:
        exam.reaction_time = exam_data.reaction_time
        exam.pupil_dialation = exam_data.pupil_dialation
        exam.eye_velocity = exam_data.eye_velocity
        exam.patient_id = exam_data.patient_id
        db.commit()
        db.refresh(exam)
    return exam

def delete_exam(db: Session, exam_id: int) -> bool:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam:
        db.delete(exam)
        db.commit()
        return True
    return False