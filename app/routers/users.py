import uuid
from logging import getLogger
from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import InvalidData
from app.models import RecordCreate, PatientCreate, UserCreate, UserResponse, PhysicianCreate, PatientResponse, \
    PhysicianResponse
from database.models import User, Patient, Physician
from database.session import get_db

users_api_router = APIRouter(prefix="/api", tags=["api"])
api_logger = getLogger('api')


# Example API endpoint to add a new user to the database
@users_api_router.post("/user/",
                       summary="Create a new user.",
                       status_code=status.HTTP_201_CREATED,
                       response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_instance = User(**user.model_dump())

    db.add(user_instance)
    try:
        db.commit()
        db.refresh(user_instance)
    except IntegrityError:
        raise InvalidData()
    return user_instance.__dict__


@users_api_router.post("/patient/",
                       summary="Create a new patient.",
                       status_code=status.HTTP_201_CREATED,
                       response_model=PatientResponse)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    patient_instance = Patient(**patient.model_dump())

    db.add(patient_instance)

    try:
        db.commit()
        db.refresh(patient_instance)
    except (IntegrityError, ValidationError):
        raise InvalidData()
    return patient_instance.__dict__


@users_api_router.post("/physician/",
                       summary="Create a new physician.",
                       status_code=status.HTTP_201_CREATED,
                       response_model=PhysicianResponse)
async def create_physician(physician: PhysicianCreate, db: Session = Depends(get_db)):
    physician_instance = Physician(**physician.model_dump())
    db.add(physician_instance)

    try:
        db.commit()
        db.refresh(physician_instance)
    except (IntegrityError, ValidationError):
        raise InvalidData()
    return physician_instance.__dict__
