from rest_framework import serializers
from .models import Doctor, NonReimbursement, Specialty

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['name']

class NonReimbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonReimbursement
        fields = ['name']

class DoctorSerializer(serializers.ModelSerializer):
    specialties = serializers.SerializerMethodField()
    non_reimbursements = serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'hospital', 'specialties', 'non_reimbursements']

    def get_specialties(self, obj):
        return [specialty.name for specialty in obj.specialties.all()] # Retrieve specialities by name, not primary key which is integer
    
    def get_non_reimbursements(self, obj):
        return [non_reimbursement.name for non_reimbursement in obj.non_reimbursements.all()] # Retrieve non_reimbursements by name, not primary key which is integer
    
    
   