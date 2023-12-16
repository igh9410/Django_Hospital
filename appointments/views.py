from django.utils import timezone
import pytz
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from appointments.serializers import AppointmentRequestSerializer
from appointments.services import create_appointment_request_service, get_appointment_request_list, update_appointment_request_status
from .models import AppointmentRequest
# Create your views here.


class AppointmentViewSet(viewsets.ViewSet):
    queryset = AppointmentRequest.objects.all()

    def create(self, request):
        serializer = AppointmentRequestSerializer(data=request.data)
        

        if serializer.is_valid():
          
            patient = serializer.validated_data['patient']  # Access the patient object
            doctor = serializer.validated_data['doctor']  # Access the doctor object
            preferred_datetime = serializer.validated_data['preferred_datetime']
            
            unconverted_datetime = timezone.now()
            seoul_timezone = pytz.timezone('Asia/Seoul')
            request_datetime = unconverted_datetime.astimezone(seoul_timezone) # The time when the API endpoint is called
           
            result = create_appointment_request_service(patient.id, doctor.id, preferred_datetime, request_datetime)
            
   
            if "error" not in result:
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result, {"error": "Error occuered for creatintg appointment request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def list_doctor_requests(self, request):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id is None:
            return Response({"error": "Doctor ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        result = get_appointment_request_list(doctor_id) # GET request, receives doctor_id as parameter

        if "error" not in result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, {"error": "Error occuered for retrieving the doctor's appointment requests" }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'])
    def accept_appointment_request(self, request, appointment_request_id):
        unconverted_datetime = timezone.now()
        seoul_timezone = pytz.timezone('Asia/Seoul')
        request_datetime = unconverted_datetime.astimezone(seoul_timezone) # The time when the API endpoint is called
           
        result = update_appointment_request_status(appointment_request_id, 'accepted', request_datetime) # Call the service method to change status 'pending' to 'accepted

        if "error" not in result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, {"error": "Error occuered for updating appointment request status to accepted"}, status=status.HTTP_400_BAD_REQUEST)

