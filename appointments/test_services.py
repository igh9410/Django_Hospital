from datetime import datetime, time
from django.test import TestCase
from django.utils import timezone
from appointments.services import create_appointment_request_service
from doctors.models import Doctor, WorkingHour, Specialty
from patients.models import Patient

class AppointmentRequestServiceTest(TestCase):

    def setUp(self):
        # Create Specialty instances
        specialties = [
            Specialty.objects.create(name="정형외과"),
            Specialty.objects.create(name="내과"),
            Specialty.objects.create(name="일반의")
        ]

        # Create Doctor and Patient instances
        self.doctor = Doctor.objects.create(name="김의사", hospital="서울대병원")
        for specialty in specialties:
            self.doctor.specialties.add(specialty)
        self.patient = Patient.objects.create(name="김환자")

        # Set up doctor's working hours
        self.working_hour = WorkingHour.objects.create(
            doctor=self.doctor,
            day_of_week='Monday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        )
        self.working_hour = WorkingHour.objects.create(
            doctor=self.doctor,
            day_of_week='Tuesday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        )
        self.working_hour = WorkingHour.objects.create(
            doctor=self.doctor,
            day_of_week='Wednesday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        )
        self.working_hour = WorkingHour.objects.create(
            doctor=self.doctor,
            day_of_week='Thursday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        )
        self.working_hour = WorkingHour.objects.create(
            doctor=self.doctor,
            day_of_week='Friday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        )
       


    def test_appointment_request_service_with_arbitrary_datetime(self): ## Testing with multiple request time, like night hours, holiday
        # Verify that Doctor and WorkingHour objects are created
        self.assertEqual(Doctor.objects.count(), 1)
        self.assertEqual(WorkingHour.objects.count(), 5)

        # Verify the attributes of the created Doctor
        doctor = Doctor.objects.first()
        self.assertEqual(doctor.name, "김의사")
        self.assertEqual(doctor.hospital, "서울대병원")

        # Verify the WorkingHour is linked to the Doctor
       
        # Create an arbitrary datetime for request
        preferred_datetime = timezone.make_aware(datetime(2022, 1, 18, 10, 0))
        request_datetime = timezone.make_aware(datetime(2022, 1, 15, 1, 0))
        print("WorkingHour: ", self.working_hour)

        # Call your service function with this arbitrary datetime
        result = create_appointment_request_service(
            patient_id=self.patient.id, 
            doctor_id=self.doctor.id, 
            preferred_datetime=preferred_datetime, 
            request_datetime=request_datetime
        )
        print("result = ", result)
        # Make assertions based on your expected outcomes
       # self.assertIn('error', result) # Adjust this according to expected result