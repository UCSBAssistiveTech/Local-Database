from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://test:test@localhost:5432/postgrestest"
engine = create_engine(DATABASE_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def inject_session():
    db = session()
    try:
        yield db
    finally:
        db.close()
