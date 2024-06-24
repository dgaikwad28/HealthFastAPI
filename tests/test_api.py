import datetime
import json
import uuid
from unittest import TestCase
from fastapi.testclient import TestClient

from app.main import app
from database.models import User, Physician, Patient, Record

from tests.conftest import setup, teardown, TestingSessionLocal


class PatientAPITestCase(TestCase, ):

    def setUp(self):
        setup()
        self.headers = {'HTTP_ACCEPT': 'application/json'}
        self.get_patients_url = "/api/patients/"
        self.records_url = "/api/records/"
        self.get_patient_records_url = "/api/records/patient/"
        self.client = TestClient(app)

        # create physician
        physician_user_instance = User(
            id=uuid.uuid4(),  # Replace with the actual UUID if needed
            username="test_physician",
            email="test_physician@example.com",
            password="testpassword",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

        self.physician_instance = Physician(
            id=uuid.uuid4(),  # Replace with the actual UUID if needed
            user_id=physician_user_instance.id,
            name="Dr. Smith",
            speciality="Cardiology"
        )

        # create patient
        patient_user_instance = User(
            id=uuid.uuid4(),  # Replace with the actual UUID if needed
            username="test_patient",
            email="test_patient@example.com",
            password="testpassword",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        self.patient_instance = Patient(
            id=uuid.uuid4(),  # Replace with the actual UUID if needed
            user_id=patient_user_instance.id,
            name="Smith",
            age=30
        )

    def tearDown(self):
        teardown()

    def test_invalid_id__get_record__400(self):
        patient_id = uuid.uuid4()
        response = self.client.get(f"/api/record/patient/?patient_id={patient_id}",
                                   headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), [])

    def test_invalid_type__get_record__400(self):
        patient_id = 'test'
        response = self.client.get(f"/api/record/patient/?patient_id={patient_id}",
                                   headers=self.headers)

        self.assertEqual(400, response.status_code)

    def test_invalid_query_param__get_record__400(self):
        response = self.client.get(f"/api/record/patient/?invalid={self.patient_instance.id}",
                                   headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), [])

    def test_valid_query_param__get_record__200(self):
        response = self.client.get(f"/api/record/patient/?patient_id={self.patient_instance.id}",
                                   headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), [])

        # create record
        diagnosis_value = "alles gut"
        record_instance = Record(id=uuid.uuid4(),
                                 physician_id=self.physician_instance.id,
                                 patient_id=self.patient_instance.id,
                                 diagnosis=diagnosis_value,
                                 healthy=True)
        session = TestingSessionLocal()
        session.add(record_instance)
        session.commit()
        session.close()

        response_later = self.client.get(f"/api/record/patient/?patient_id={self.patient_instance.id}",
                                         headers=self.headers)

        self.assertEqual(200, response_later.status_code)
        response_content = json.loads(response_later.content)[0]
        self.assertEqual(response_content.get('physician_id'), str(self.physician_instance.id))
        self.assertEqual(response_content.get('patient_id'), str(self.patient_instance.id))
        self.assertEqual(response_content.get('diagnosis'), diagnosis_value)
        self.assertTrue(response_content.get('healthy'))

        def test_create_record__200(self):
            # create physician
            physician_user_response = self.client.post(f"/api/user/",
                                                       data=json.dumps({
                                                           "username": "test",
                                                           "email": "test@test.de",
                                                           "password": "alles gut"
                                                       }),
                                                       headers=self.headers)
            self.assertEqual(201, physician_user_response.status_code)
            physician_user_id = json.loads(physician_user_response.content).get('id')

            physician_response = self.client.post(f"/api/physician/",
                                                  data=json.dumps({
                                                      "user_id": physician_user_id,
                                                      "name": "test",
                                                      "speciality": "test_speciality"
                                                  }),
                                                  headers=self.headers)
            self.assertEqual(201, physician_response.status_code)
            physician_id = json.loads(physician_response.content).get('id')

            # create patient
            patient_user_response = self.client.post(f"/api/user/",
                                                     data=json.dumps({
                                                         "username": "test",
                                                         "email": "test_patient@test.de",
                                                         "password": "alles gut"
                                                     }),
                                                     headers=self.headers)
            self.assertEqual(201, patient_user_response.status_code)
            patient_user_id = json.loads(physician_user_response.content).get('id')

            patient_response = self.client.post(f"/api/patient/",
                                                data=json.dumps({
                                                    "user_id": patient_user_id,
                                                    "name": "test",
                                                    "age": 30
                                                }),
                                                headers=self.headers)
            self.assertEqual(201, patient_response.status_code)
            patient_id = json.loads(patient_response.content).get('id')

            response = self.client.post(f"/api/record/",
                                        data=json.dumps({
                                            "physician_id": physician_id,
                                            "patient_id": patient_id,
                                            "diagnosis": "alles gut",
                                            "healthy": True
                                        }),
                                        headers=self.headers)

            self.assertEqual(201, response.status_code)
