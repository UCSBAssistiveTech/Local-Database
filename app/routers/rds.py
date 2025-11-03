from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from rds.db import inject_session
from rds import crud
from rds.schemas import PatientBase, PatientInteract, PatientRead, ExamBase, ExamInteract, ExamRead

router = APIRouter(prefix="/rds", tags=["rds"])

@router.get("/health")
def health():
    return {"status": "RDS router is running"}

# Patient endpoints
@router.post("/patients", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientBase, db: Session = Depends(inject_session)):
    return crud.create_patient(db=db, patient=patient)

@router.get("/patients", response_model=List[PatientRead])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(inject_session)):
    patients = crud.get_patients(db=db, skip=skip, limit=limit)
    return patients

@router.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(inject_session)):
    patient = crud.get_patient(db=db, patient_id=patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/patients", response_model=PatientRead)
def update_patient(patient: PatientInteract, db: Session = Depends(inject_session)):
    updated_patient = crud.update_patient(db=db, patient_data=patient)
    if updated_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient

@router.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(inject_session)):
    success = crud.delete_patient(db=db, patient_id=patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return

# Exam endpoints
@router.post("/exams", response_model=ExamRead, status_code=status.HTTP_201_CREATED)
def create_exam(exam: ExamBase, db: Session = Depends(inject_session)):
    return crud.create_exam(db=db, exam=exam)

@router.get("/exams", response_model=List[ExamRead])
def get_exams(skip: int = 0, limit: int = 100, db: Session = Depends(inject_session)):
    exams = crud.get_exams(db=db, skip=skip, limit=limit)
    return exams

@router.get("/exams/{exam_id}", response_model=ExamRead)
def get_exam(exam_id: int, db: Session = Depends(inject_session)):
    exam = crud.get_exam(db=db, exam_id=exam_id)
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.get("/patients/{patient_id}/exams", response_model=List[ExamRead])
def get_patient_exams(patient_id: int, db: Session = Depends(inject_session)):
    # First check if patient exists
    patient = crud.get_patient(db=db, patient_id=patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    exams = crud.get_exams_by_patient(db=db, patient_id=patient_id)
    return exams

@router.put("/exams", response_model=ExamRead)
def update_exam(exam: ExamInteract, db: Session = Depends(inject_session)):
    updated_exam = crud.update_exam(db=db, exam_data=exam)
    if updated_exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return updated_exam

@router.delete("/exams/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(exam_id: int, db: Session = Depends(inject_session)):
    success = crud.delete_exam(db=db, exam_id=exam_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exam not found")
    return