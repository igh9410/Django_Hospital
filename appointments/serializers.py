from rest_framework import serializers

from appointments.models import AppointmentRequest
from doctors.models import Doctor
from patients.models import Patient


class AppointmentRequestSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), 
        source='patient',  # Maps to the 'patient' field of the model
        write_only=True
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), 
        source='doctor',  # Maps to the 'doctor' field of the model
        write_only=True
    )

    class Meta:
        model = AppointmentRequest
        fields = ['patient_id', 'doctor_id', 'preferred_datetime']

class AppointmentResponseSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    class Meta:
        model = AppointmentRequest
        fields = ['id', 'patient_name', 'doctor_name', 'preferred_datetime', 'request_expiration_datetime']

    def get_patient_name(self, obj):      
        return obj.patient.name

    def get_doctor_name(self, obj):
        return obj.doctor.name

class AppointmentRequestListSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = AppointmentRequest
        fields = ['id', 'patient_name', 'preferred_datetime', 'request_expiration_datetime']
    
    def get_patient_name(self, obj):
        return obj.patient.name

class AppointmentRequestAcceptSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    class Meta:
        model = AppointmentRequest
        fields = ['id', 'patient_name', 'preferred_datetime', 'request_expiration_datetime']

    def get_patient_name(self, obj):      
        return obj.patient.name
