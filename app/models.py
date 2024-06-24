from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr, UUID4


class RecordCreate(BaseModel):
    physician_id: UUID4
    patient_id: UUID4
    diagnosis: str
    healthy: bool


class RecordResponse(BaseModel):
    id: UUID4
    physician_id: UUID4
    patient_id: UUID4
    diagnosis: str
    healthy: bool


class PatientCreate(BaseModel):
    user_id: UUID4
    name: str
    age: int


class PatientResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    name: str
    age: int


class PhysicianCreate(BaseModel):
    user_id: UUID4
    name: str
    speciality: str


class PhysicianResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    name: str
    speciality: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID4 = None
    username: str
    email: EmailStr
    password: str
