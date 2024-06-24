# from logging import getLogger
#
# from fastapi import APIRouter
#
# from app.exceptions import InvalidData
# from app.models import RecordCreate
#
# record_api_router = APIRouter(prefix="/api", tags=["api"])
# api_logger = getLogger('api')
#
#
# @record_api_router.get("/records/")
# async def get_all_records():
#     return await db.fetch_records()
#
#
# @record_api_router.get("/records/patient/")
# async def get_patient_record(id: str):
#     validated_patient = await db.validate_patients(id)
#     if not validated_patient:
#         api_logger.info('Incorrect patient id')
#         raise InvalidData()
#
#     api_logger.info('validate patient with id: %s', id)
#     return await db.fetch_records_patient_specific(id)
#
#
# @record_api_router.post("/records/")
# async def create_record(record: RecordCreate):
#     validated_patient = await db.validate_patients(record.patient_id)
#     if not validated_patient:
#         api_logger.info('Incorrect patient id')
#         raise InvalidData()
#
#     api_logger.info('validate patient with id: %s', record.patient_id)
#     return await db.create_records(record)
