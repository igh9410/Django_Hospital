from datetime import datetime, time
from django.test import TestCase
from django.utils import timezone
from appointments.services import create_appointment_request_service
from doctors.models import Doctor, WorkingHour, Specialty
from patients.models import Patient

class AppointmentRequestServiceTest(TestCase):

    def test_appointment_request_service_within_working_hour(self): ## Testing with multiple request time, like night hours, holiday
        # Request time is made within Doctor's working hours        
        doctor = Doctor.objects.create(name="Doctor A", hospital="Hospital_1")
        patient = Patient.objects.create(name="Patient A")
        working_hours = []
    
        # Set up doctor's working hours
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Monday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Tuesday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Wednesday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Thursday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Friday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
       
        # Create an arbitrary datetime for request
        preferred_datetime = timezone.make_aware(datetime(2023, 12, 22, 10, 0)) ## Thursday
        request_datetime = timezone.make_aware(datetime(2023, 12, 15, 13, 0)) # Friday, 13:00
        print("WorkingHour: ", working_hours)

        # Call your service function with this arbitrary datetime
        result = create_appointment_request_service(
            patient_id=patient.id, 
            doctor_id=doctor.id, 
            preferred_datetime=preferred_datetime, 
            request_datetime=request_datetime
        )
        print("result = ", result)
        # Make assertions based on your expected outcomes
        self.assertEqual(result['patient_name'], 'Patient A')
        self.assertEqual(result['doctor_name'], 'Doctor A')
        self.assertEqual(result['preferred_datetime'], '2023-12-22T10:00:00+09:00')
        self.assertEqual(result['request_expiration_datetime'], '2023-12-15T13:20:00+09:00') # Expiration time should be set to 13:20 because request is made in 13:00, working hour, so 20 mins should be expiration time
        
    
    def test_appointment_request_service_outside_workinghour(self): ## Testing with multiple request time, like night hours, holiday
        # Request is made outside Doctor's working hours, expiration time should be set to 15 mins after the Doctor's next work hour start time        
        doctor = Doctor.objects.create(name="Doctor B", hospital="Hospital_B")
        patient = Patient.objects.create(name="Patient B")
        working_hours = []
    
        # Set up doctor's working hours
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Monday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Tuesday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Wednesday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Thursday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Friday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
       
        # Create an arbitrary datetime for request
        preferred_datetime = timezone.make_aware(datetime(2023, 12, 22, 10, 0)) ## Thursday
        request_datetime = timezone.make_aware(datetime(2023, 12, 9, 1, 0)) # Request made in Saturday 01:00 AM, Doctor is not operational.
        print("WorkingHour: ", working_hours)

        # Call your service function with this arbitrary datetime
        result = create_appointment_request_service(
            patient_id=patient.id, 
            doctor_id=doctor.id, 
            preferred_datetime=preferred_datetime, 
            request_datetime=request_datetime
        )
        print("result = ", result)
        # Make assertions based on your expected outcomes
        self.assertEqual(result['patient_name'], 'Patient B')
        self.assertEqual(result['doctor_name'], 'Doctor B')
        self.assertEqual(result['preferred_datetime'], '2023-12-22T10:00:00+09:00')
        self.assertEqual(result['request_expiration_datetime'], '2023-12-11T09:15:00+09:00') # Expiration datetime should be set to 2023-12-11 09:15 (Monday) because request is made in 01:00 AM in Saturday, which is not working hour
        # Should be expired at 09:15 AM, Monday. Doctor's working hour resumes on Monday and should be expired 15 mins after the next working hour starts      

    def test_appointment_request_service_during_lunch_break(self): ## Testing with multiple request time, like night hours, holiday
        # Request is made within Doctor's break time.        
        doctor = Doctor.objects.create(name="Doctor C", hospital="Hospital_C")
        patient = Patient.objects.create(name="Patient C")
        working_hours = []
    
        # Set up doctor's working hours
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Monday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Tuesday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Wednesday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Thursday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
        working_hours.append(WorkingHour.objects.create(
            doctor=doctor,
            day_of_week='Friday',
            start_time=time(9, 0),
            end_time=time(19, 0),
            break_start_time=time(11, 0),
            break_end_time=time(12, 0)
        ))
    
        # Create an arbitrary datetime for request
        preferred_datetime = timezone.make_aware(datetime(2023, 12, 22, 10, 0)) ## Thursday
        request_datetime = timezone.make_aware(datetime(2023, 12, 8, 11, 30)) # Request made in Friday 11:30 AM, Doctor is having lunch break.
        print("WorkingHour: ", working_hours)

        # Call your service function with this arbitrary datetime
        result = create_appointment_request_service(
            patient_id=patient.id, 
            doctor_id=doctor.id, 
            preferred_datetime=preferred_datetime, 
            request_datetime=request_datetime
        )
        print("result = ", result)
        # Make assertions based on your expected outcomes
        self.assertEqual(result['patient_name'], 'Patient C')
        self.assertEqual(result['doctor_name'], 'Doctor C')
        self.assertEqual(result['preferred_datetime'], '2023-12-22T10:00:00+09:00')
        self.assertEqual(result['request_expiration_datetime'], '2023-12-08T12:15:00+09:00') # Expiration datetime should be set to 2023-12-08 12:15 PM (Friday) because request is made in 11:30 AM in Friday. 
        # Should be expired at 12:15 PM, which is 15 mins after the lunch break ends       