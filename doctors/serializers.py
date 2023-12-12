from rest_framework import serializers
from .models import Doctor, Specialty

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['name']

class DoctorSerializer(serializers.ModelSerializer):
    specialties = serializers.SerializerMethodField() 
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'hospital', 'specialties']

    def get_specialties(self, obj):
        return [specialty.name for specialty in obj.specialties.all()]
    
   