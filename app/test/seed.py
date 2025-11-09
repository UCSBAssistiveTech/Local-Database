from sqlalchemy.orm import Session
from app.rds.models import Patient, Exam
from app.rds.db import session
from random import uniform, randint

def seed_database():
    db = session()
    try:
        # Clear existing data
        db.query(Exam).delete()
        db.query(Patient).delete()
        
        # Seed patients with more diverse data
        patients = [
            Patient(name="John Doe", age=45),
            Patient(name="Jane Smith", age=32),
            Patient(name="Bob Johnson", age=28),
            Patient(name="Maria Garcia", age=56),
            Patient(name="David Chen", age=19),
            Patient(name="Sarah Williams", age=41),
            Patient(name="James Wilson", age=67),
            Patient(name="Emma Brown", age=23),
            Patient(name="Michael Davis", age=38),
            Patient(name="Lisa Anderson", age=49)
        ]
        db.add_all(patients)
        db.commit()

        # Seed multiple exams per patient with realistic ranges
        exams = []
        for patient in patients:
            # Generate 2-4 exams per patient
            num_exams = randint(2, 4)
            for _ in range(num_exams):
                exams.append(
                    Exam(
                        reaction_time=round(uniform(0.15, 0.8), 2),  # typical reaction times in seconds
                        pupil_dialation=round(uniform(2.0, 8.0), 1),  # pupil size in mm
                        eye_velocity=round(uniform(8.0, 15.0), 1),  # typical saccadic velocity
                        patient_id=patient.id
                    )
                )

        db.add_all(exams)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()