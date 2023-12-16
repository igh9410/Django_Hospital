from datetime import time
from django.test import TestCase
from doctors.models import Doctor, NonReimbursement, Specialty, WorkingHour

from doctors.services import search_doctors_by_datetime, search_doctors_by_string
from patients.models import Patient

class DoctorServicesTest(TestCase):
    def setUp(self):
        # Create Specialties
        orthopedics = Specialty.objects.create(name='정형외과')
        general_medicine = Specialty.objects.create(name='일반의')
        internal_medicine = Specialty.objects.create(name='내과')
        oriental_medicine = Specialty.objects.create(name='한의학과')

        # Create non-reimbursements
        diet_medicine = NonReimbursement.objects.create(name='다이어트약')

        # Create doctors
        # No non_reimbursements for doctor_1
        doctor_1 = Doctor.objects.create(name='백의사', hospital='서울백병원')
        doctor_1.specialties.add(orthopedics, general_medicine, internal_medicine)
        

        # doctor_2 has non-reimubrsements (비급여)
        doctor_2 = Doctor.objects.create(name='박의사', hospital='서울백병원')
        doctor_2.specialties.add(oriental_medicine, general_medicine)
        doctor_2.non_reimbursements.add(diet_medicine)

        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for day in weekdays:
            WorkingHour.objects.create(
                doctor=doctor_1,
                day_of_week=day,
                start_time=time(9, 0),
                break_start_time=time(11, 0),
                break_end_time=time(12, 0),
                end_time=time(19, 0)
            )

        # Set working hours for doctor_2
        for day in weekdays:
            WorkingHour.objects.create(
                doctor=doctor_2,
                day_of_week=day,
                start_time=time(8, 0),
                break_start_time=time(12, 0),
                break_end_time=time(13, 0),
                end_time=time(17, 0)
            )
        # Saturday working hours for doctor_2
        WorkingHour.objects.create(
            doctor=doctor_2,
            day_of_week='Saturday',
            start_time=time(8, 0),
            end_time=time(13, 0)
        )


    def test_search_doctors_by_string_specialty(self): # Search Doctor by specialty query 
        query = "일반의"
        result = search_doctors_by_string(query) # Specailty = '일반의', 
        # Assertions about the result
        # 박의사 and 백의사 should be searched in query because they all have general medicine ("일반의") as specialties

        result_doctor_names = [doctor.name for doctor in result]

        self.assertIn("박의사", result_doctor_names, "박의사 should be in the result")
        self.assertIn("백의사", result_doctor_names, "백의사 should be in the result")


    def test_search_doctors_by_string_hospital(self): # Search Doctor by hospital name
        query = "서울백" # Search query = "서울백", 서울백병원
        result = search_doctors_by_string(query) # Hospital = "서울백병원", 
        # Assertions about the result
        # 박의사 and 백의사 should be searched in query because they all have general medicine ("일반의") as specialties

        result_doctor_names = [doctor.name for doctor in result]
        result_hospitals = [doctor.hospital for doctor in result]

        self.assertIn("박의사", result_doctor_names, "박의사 should be in the result")
        self.assertIn("백의사", result_doctor_names, "백의사 should be in the result")
        self.assertIn("서울백병원", result_hospitals, "서울백병원 should be in the result")
    
    def test_search_doctors_by_string_combined_hospital_and_doctor_name(self): # Search Doctor by combined query, either by hospital or doctor name
        query = "서울백 백의사"
        result = search_doctors_by_string(query) # Hospital = "서울백병원", Doctor = "백의사" 
        # Assertions about the result
        # 박의사 should be in the result query
        result_doctor_names = [doctor.name for doctor in result]
        result_hospitals = [doctor.hospital for doctor in result]

        self.assertIn("백의사", result_doctor_names, "백의사 should be in the result")
        self.assertIn("서울백병원", result_hospitals, "서울백병원 should be in the result")

    def test_search_doctors_by_string_combined_non_reimbursements_and_doctor_name(self): # Search Doctor by combined query, either by non-reimbursements or doctor name
        query = "다이어트 백의사"
        result = search_doctors_by_string(query) # NonReimbursement="다이어트약", Doctor = "백의사"
        # Assertions about the result
        # Result should be empty
 
        self.assertQuerysetEqual(result, [], msg="The result should be an empty queryset because 백의사 has no non-reimbursements named 다이어트약")
       
 
    def test_search_doctors_by_datetime_function(self):
        date_time1 = "2022-01-11 15:00" # 2022년 1월 11일 오후 3시
        result_1 = search_doctors_by_datetime(date_time1)
        # Assertions about the result'''
        result_1_doctor_names = [doctor.name for doctor in result_1]
        self.assertIn("박의사", result_1_doctor_names, "박의사 should be in the result_1")
        self.assertIn("백의사", result_1_doctor_names, "백의사 should be in the result_1")

        date_time2 = "2022-01-15 09:00" # 2022년 1월 15일 오전 9시
        result_2 = search_doctors_by_datetime(date_time2)
        result_2_doctor_names = [doctor.name for doctor in result_2]
        self.assertNotIn("백의사", result_2_doctor_names, "백의사 should not be in the result_2")
        self.assertIn("박의사", result_2_doctor_names, "박의사 should be in the result_2")
        