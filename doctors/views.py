from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from doctors.services import search_doctors_by_datetime, search_doctors_by_string
from .models import Doctor
from .serializers import DoctorSerializer

# Create your views here.
class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return Doctor.objects.none()  # Returns an empty queryset by default
    
    @action(detail=False, methods=['get'], url_path='search-by-string')
    def search_doctors_by_string(self, request):
        search_query = request.query_params.get('string', None)
        if search_query:
            doctors = search_doctors_by_string(search_query)
            serializer = self.get_serializer(doctors, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='search-by-datetime')
    def search_doctors_by_datetime(self, request):
        datetime_query = request.query_params.get('datetime', None)
        if datetime_query:
            doctors = search_doctors_by_datetime(datetime_query)
            serializer = self.get_serializer(doctors, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


