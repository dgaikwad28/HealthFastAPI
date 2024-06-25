from logging import getLogger
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, status

from app.exceptions import InvalidData
from app.models import RecordCreate, RecordResponse
from database.models import Record
from database.session import get_db

record_api_router = APIRouter(prefix="/api", tags=["api"])
api_logger = getLogger('api')


@record_api_router.post(
    "/record/",
    summary="Create a new record.",
    status_code=status.HTTP_201_CREATED,
    response_model=RecordResponse,
)
async def create_record_route(record: RecordCreate, db: Session = Depends(get_db)):
    """
        Create a new record.

        Args:
        - record: RecordCreate - The record data to be created.
        - db: Session - The database session.

        Returns:
        - dict: The created record data.

        Raises:
        - InvalidData: If the data provided is invalid.
    """
    record_instance = Record(**record.model_dump())
    db.add(record_instance)
    try:
        db.commit()
        db.refresh(record_instance)
    except IntegrityError:
        raise InvalidData()
    return record_instance.__dict__


@record_api_router.get(
    "/record/patient/",
    summary="Get a patient's record.",
    status_code=status.HTTP_200_OK,
    response_model=List[RecordCreate],
)
async def get_record_route(patient_id: UUID = None, db: Session = Depends(get_db)):
    """
        Get a patient's record.

        Args:
        - patient_id: UUID - The patient's ID for retrieving records.
        - db: Session - The database session.

        Returns:
        - List[dict]: A list of patient's record data.

    """
    record_queryset = db.query(Record).filter(Record.patient_id == patient_id).all()
    if not record_queryset:
        return record_queryset
    return [record_instance.__dict__ for record_instance in record_queryset]
